from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


# -------------------------------------------------------------
# Workflow Lifecycle Enums
# -------------------------------------------------------------

class WorkflowStatus(str, Enum):
    IDLE = "IDLE"
    ANALYZING_REQUIREMENTS = "ANALYZING_REQUIREMENTS"
    PLANNING = "PLANNING"
    DESIGNING_ARCHITECTURE = "DESIGNING_ARCHITECTURE"
    SENIOR_REVIEW = "SENIOR_REVIEW"
    GENERATING_CODE = "GENERATING_CODE"
    TESTING = "TESTING"
    DEBUGGING = "DEBUGGING"
    RETESTING = "RETESTING"
    SECURITY_REVIEW = "SECURITY_REVIEW"
    OPTIMIZING_CODE = "OPTIMIZING_CODE"
    FINAL_REVIEW = "FINAL_REVIEW"
    DOCUMENTATION = "DOCUMENTATION"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"



# -------------------------------------------------------------
# Agent 1: Requirements Analysis
# -------------------------------------------------------------

class RequirementAnalysisResult(BaseModel):
    project_name: str = Field(description="Short, descriptive project name")
    summary: str = Field(description="Summary of the user requirement")
    functional_requirements: List[str] = Field(default_factory=list, description="List of functional capabilities required")
    non_functional_requirements: List[str] = Field(default_factory=list, description="Performance, security, usability, etc.")
    assumptions: List[str] = Field(default_factory=list, description="Assumptions made about the domain, environment, users")
    constraints: List[str] = Field(default_factory=list, description="Technical or business boundaries/constraints")
    actors: List[str] = Field(default_factory=list, description="Identified user roles or external actors")
    use_cases: List[str] = Field(default_factory=list, description="Key use case scenarios")
    acceptance_criteria: List[str] = Field(default_factory=list, description="Clear measurable acceptance criteria")


# -------------------------------------------------------------
# Agent 2: Development Planning
# -------------------------------------------------------------

class DevelopmentStep(BaseModel):
    step_number: int = Field(description="Step order number starting at 1")
    title: str = Field(description="Short title of the step")
    description: str = Field(description="What needs to be implemented or configured")
    deliverable: str = Field(description="Concrete deliverable produced in this step")
    dependencies: List[str] = Field(default_factory=list, description="Prerequisite step titles or components")
    priority: str = Field(default="High", description="Priority level: High, Medium, Low")


class DevelopmentPlanResult(BaseModel):
    project_objective: str = Field(description="Core project objective statement")
    steps: List[DevelopmentStep] = Field(default_factory=list, description="Ordered implementation steps")
    milestones: List[str] = Field(default_factory=list, description="Key progress milestones")
    deliverables: List[str] = Field(default_factory=list, description="Major project deliverables")
    dependencies: List[str] = Field(default_factory=list, description="System or package dependencies")
    implementation_priorities: List[str] = Field(default_factory=list, description="Prioritized focal points")


# -------------------------------------------------------------
# Agent 3: Architecture Design
# -------------------------------------------------------------

class APIEndpoint(BaseModel):
    method: str = Field(description="HTTP method (GET, POST, PUT, DELETE)")
    path: str = Field(description="Endpoint URL path")
    description: str = Field(description="What this endpoint does")
    request_body: Optional[str] = Field(default=None, description="Expected request payload schema description")
    response: str = Field(description="Expected response schema description")


class ModuleDesign(BaseModel):
    name: str = Field(description="Module or package name")
    responsibility: str = Field(description="What this module is responsible for")
    key_classes_or_functions: List[str] = Field(default_factory=list, description="Key classes or functions")


class ArchitectureResult(BaseModel):
    architecture_style: str = Field(description="Style e.g., Layered Modular Architecture, REST Micro-service")
    frontend_architecture: str = Field(description="Frontend structure, components, state management")
    backend_architecture: str = Field(description="Backend layers, framework choice, routing")
    database_storage: str = Field(description="Database or data storage design, schemas, tables/models")
    api_design: List[APIEndpoint] = Field(default_factory=list, description="Core REST API endpoints")
    major_modules: List[ModuleDesign] = Field(default_factory=list, description="Component modules and responsibilities")
    component_responsibilities: List[str] = Field(default_factory=list, description="Key responsibilities breakdown")
    data_flow: List[str] = Field(default_factory=list, description="Step-by-step description of data flow")
    security_considerations: List[str] = Field(default_factory=list, description="Security safeguards and validations")
    scalability_considerations: List[str] = Field(default_factory=list, description="Scalability considerations")
    architectural_decisions_rationale: str = Field(description="Justification for design choices and avoiding over-engineering")


# -------------------------------------------------------------
# Agent 4: Senior Engineer Review
# -------------------------------------------------------------

