from typing import List, Optional, Dict, Any
from typing_extensions import TypedDict

from app.models.schemas import (
    WorkflowStatus,
    RequirementAnalysisResult,
    DevelopmentPlanResult,
    ArchitectureResult,
    SeniorReviewResult,
    GeneratedFile,
    TestExecutionReport,
    DebuggingResult,
    SecurityReviewResult,
    CodeOptimizationResult,
    FinalReviewResult,
    DocumentationResult,
    WorkflowLogEntry,
)


class WorkflowState(TypedDict, total=False):
    workflow_id: str
    project_name: str
    user_requirement: str
    tech_preferences: str
    provider: str
    use_mock: bool
    
    status: str
    current_agent: str
    current_step: int
    progress_percentage: int
    
    requirements: Optional[RequirementAnalysisResult]
    plan: Optional[DevelopmentPlanResult]
    architecture: Optional[ArchitectureResult]
    senior_review: Optional[SeniorReviewResult]
    senior_review_revisions: int
    
    generated_files: List[GeneratedFile]
    test_report: Optional[TestExecutionReport]
    debugging_history: List[DebuggingResult]
    
    retry_count: int
    max_retries: int
    
    security_review: Optional[SecurityReviewResult]
    optimization: Optional[CodeOptimizationResult]
    
    final_review: Optional[FinalReviewResult]
    documentation: Optional[DocumentationResult]
    
    errors: List[str]
    logs: List[WorkflowLogEntry]
    start_time: str
    end_time: Optional[str]
