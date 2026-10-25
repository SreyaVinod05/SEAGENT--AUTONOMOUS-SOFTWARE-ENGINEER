import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import List

from app.config import CODE_EXECUTION_TIMEOUT_SECONDS
from app.models.schemas import (
    GeneratedFile,
    TestExecutionReport,
    TestCaseResult,
)

logger = logging.getLogger("seagent.executor")

RUNNER_SCRIPT = '''import unittest
import json
import sys
import time
import os

class StructuredResult(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.records = []
        self._start_time = None

    def startTest(self, test):
        super().startTest(test)
        self._start_time = time.time()

    def addSuccess(self, test):
        super().addSuccess(test)
        duration = time.time() - (self._start_time or time.time())
        self.records.append({
            "name": str(test),
            "status": "PASSED",
            "error_message": None,
            "duration": round(duration, 4)
        })

    def addFailure(self, test, err):
        super().addFailure(test, err)
        duration = time.time() - (self._start_time or time.time())
        msg = self._exc_info_to_string(err, test)
        self.records.append({
            "name": str(test),
            "status": "FAILED",
            "error_message": msg.strip(),
            "duration": round(duration, 4)
        })

    def addError(self, test, err):
        super().addError(test, err)
        duration = time.time() - (self._start_time or time.time())
        msg = self._exc_info_to_string(err, test)
        self.records.append({
            "name": str(test),
            "status": "ERROR",
            "error_message": msg.strip(),
            "duration": round(duration, 4)
        })

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.records.append({
            "name": str(test),
            "status": "SKIPPED",
            "error_message": reason,
            "duration": 0.0
        })

def run_suite():
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=".", pattern="test*.py")
    runner_result = StructuredResult()
    start_total = time.time()
    suite.run(runner_result)
    total_time = time.time() - start_total

    output = {
        "total": runner_result.testsRun,
        "passed": len([r for r in runner_result.records if r["status"] == "PASSED"]),
        "failed": len([r for r in runner_result.records if r["status"] in ("FAILED", "ERROR")]),
        "skipped": len(runner_result.skipped),
        "total_time": round(total_time, 4),
        "records": runner_result.records
    }
    print("---SEAGENT_TEST_OUTPUT_START---")
    print(json.dumps(output))
    print("---SEAGENT_TEST_OUTPUT_END---")

if __name__ == "__main__":
    run_suite()
'''


