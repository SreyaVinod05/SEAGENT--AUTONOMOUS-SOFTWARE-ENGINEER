from app.agents.requirements_agent import RequirementsAgent
from app.agents.planning_agent import PlanningAgent
from app.agents.architecture_agent import ArchitectureAgent
from app.agents.senior_engineer_agent import SeniorEngineerAgent
from app.agents.coding_agent import CodingAgent
from app.agents.testing_agent import TestingAgent
from app.agents.debugging_agent import DebuggingAgent
from app.agents.security_review_agent import SecurityReviewAgent
from app.agents.code_optimization_agent import CodeOptimizationAgent
from app.agents.final_review_agent import FinalReviewAgent
from app.agents.documentation_agent import DocumentationAgent
from app.agents.Requirement import RequirementAnalysisAgent

# SeniorReasoningAgent alias per project proposal
SeniorReasoningAgent = SeniorEngineerAgent

__all__ = [
    "RequirementsAgent",
    "PlanningAgent",
    "ArchitectureAgent",
    "SeniorEngineerAgent",
    "SeniorReasoningAgent",
    "CodingAgent",
    "TestingAgent",
    "DebuggingAgent",
    "SecurityReviewAgent",
    "CodeOptimizationAgent",
    "FinalReviewAgent",
    "DocumentationAgent",
    "RequirementAnalysisAgent",
]
