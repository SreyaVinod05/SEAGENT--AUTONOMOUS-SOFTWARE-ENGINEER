from typing import List, Optional
from app.agents.base import BaseAgent
from app.models.schemas import (
    RequirementAnalysisResult,
    ArchitectureResult,
    GeneratedFile,
    TestExecutionReport,
    FinalReviewResult,
)


class FinalReviewAgent(BaseAgent):
    """
    Final Review Agent:
    Evaluates the complete generated software deliverable against original requirements,
    architectural decisions, and automated test results to deliver an objective
    production readiness score, limitations, and future improvements.
    """

    SYSTEM_INSTRUCTION = """You are a Lead Software Auditor and Principal QA Director in SEAGENT.
Your role is to conduct a holistic, objective final review of the generated project deliverable.

Rules:
1. Objectively evaluate requirements coverage, code quality, architecture adherence, and test outcomes.
2. Determine final status:
   - 'SUCCESS' if all core requirements are met and tests pass.
   - 'COMPLETED WITH LIMITATIONS' if tests had minor failures or some non-critical edge cases are missing.
   - 'FAILED' if critical components are fundamentally broken.
3. Score requirements coverage (1-100) and code quality (1-100).
4. Provide structured analysis of security, maintainability, strengths, limitations, and future enhancements.
5. Return structured data conforming to the FinalReviewResult schema.
"""

    def review(
        self,
        requirements: RequirementAnalysisResult,
        architecture: ArchitectureResult,
        files: List[GeneratedFile],
        test_report: Optional[TestExecutionReport] = None,
    ) -> FinalReviewResult:
        tests_summary = (
            f"Total: {test_report.total_tests}, Passed: {test_report.passed_count}, "
            f"Failed: {test_report.failed_count}, AllPassed: {test_report.all_passed}"
            if test_report
            else "No test report available"
        )

        prompt = f"""Perform a final engineering review for the project:

Project: {requirements.project_name}
Requirements: {', '.join(requirements.functional_requirements)}

Architecture: {architecture.architecture_style}
Files Generated: {', '.join(f.path for f in files)}

Test Execution Summary:
{tests_summary}

Provide a comprehensive, objective final assessment.
"""
        return self.run_prompt(
            prompt=prompt,
            schema=FinalReviewResult,
            system_instruction=self.SYSTEM_INSTRUCTION,
            temperature=0.2,
        )
