from typing import Optional, Any
from app.agents.base import BaseAgent
from app.models.schemas import RequirementAnalysisResult


class RequirementsAgent(BaseAgent):
    """
    Requirements Analysis Agent:
    Analyzes natural-language software requirements and extracts structured functional
    and non-functional requirements, constraints, assumptions, actors, use cases,
    and acceptance criteria.
    Does NOT generate implementation code.
    """

    SYSTEM_INSTRUCTION = """You are a Principal Software Requirements Engineer in SEAGENT, an AI software engineering team.
Your sole mission is to thoroughly analyze the user's natural-language software requirement and produce a comprehensive, structured requirements specification.

Rules:
1. Focus entirely on WHAT the system must do and WHY, NOT on writing implementation code.
2. Break down vague statements into concrete, unambiguous functional requirements.
3. Identify critical non-functional requirements (performance, usability, reliability, security).
4. Identify realistic assumptions, technical constraints, user actors, and essential use cases.
5. Formulate precise, verifiable acceptance criteria.
6. Return structured data conforming to the RequirementAnalysisResult schema.
"""

    def analyze(self, user_requirement: str, tech_preferences: Optional[str] = "") -> RequirementAnalysisResult:
        if not user_requirement or not user_requirement.strip():
            raise ValueError("Requirement cannot be empty.")

        prompt = f"""Analyze the following software engineering requirement:

--- USER REQUIREMENT ---
{user_requirement.strip()}

--- TECHNOLOGY PREFERENCES / CONSTRAINTS ---
{tech_preferences.strip() if tech_preferences else 'Standard production best practices'}

Provide a rigorous, structured requirement analysis.
"""
        return self.run_prompt(
            prompt=prompt,
            schema=RequirementAnalysisResult,
            system_instruction=self.SYSTEM_INSTRUCTION,
            temperature=0.2,
        )