class SeniorReviewResult(BaseModel):
    approved: bool = Field(description="True if architecture and plan meet senior engineering standards")
    overall_score: int = Field(default=8, description="Engineering quality score from 1 to 10")
    strengths: List[str] = Field(default_factory=list, description="Key strengths of the design")
    issues: List[str] = Field(default_factory=list, description="Identified design gaps, complexities, or risks")
    recommendations: List[str] = Field(default_factory=list, description="Actionable technical recommendations")
    revision_target: Optional[str] = Field(default="none", description="'none', 'requirements', 'plan', or 'architecture'")


# -------------------------------------------------------------
# Agent 5: Code Generation
# -------------------------------------------------------------

class GeneratedFile(BaseModel):
    path: str = Field(description="Relative file path e.g. 'app/main.py' or 'tests/test_tasks.py'")
    content: str = Field(description="Complete, syntactically valid source code")
    description: str = Field(default="", description="Brief explanation of the file's role")


class CodeGenerationResult(BaseModel):
    project_summary: str = Field(description="Overview of the generated implementation")
    files: List[GeneratedFile] = Field(default_factory=list, description="List of generated source code and test files")


# -------------------------------------------------------------
# Agent 6: Testing & Safe Execution
# -------------------------------------------------------------

class TestCaseResult(BaseModel):
    name: str = Field(description="Test function or test case name")
    status: str = Field(description="PASSED, FAILED, or ERROR")
    error_message: Optional[str] = Field(default=None, description="Traceback or assertion failure message")
    duration_seconds: float = Field(default=0.0, description="Execution time for this test")


class TestExecutionReport(BaseModel):
    executed: bool = Field(default=False, description="Whether tests were physically executed in the safe environment")
    total_tests: int = Field(default=0, description="Total number of test cases found")
    passed_count: int = Field(default=0, description="Number of passed tests")
    failed_count: int = Field(default=0, description="Number of failed tests")
    skipped_count: int = Field(default=0, description="Number of skipped tests")
    execution_time_seconds: float = Field(default=0.0, description="Total run duration")
    all_passed: bool = Field(default=False, description="True only if total_tests > 0 and failed_count == 0")
    test_cases: List[TestCaseResult] = Field(default_factory=list, description="Detailed test case outcomes")
    stdout: str = Field(default="", description="Captured standard output from the test runner")
    stderr: str = Field(default="", description="Captured standard error or tracebacks")
    summary: str = Field(default="", description="High-level evaluation of test results")


# -------------------------------------------------------------
# Agent 7: Debugging
# -------------------------------------------------------------

class DebuggingResult(BaseModel):
    root_cause: str = Field(description="Detailed analysis of why the test(s) failed")
    affected_files: List[str] = Field(default_factory=list, description="Paths of files that had bugs")
    proposed_fix: str = Field(description="Description of what was changed and why")
    corrected_files: List[GeneratedFile] = Field(default_factory=list, description="List of files with corrected code")


# -------------------------------------------------------------
# Agent 8: Security Review Agent
# -------------------------------------------------------------

class SecurityVulnerability(BaseModel):
    severity: str = Field(description="'CRITICAL', 'HIGH', 'MEDIUM', or 'LOW'")
    vulnerability_type: str = Field(description="Vulnerability category e.g., 'SQL Injection Risk', 'Hardcoded Secret', 'CORS Misconfiguration'")
    file_path: str = Field(description="Target file path containing the vulnerability")
    line_number: Optional[int] = Field(default=None, description="Line number if known")
    description: str = Field(description="Detailed explanation of the vulnerability and risk")
    remediation: str = Field(description="Actionable fix or code patch to eliminate the vulnerability")


class SecurityReviewResult(BaseModel):
    security_score: int = Field(default=95, description="Security health score from 1 to 100")
    status: str = Field(description="'PASSED', 'WARNINGS_DETECTED', or 'NEEDS_REMEDIATION'")
    vulnerabilities: List[SecurityVulnerability] = Field(default_factory=list, description="List of detected vulnerabilities")
    owasp_compliance: List[str] = Field(default_factory=list, description="OWASP compliance verification checklist")
    secure_design_patterns: List[str] = Field(default_factory=list, description="Security patterns successfully implemented")
    remediation_steps: List[str] = Field(default_factory=list, description="Recommendations to strengthen system defenses")
    summary: str = Field(description="Executive summary of the security audit")


# -------------------------------------------------------------
# Agent 9: Code Optimization Agent
# -------------------------------------------------------------

class OptimizedFileDetail(BaseModel):
    path: str = Field(description="File path that was analyzed or optimized")
    optimization_type: str = Field(description="Type e.g., 'Algorithmic Complexity', 'Memory Efficiency', 'Caching', 'Refactoring'")
    time_complexity_before: str = Field(default="O(N)", description="Estimated time complexity before")
    time_complexity_after: str = Field(default="O(1)", description="Estimated time complexity after optimization")
    space_complexity_before: str = Field(default="O(N)", description="Space complexity before")
    space_complexity_after: str = Field(default="O(1)", description="Space complexity after")
    changes_made: str = Field(description="Specific refactoring or optimization applied")


