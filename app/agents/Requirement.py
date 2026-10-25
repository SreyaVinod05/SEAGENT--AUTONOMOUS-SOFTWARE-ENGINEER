"""
Requirement Analysis Agent module.
Preserved for backward-compatibility while routing to the new RequirementsAgent.
"""
from typing import Optional, Any
from app.agents.requirements_agent import RequirementsAgent
from app.models.schemas import RequirementAnalysisResult


class RequirementAnalysisAgent:
    """
    Adapter class for backward compatibility with existing project scripts.
    """

    def __init__(self, provider: Optional[Any] = None, use_mock: bool = False):
        self._agent = RequirementsAgent(provider=provider, use_mock=use_mock)

    def analyze(self, user_requirement: str) -> dict:
        """
        Analyze user requirement and return dictionary representation.
        If provider is not configured or in fallback, returns structured analysis.
        """
        if not user_requirement or not user_requirement.strip():
            return {
                "status": "error",
                "message": "Requirement cannot be empty."
            }

        try:
            result = self._agent.analyze(user_requirement)
            return {
                "status": "success",
                "original_requirement": user_requirement,
                "analysis": result.model_dump(),
            }
        except Exception as e:
            # Fallback for offline execution if key is missing
            return {
                "status": "error",
                "message": str(e),
                "original_requirement": user_requirement,
            }