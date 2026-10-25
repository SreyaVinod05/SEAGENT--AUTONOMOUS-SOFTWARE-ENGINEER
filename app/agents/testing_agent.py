import logging
from typing import List, Optional, Any
from app.agents.base import BaseAgent
from app.models.schemas import (
    GeneratedFile,
    TestExecutionReport,
    RequirementAnalysisResult,
    ArchitectureResult,
)
from app.services.code_executor import SafeCodeExecutor

logger = logging.getLogger("seagent.testing")


class TestingAgent(BaseAgent):
    """
    Automated Testing Agent:
    Analyzes generated implementation, ensures appropriate test files exist,
    executes tests safely in an isolated sandbox, and collects authentic test outcomes.
    """

    SYSTEM_INSTRUCTION = """You are a Lead QA and Test Automation Engineer in SEAGENT.
Your role is to inspect the software codebase and generate comprehensive, robust unit tests
using Python's standard `unittest` framework.

Rules:
1. Generate test cases covering both expected behavior and edge cases (e.g. invalid inputs, empty values, boundaries).
2. The generated test file must be a complete, self-contained Python script using standard `unittest`.
3. Return the test file as a GeneratedFile.
"""

    def __init__(
        self,
        provider: Optional[Any] = None,
        use_mock: bool = False,
        provider_name: Optional[str] = None,
    ):
        super().__init__(provider=provider, use_mock=use_mock, provider_name=provider_name)
        self.executor = SafeCodeExecutor()

    def run_tests(
        self,
        files: List[GeneratedFile],
        requirements: Optional[RequirementAnalysisResult] = None,
        architecture: Optional[ArchitectureResult] = None,
    ) -> TestExecutionReport:
        """
        Executes the tests against the generated files in an isolated execution sandbox.
        """
        # Check if a test file already exists
        has_tests = any("test" in f.path.lower() for f in files)

        files_to_test = list(files)

        # If no tests exist in generated files, generate a test suite
        if not has_tests and requirements:
            try:
                test_file = self._generate_test_suite(files, requirements, architecture)
                if test_file:
                    files_to_test.append(test_file)
            except Exception as e:
                logger.warning(f"Could not automatically generate missing test file: {e}")

        # Safely execute the tests
        report = self.executor.execute_tests(files_to_test)
        return report

    def _generate_test_suite(
        self,
        files: List[GeneratedFile],
        requirements: RequirementAnalysisResult,
        architecture: Optional[ArchitectureResult],
    ) -> Optional[GeneratedFile]:
        """Generate test cases if the coding agent did not include them."""
        files_formatted = "\n".join(f"--- File: {f.path} ---\n{f.content}" for f in files)
        reqs_formatted = "\n".join(f"- {fr}" for fr in requirements.functional_requirements)
        prompt = f"""Generate a comprehensive unittest suite for the following files:

{files_formatted}

Requirements:
{reqs_formatted}

Create a complete `test_suite.py` file with standard `unittest` test cases.
"""
        result = self.run_prompt(
            prompt=prompt,
            schema=GeneratedFile,
            system_instruction=self.SYSTEM_INSTRUCTION,
            temperature=0.2,
        )
        if not result.path.endswith(".py"):
            result.path = "test_generated.py"
        return result