class SafeCodeExecutor:
    """
    Isolated and restricted execution engine for generated code and tests.
    Executes tests within an ephemeral sandbox workspace, applies timeouts,
    filters sensitive environment variables, captures output, and cleans up.
    """

    def __init__(self, timeout: int = CODE_EXECUTION_TIMEOUT_SECONDS):
        self.timeout = timeout

    def execute_tests(self, files: List[GeneratedFile]) -> TestExecutionReport:
        if not files:
            return TestExecutionReport(
                executed=False,
                summary="No files provided to execute.",
                all_passed=False,
            )

        temp_dir = tempfile.mkdtemp(prefix="seagent_sandbox_")
        start_time = time.time()

        try:
            # 1. Safely write files to temporary workspace
            for f in files:
                rel_path = f.path.replace("\\", "/").strip().lstrip("/")
                # Prevent directory traversal attacks
                if ".." in rel_path or rel_path.startswith("/"):
                    continue

                target_path = Path(temp_dir) / rel_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                with open(target_path, "w", encoding="utf-8") as out:
                    out.write(f.content)

            # 2. Write test runner script
            runner_file = Path(temp_dir) / "_seagent_runner.py"
            with open(runner_file, "w", encoding="utf-8") as out:
                out.write(RUNNER_SCRIPT)

            # 3. Create sanitized execution environment
            safe_env = os.environ.copy()
            # Strip secrets and sensitive keys
            for secret_var in [
                "GEMINI_API_KEY",
                "OPENAI_API_KEY",
                "ANTHROPIC_API_KEY",
                "AWS_SECRET_ACCESS_KEY",
                "GITHUB_TOKEN",
            ]:
                safe_env.pop(secret_var, None)

            safe_env["PYTHONPATH"] = temp_dir
            safe_env["PYTHONDONTWRITEBYTECODE"] = "1"

            # 4. Execute test runner in isolated subprocess
            try:
                proc = subprocess.run(
                    [sys.executable, str(runner_file)],
                    cwd=temp_dir,
                    env=safe_env,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                )
                stdout = proc.stdout
                stderr = proc.stderr
                returncode = proc.returncode

            except subprocess.TimeoutExpired:
                total_duration = time.time() - start_time
                return TestExecutionReport(
                    executed=True,
                    total_tests=0,
                    passed_count=0,
                    failed_count=1,
                    execution_time_seconds=round(total_duration, 4),
                    all_passed=False,
                    stdout="",
                    stderr=f"Execution timed out after {self.timeout} seconds.",
                    summary="Test execution aborted due to timeout.",
                    test_cases=[
                        TestCaseResult(
                            name="ExecutionTimeout",
                            status="FAILED",
                            error_message=f"Process exceeded timeout limit of {self.timeout}s",
                        )
                    ],
                )

            # 5. Parse test execution results
            total_duration = time.time() - start_time
            return self._parse_runner_output(stdout, stderr, total_duration)

        except Exception as e:
            logger.error(f"Error in safe code executor: {e}")
            total_duration = time.time() - start_time
            return TestExecutionReport(
                executed=False,
                total_tests=0,
                passed_count=0,
                failed_count=1,
                execution_time_seconds=round(total_duration, 4),
                all_passed=False,
                stdout="",
                stderr=str(e),
                summary=f"Safe execution setup error: {str(e)}",
            )
        finally:
            # 6. Strict cleanup of sandbox directory
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception as clean_err:
                logger.warning(f"Failed to clean sandbox {temp_dir}: {clean_err}")

    def _parse_runner_output(
        self,
        stdout: str,
        stderr: str,
        duration: float,
    ) -> TestExecutionReport:
        if "---SEAGENT_TEST_OUTPUT_START---" in stdout:
            try:
                parts = stdout.split("---SEAGENT_TEST_OUTPUT_START---")[1]
                json_str = parts.split("---SEAGENT_TEST_OUTPUT_END---")[0].strip()
                data = json.loads(json_str)

                test_cases = [
                    TestCaseResult(
                        name=rec["name"],
                        status=rec["status"],
                        error_message=rec.get("error_message"),
                        duration_seconds=rec.get("duration", 0.0),
                    )
                    for rec in data.get("records", [])
                ]

                total = data.get("total", 0)
                passed = data.get("passed", 0)
                failed = data.get("failed", 0)
                skipped = data.get("skipped", 0)
                all_passed = total > 0 and failed == 0

                summary = (
                    f"Executed {total} tests: {passed} passed, {failed} failed in {duration:.2f}s."
                )

                return TestExecutionReport(
                    executed=True,
                    total_tests=total,
                    passed_count=passed,
                    failed_count=failed,
                    skipped_count=skipped,
                    execution_time_seconds=round(duration, 4),
                    all_passed=all_passed,
                    test_cases=test_cases,
                    stdout=stdout,
                    stderr=stderr,
                    summary=summary,
                )
            except Exception as parse_err:
                logger.error(f"Failed to parse structured test output: {parse_err}")

        # Fallback if runner encountered top-level syntax error in user code
        summary = "No tests discovered or error during module loading."
        if stderr:
            summary = f"Execution failed during test loading: {stderr[:200]}"

        return TestExecutionReport(
            executed=True,
            total_tests=0,
            passed_count=0,
            failed_count=1 if stderr else 0,
            execution_time_seconds=round(duration, 4),
            all_passed=False,
            test_cases=[
                TestCaseResult(
                    name="ModuleLoadCheck",
                    status="FAILED" if stderr else "SKIPPED",
                    error_message=stderr if stderr else "No tests found.",
                )
            ],
            stdout=stdout,
            stderr=stderr,
            summary=summary,
        )