class CodeOptimizationResult(BaseModel):
    overall_improvement_summary: str = Field(description="Summary of performance, readability, and complexity improvements")
    performance_rating: int = Field(default=92, description="Performance efficiency rating from 1 to 100")
    estimated_speedup: str = Field(default="25-40% throughput increase", description="Estimated algorithmic or execution speedup")
    file_optimizations: List[OptimizedFileDetail] = Field(default_factory=list, description="Per-file optimization breakdown")
    optimized_files: List[GeneratedFile] = Field(default_factory=list, description="Refactored code files with optimizations applied")
    best_practices_applied: List[str] = Field(default_factory=list, description="Software engineering optimizations implemented")


# -------------------------------------------------------------
# Agent 10: Final Review
# -------------------------------------------------------------

class FinalReviewResult(BaseModel):
    status: str = Field(description="'SUCCESS', 'COMPLETED WITH LIMITATIONS', or 'FAILED'")
    requirements_coverage_score: int = Field(default=95, description="Percentage (1-100) of requirements satisfied")
    code_quality_score: int = Field(default=90, description="Code quality rating (1-100)")
    test_coverage_summary: str = Field(description="Evaluation of automated test coverage and verification")
    security_assessment: str = Field(description="Review of security practices and input handling")
    maintainability_assessment: str = Field(description="Review of code structure, readability, and modularity")
    strengths: List[str] = Field(default_factory=list, description="Noteworthy strengths of the final solution")
    limitations_or_known_issues: List[str] = Field(default_factory=list, description="Any trade-offs, constraints or limitations")
    future_improvements: List[str] = Field(default_factory=list, description="Suggested extensions for future phases")


# -------------------------------------------------------------
# Agent 11: Documentation
# -------------------------------------------------------------

class DocumentationResult(BaseModel):
    project_overview: str = Field(description="High-level project description and purpose")
    architecture_explanation: str = Field(description="Explanation of architectural components and patterns")
    setup_instructions: str = Field(description="Step-by-step setup, installation, and run instructions")
    api_documentation: str = Field(description="Documentation of endpoints and payloads")
    agent_workflow_description: str = Field(description="How the multi-agent system designed and validated this project")
    testing_guide: str = Field(description="How to run unit and integration tests")
    known_limitations: str = Field(description="Documented constraints and limitations")
    future_improvements: str = Field(description="Roadmap for future iterations")
    readme_markdown: str = Field(description="Complete, ready-to-use GitHub README.md in Markdown format")


# -------------------------------------------------------------
# API Request / Response Schemas
# -------------------------------------------------------------

class WorkflowRunRequest(BaseModel):
    project_name: Optional[str] = Field(default="", description="Optional project name")
    requirement: str = Field(description="Natural-language software requirement from user")
    tech_preferences: Optional[str] = Field(default="", description="Optional technology or framework preferences")
    provider: Optional[str] = Field(default="", description="Preferred LLM provider: 'openai', 'gemini', or 'mock'")
    use_mock: Optional[bool] = Field(default=False, description="Use deterministic offline mock mode for testing without API key")


class WorkflowLogEntry(BaseModel):
    timestamp: str
    stage: str
    message: str
    level: str = "INFO"


class WorkflowStatusResponse(BaseModel):
    workflow_id: str
    project_name: str
    status: WorkflowStatus
    current_agent: str
    current_step: int
    total_steps: int = 11
    progress_percentage: int
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    error_message: Optional[str] = None
    recent_logs: List[WorkflowLogEntry] = Field(default_factory=list)


class WorkflowFullResponse(BaseModel):
    workflow_id: str
    project_name: str
    requirement: str
    tech_preferences: Optional[str] = ""
    provider: Optional[str] = ""
    status: WorkflowStatus
    current_agent: str
    progress_percentage: int
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    retry_count: int = 0
    error_message: Optional[str] = None
    
    requirements: Optional[RequirementAnalysisResult] = None
    plan: Optional[DevelopmentPlanResult] = None
    architecture: Optional[ArchitectureResult] = None
    senior_review: Optional[SeniorReviewResult] = None
    generated_files: List[GeneratedFile] = Field(default_factory=list)
    test_report: Optional[TestExecutionReport] = None
    debugging_history: List[DebuggingResult] = Field(default_factory=list)
    security_review: Optional[SecurityReviewResult] = None
    optimization: Optional[CodeOptimizationResult] = None
    final_review: Optional[FinalReviewResult] = None
    documentation: Optional[DocumentationResult] = None
    logs: List[WorkflowLogEntry] = Field(default_factory=list)

