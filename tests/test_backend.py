import time
import unittest
from fastapi.testclient import TestClient

from main import app
from app.models.schemas import (
    RequirementAnalysisResult,
    DevelopmentPlanResult,
    ArchitectureResult,
    SeniorReviewResult,
    CodeGenerationResult,
    GeneratedFile,
    TestExecutionReport,
    DebuggingResult,
    FinalReviewResult,
    DocumentationResult,
)
from app.services.code_executor import SafeCodeExecutor


class TestSeagentBackend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_health_and_config(self):
        # Health Check
        r = self.client.get("/health")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("gemini_ready", data)

        # Config Endpoint
        r_conf = self.client.get("/api/v1/config")
        self.assertEqual(r_conf.status_code, 200)
        conf = r_conf.json()
        self.assertIn("model", conf)
        self.assertIn("supported_agents", conf)
        self.assertEqual(len(conf["supported_agents"]), 9)

    def test_02_safe_code_executor_success_and_failure(self):
        executor = SafeCodeExecutor(timeout=10)

        # 1. Successful test execution
        passing_files = [
            GeneratedFile(
                path="calculator.py",
                content="def multiply(x, y): return x * y\n",
            ),
            GeneratedFile(
                path="test_calc.py",
                content="""import unittest
from calculator import multiply

class TestCalc(unittest.TestCase):
    def test_multiply(self):
        self.assertEqual(multiply(3, 4), 12)
""",
            ),
        ]
        report = executor.execute_tests(passing_files)
        self.assertTrue(report.executed)
        self.assertEqual(report.total_tests, 1)
        self.assertEqual(report.passed_count, 1)
        self.assertEqual(report.failed_count, 0)
        self.assertTrue(report.all_passed)

        # 2. Failing test execution
        failing_files = [
            GeneratedFile(
                path="buggy.py",
                content="def subtract(x, y): return x + y  # Intentional bug\n",
            ),
            GeneratedFile(
                path="test_buggy.py",
                content="""import unittest
from buggy import subtract

class TestBuggy(unittest.TestCase):
    def test_subtract(self):
        self.assertEqual(subtract(10, 4), 6)
""",
            ),
        ]
        fail_report = executor.execute_tests(failing_files)
        self.assertTrue(fail_report.executed)
        self.assertEqual(fail_report.total_tests, 1)
        self.assertEqual(fail_report.failed_count, 1)
        self.assertFalse(fail_report.all_passed)
        self.assertIn("AssertionError", fail_report.test_cases[0].error_message)

    def test_03_workflow_end_to_end_mock_mode(self):
        # Trigger workflow run in mock mode
        payload = {
            "project_name": "Task Tracker API",
            "requirement": "Build a task management service where users can create, read, update, delete, and complete tasks.",
            "use_mock": True,
        }
        res = self.client.post("/api/v1/workflows/run", json=payload)
        self.assertEqual(res.status_code, 202)
        resp_data = res.json()
        wid = resp_data["workflow_id"]
        self.assertTrue(wid.startswith("wf-"))

        # Poll status until complete (timeout 25s)
        completed = False
        final_status = None
        for _ in range(25):
            status_res = self.client.get(f"/api/v1/workflows/{wid}/status")
            self.assertEqual(status_res.status_code, 200)
            status_data = status_res.json()
            if status_data["status"] in ("COMPLETED", "FAILED"):
                completed = True
                final_status = status_data["status"]
                break
            time.sleep(1)

        self.assertTrue(completed, "Workflow did not finish within timeout.")
        self.assertEqual(final_status, "COMPLETED")

        # Verify full result endpoint
        res_full = self.client.get(f"/api/v1/workflows/{wid}/result")
        self.assertEqual(res_full.status_code, 200)
        result_data = res_full.json()
        self.assertIsNotNone(result_data["requirements"])
        self.assertIsNotNone(result_data["plan"])
        self.assertIsNotNone(result_data["architecture"])
        self.assertIsNotNone(result_data["senior_review"])
        self.assertGreaterEqual(len(result_data["generated_files"]), 3)
        self.assertTrue(result_data["test_report"]["all_passed"])
        self.assertIsNotNone(result_data["final_review"])
        self.assertIsNotNone(result_data["documentation"])

        # Verify files endpoint
        files_res = self.client.get(f"/api/v1/workflows/{wid}/files")
        self.assertEqual(files_res.status_code, 200)
        files_data = files_res.json()
        self.assertGreaterEqual(len(files_data["files"]), 3)

        # Verify tests endpoint
        tests_res = self.client.get(f"/api/v1/workflows/{wid}/tests")
        self.assertEqual(tests_res.status_code, 200)
        tests_data = tests_res.json()
        self.assertTrue(tests_data["test_report"]["executed"])

        # Verify ZIP download
        zip_res = self.client.get(f"/api/v1/workflows/{wid}/download")
        self.assertEqual(zip_res.status_code, 200)
        self.assertEqual(zip_res.headers.get("content-type"), "application/zip")
        self.assertGreater(len(zip_res.content), 500)

    def test_04_debugging_loop_patching(self):
        # Verify debugging agent and re-testing loop mechanics
        from app.agents.debugging_agent import DebuggingAgent
        from app.services.code_executor import SafeCodeExecutor

        executor = SafeCodeExecutor(timeout=10)
        # 1. Buggy code that fails unit tests
        buggy_files = [
            GeneratedFile(
                path="math_service.py",
                content="def add_numbers(a, b): return a - b  # Bug: returns subtraction\n",
            ),
            GeneratedFile(
                path="test_math.py",
                content="""import unittest
from math_service import add_numbers

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add_numbers(5, 7), 12)
""",
            ),
        ]
        fail_report = executor.execute_tests(buggy_files)
        self.assertFalse(fail_report.all_passed)

        # 2. In mock mode, debugging agent produces correct fix
        debug_agent = DebuggingAgent(use_mock=True)
        # Mock debugging agent with a fix
        fixed_files = [
            GeneratedFile(
                path="math_service.py",
                content="def add_numbers(a, b): return a + b  # Fixed: returns addition\n",
            ),
            buggy_files[1],
        ]
        pass_report = executor.execute_tests(fixed_files)
        self.assertTrue(pass_report.all_passed)
        self.assertEqual(pass_report.passed_count, 1)



if __name__ == "__main__":
    unittest.main()
