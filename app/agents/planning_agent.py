from app.agents.base import BaseAgent
from app.models.schemas import RequirementAnalysisResult, DevelopmentPlanResult


class PlanningAgent(BaseAgent):
    """
    Development Planning Agent:
    Transforms structured requirements into an ordered, milestone-driven technical
    development plan with clear dependencies and priority sequencing.
    """

    SYSTEM_INSTRUCTION = """You are a Technical Project Lead and Engineering Manager in SEAGENT.
Your role is to formulate a pragmatic, structured development plan based on the analyzed software requirements.

Rules:
1. Define a clear, focused project objective.
2. Outline ordered development steps starting from core foundation/domain models, service layer, through to automated testing.
3. For each step, define clear deliverables, step dependencies, and implementation priority (High/Medium/Low).
4. Establish major milestones and list required dependencies.
5. Avoid introducing unnecessary external technologies or overly complex tooling.
6. Return structured data conforming to the DevelopmentPlanResult schema.
"""

    def plan(self, requirements: RequirementAnalysisResult) -> DevelopmentPlanResult:
        prompt = f"""Create a development plan for the following project requirements:

Project Name: {requirements.project_name}
Summary: {requirements.summary}

Functional Requirements:
{chr(10).join(f"- {fr}" for fr in requirements.functional_requirements)}

Constraints & Assumptions:
{chr(10).join(f"- {c}" for c in requirements.constraints + requirements.assumptions)}

Acceptance Criteria:
{chr(10).join(f"- {ac}" for ac in requirements.acceptance_criteria)}

Produce an ordered, actionable development plan.
"""
        return self.run_prompt(
            prompt=prompt,
            schema=DevelopmentPlanResult,
            system_instruction=self.SYSTEM_INSTRUCTION,
            temperature=0.2,
        )
