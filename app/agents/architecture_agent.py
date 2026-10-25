from app.agents.base import BaseAgent
from app.models.schemas import (
    RequirementAnalysisResult,
    DevelopmentPlanResult,
    ArchitectureResult,
)


class ArchitectureAgent(BaseAgent):
    """
    Architecture Design Agent:
    Formulates a clean, modular software architecture tailored to the requirements
    and development plan. Explains architectural decisions and prevents over-engineering.
    """

    SYSTEM_INSTRUCTION = """You are a Principal Software Architect in SEAGENT.
Your mission is to design a clean, modular, maintainable software architecture for the requested system.

Rules:
1. Choose an architecture style that fits the problem domain simply and robustly. Avoid over-engineering.
2. Clearly define backend structure, data storage model, and API endpoint designs (methods, paths, bodies, responses).
3. Outline major modules, component responsibilities, and the end-to-end data flow.
4. Address real security considerations (input validation, sanitization, defensive programming) and scalability.
5. Provide explicit rationale explaining WHY this architectural approach was chosen.
6. Return structured data conforming to the ArchitectureResult schema.
"""

    def design(
        self,
        requirements: RequirementAnalysisResult,
        plan: DevelopmentPlanResult,
    ) -> ArchitectureResult:
        prompt = f"""Design the system architecture for the project:

Project: {requirements.project_name}
Summary: {requirements.summary}

Objective: {plan.project_objective}

Functional Requirements:
{chr(10).join(f"- {r}" for r in requirements.functional_requirements)}

Key Milestones:
{chr(10).join(f"- {m}" for m in plan.milestones)}

Design an elegant, modular software architecture with clear module responsibilities and API definitions.
"""
        return self.run_prompt(
            prompt=prompt,
            schema=ArchitectureResult,
            system_instruction=self.SYSTEM_INSTRUCTION,
            temperature=0.2,
        )
