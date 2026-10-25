from app.agents.base import BaseAgent
from app.models.schemas import (
    RequirementAnalysisResult,
    DevelopmentPlanResult,
    ArchitectureResult,
    SeniorReviewResult,
)


class SeniorEngineerAgent(BaseAgent):
    """
    Senior Engineer Review Agent:
    Acts as a staff/principal engineering reviewer assessing the requirements, plan,
    and architecture for flaws, contradictions, over-engineering, security vulnerabilities,
    and maintainability before code generation begins.
    """

    SYSTEM_INSTRUCTION = """You are a Staff / Principal Engineer and Tech Lead conducting a rigorous architecture review in SEAGENT.
Your role is to rigorously review the software requirements, development plan, and proposed architecture before approval.

Rules:
1. Examine for contradictions, missing requirements, unnecessary complexity, and security/reliability hazards.
2. Evaluate if the architecture is practical, cleanly modularized, and directly testable in Python.
3. If the design is sound and ready for coding, set approved = True.
4. If critical issues or fatal flaws exist, set approved = False, specify the revision_target ('requirements', 'plan', or 'architecture'), and provide concrete recommendations.
5. Provide actionable recommendations and strengths.
6. Return structured data conforming to the SeniorReviewResult schema.
"""

    def review(
        self,
        requirements: RequirementAnalysisResult,
        plan: DevelopmentPlanResult,
        architecture: ArchitectureResult,
    ) -> SeniorReviewResult:
        prompt = f"""Conduct a thorough Senior Engineering Review for:

--- REQUIREMENTS ---
Project: {requirements.project_name}
Summary: {requirements.summary}
Functional Requirements count: {len(requirements.functional_requirements)}
Acceptance Criteria: {chr(10).join(f"- {ac}" for ac in requirements.acceptance_criteria)}

--- PLAN ---
Objective: {plan.project_objective}
Steps count: {len(plan.steps)}

--- ARCHITECTURE ---
Style: {architecture.architecture_style}
Backend: {architecture.backend_architecture}
Database/Storage: {architecture.database_storage}
Rationale: {architecture.architectural_decisions_rationale}

Assess feasibility, modularity, security, and testability. Make an explicit approval determination.
"""
        return self.run_prompt(
            prompt=prompt,
            schema=SeniorReviewResult,
            system_instruction=self.SYSTEM_INSTRUCTION,
            temperature=0.2,
        )
