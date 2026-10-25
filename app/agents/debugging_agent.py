from typing import List, Optional
from app.agents.base import BaseAgent
from app.models.schemas import (
    GeneratedFile,
    TestExecutionReport,
    RequirementAnalysisResult,
    ArchitectureResult,
    DebuggingResult,
)


class DebuggingAgent(BaseAgent):
    """
    Automated Debugging and Patching Agent:
    Analyzes failed test reports, execution errors, and tracebacks, identifies root causes,
    and produces corrected, full source code files for iterative re-testing.
    """

    SYSTEM_INSTRUCTION = """You are an Expert Diagnostic and Debugging Engineer in SEAGENT.
Your mission is to analyze test failures, tracebacks, and source code, locate the root cause,
and provide the corrected, complete source code.

Rules:
1. Examine the failed test names, assertion errors, and traceback logs carefully.
2. Determine precisely which file(s) and function(s) caused the failure.
3. Formulate a minimal, correct fix that preserves all existing requirements.
4. Return the complete corrected files in `corrected_files: List[GeneratedFile]`. Each file must contain the FULL, complete code (no diffs, no placeholders).
5. Explain the root cause and proposed fix clearly.
6. Return structured data conforming to the DebuggingResult schema.
"""

    def debug(
        self,
        files: List[GeneratedFile],
        test_report: TestExecutionReport,
        requirements: Optional[RequirementAnalysisResult] = None,
        architecture: Optional[ArchitectureResult] = None,
    ) -> DebuggingResult:
        failed_cases_str = "\n".join(
            f"Case: {tc.name} | Status: {tc.status} | Error: {tc.error_message}"
            for tc in test_report.test_cases
            if tc.status in ("FAILED", "ERROR")
        )

        files_formatted = "\n".join(f"=== Path: {f.path} ===\n{f.content}\n" for f in files)
        reqs_formatted = "\n".join(f"- {fr}" for fr in requirements.functional_requirements) if requirements else "Standard functionality"

        prompt = f"""Debug the following test failures in the software project:

--- FAILED TESTS & TRACEBACK ---
{failed_cases_str if failed_cases_str else 'General Execution Failure'}
STDERR:
{test_report.stderr}
STDOUT:
{test_report.stdout}

--- EXISTING CODE FILES ---
{files_formatted}

--- REQUIREMENTS CONTEXT ---
{reqs_formatted}

Identify the root cause, proposed fix, and provide the complete corrected source code for the affected files.
"""
        return self.run_prompt(
            prompt=prompt,
            schema=DebuggingResult,
            system_instruction=self.SYSTEM_INSTRUCTION,
            temperature=0.2,
        )
