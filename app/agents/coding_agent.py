from app.agents.base import BaseAgent
from app.models.schemas import (
    RequirementAnalysisResult,
    DevelopmentPlanResult,
    ArchitectureResult,
    SeniorReviewResult,
    CodeGenerationResult,
)


class CodingAgent(BaseAgent):
    """
    Code Generation Agent:
    Transforms approved requirements, development plan, and architecture into
    a complete, modular multi-file software project with automated unit tests.
    """

    SYSTEM_INSTRUCTION = """You are a Senior Full-Stack Software Engineer in SEAGENT.
Your mission is to generate clean, robust, syntactically valid source code for the requested system.

CRITICAL RULES:
1. Represent the project structurally as multiple distinct files (e.g., domain models, service layer, data store, and unit tests).
2. NEVER output placeholders, ellipses ('# TODO', 'pass', '...'), or partial snippets. Generate complete, working code.
3. Every file must be syntactically valid Python.
4. MUST include a comprehensive test file (e.g. 'test_app.py' or 'tests/test_main.py') using Python's standard `unittest` framework testing all primary requirements and edge cases.
5. Do NOT import non-standard packages that require complex external services (like Postgres or Redis); use standard Python library patterns, dataclasses, or in-memory repositories.
6. Strictly adhere to the architecture and senior review recommendations.
7. Return structured output matching the CodeGenerationResult schema with files as List[GeneratedFile].
"""

    def generate_code(
        self,
        requirements: RequirementAnalysisResult,
        plan: DevelopmentPlanResult,
        architecture: ArchitectureResult,
        senior_review: SeniorReviewResult,
    ) -> CodeGenerationResult:
        prompt = f"""Generate the complete multi-file implementation and unit tests for:

--- PROJECT ---
Name: {requirements.project_name}
Summary: {requirements.summary}

--- FUNCTIONAL REQUIREMENTS ---
{chr(10).join(f"- {fr}" for fr in requirements.functional_requirements)}

--- ARCHITECTURE DESIGN ---
Style: {architecture.architecture_style}
Modules: {', '.join(m.name for m in architecture.major_modules)}
Storage: {architecture.database_storage}

--- SENIOR REVIEW RECOMMENDATIONS ---
{chr(10).join(f"- {rec}" for rec in senior_review.recommendations)}

Generate all required source files and a complete `unittest` test suite. Return all files in the CodeGenerationResult schema.
"""
        return self.run_prompt(
            prompt=prompt,
            schema=CodeGenerationResult,
            system_instruction=self.SYSTEM_INSTRUCTION,
            temperature=0.2,
        )
