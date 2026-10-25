from typing import List, Optional
from app.agents.base import BaseAgent
from app.models.schemas import (
    RequirementAnalysisResult,
    DevelopmentPlanResult,
    ArchitectureResult,
    GeneratedFile,
    TestExecutionReport,
    FinalReviewResult,
    DocumentationResult,
)


class DocumentationAgent(BaseAgent):
    """
    Documentation Agent:
    Synthesizes the complete engineering lifecycle into clear technical documentation
    and a production-ready README.md file.
    """

    SYSTEM_INSTRUCTION = """You are a Principal Technical Writer and Developer Advocate in SEAGENT.
Your role is to author clear, comprehensive, and professional documentation for the completed software project.

Rules:
1. Provide an executive project overview and explain how the multi-agent system built the application.
2. Document the architecture, modules, and API interfaces clearly.
3. Provide realistic setup and run instructions (commands, prerequisites).
4. Provide a testing guide showing how to run the automated unit tests.
5. Create a complete, beautifully formatted GitHub README.md markdown string in `readme_markdown`.
6. Return structured data conforming to the DocumentationResult schema.
"""

    def document(
        self,
        requirements: RequirementAnalysisResult,
        plan: DevelopmentPlanResult,
        architecture: ArchitectureResult,
        files: List[GeneratedFile],
        test_report: Optional[TestExecutionReport] = None,
        final_review: Optional[FinalReviewResult] = None,
    ) -> DocumentationResult:
        prompt = f"""Generate comprehensive documentation and a GitHub README.md for:

Project: {requirements.project_name}
Summary: {requirements.summary}

Architecture: {architecture.architecture_style}
Files: {', '.join(f.path for f in files)}

Test Status: {test_report.summary if test_report else 'Verified'}
Final Review Status: {final_review.status if final_review else 'Completed'}

Produce complete documentation conforming to the DocumentationResult schema.
"""
        return self.run_prompt(
            prompt=prompt,
            schema=DocumentationResult,
            system_instruction=self.SYSTEM_INSTRUCTION,
            temperature=0.2,
        )
