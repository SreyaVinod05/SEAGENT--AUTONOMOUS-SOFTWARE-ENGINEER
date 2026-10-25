import logging
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

from langgraph.graph import StateGraph, START, END

from app.config import MAX_DEBUG_RETRIES
from app.models.schemas import (
    WorkflowStatus,
    WorkflowLogEntry,
    GeneratedFile,
    RequirementAnalysisResult,
    DevelopmentPlanResult,
    ArchitectureResult,
    SeniorReviewResult,
    TestExecutionReport,
    DebuggingResult,
    SecurityReviewResult,
    CodeOptimizationResult,
    FinalReviewResult,
    DocumentationResult,
)
from app.workflows.state import WorkflowState
from app.agents import (
    RequirementsAgent,
    PlanningAgent,
    ArchitectureAgent,
    SeniorEngineerAgent,
    SeniorReasoningAgent,
    CodingAgent,
    TestingAgent,
    DebuggingAgent,
    SecurityReviewAgent,
    CodeOptimizationAgent,
    FinalReviewAgent,
    DocumentationAgent,
)
from app.services.workflow_storage import workflow_storage

logger = logging.getLogger("seagent.engine")


def _log(state: WorkflowState, stage: str, message: str, level: str = "INFO"):
    entry = WorkflowLogEntry(
        timestamp=datetime.utcnow().isoformat(),
        stage=stage,
        message=message,
        level=level,
    )
    if "logs" not in state or state["logs"] is None:
        state["logs"] = []
    state["logs"].append(entry)
    logger.info(f"[{stage}] {message}")


# -------------------------------------------------------------
# Graph Node Definitions (11 Specialized Engineering Agents)
# -------------------------------------------------------------

def requirements_node(state: WorkflowState) -> WorkflowState:
    state["status"] = WorkflowStatus.ANALYZING_REQUIREMENTS.value
    state["current_agent"] = "RequirementsAgent"
    state["current_step"] = 1
    state["progress_percentage"] = 10
    _log(state, "RequirementsAgent", "Analyzing natural-language requirement and extracting specifications...")
    workflow_storage.save_workflow(state)

    use_mock = state.get("use_mock", False)
    provider_name = state.get("provider", "")
    agent = RequirementsAgent(use_mock=use_mock, provider_name=provider_name)

    try:
        req_result = agent.analyze(
            user_requirement=state["user_requirement"],
            tech_preferences=state.get("tech_preferences", ""),
        )
        state["requirements"] = req_result
        if not state.get("project_name") or state["project_name"] == "Untitled Project":
            state["project_name"] = req_result.project_name
        _log(state, "RequirementsAgent", f"Requirement analysis completed: {len(req_result.functional_requirements)} functional requirements identified.")
    except Exception as e:
        _log(state, "RequirementsAgent", f"Error in requirement analysis: {e}", level="ERROR")
        if "errors" not in state:
            state["errors"] = []
        state["errors"].append(str(e))
        state["status"] = WorkflowStatus.FAILED.value
        raise

    workflow_storage.save_workflow(state)
    return state


def planning_node(state: WorkflowState) -> WorkflowState:
    state["status"] = WorkflowStatus.PLANNING.value
    state["current_agent"] = "PlanningAgent"
    state["current_step"] = 2
    state["progress_percentage"] = 20
    _log(state, "PlanningAgent", "Formulating structured development plan, milestones, and deliverables...")
    workflow_storage.save_workflow(state)

    use_mock = state.get("use_mock", False)
    provider_name = state.get("provider", "")
    agent = PlanningAgent(use_mock=use_mock, provider_name=provider_name)

    try:
        plan_result = agent.plan(requirements=state["requirements"])
        state["plan"] = plan_result
        _log(state, "PlanningAgent", f"Development plan ready with {len(plan_result.steps)} ordered execution steps.")
    except Exception as e:
        _log(state, "PlanningAgent", f"Error in planning: {e}", level="ERROR")
        if "errors" not in state:
            state["errors"] = []
        state["errors"].append(str(e))
        state["status"] = WorkflowStatus.FAILED.value
        raise

    workflow_storage.save_workflow(state)
    return state


def architecture_node(state: WorkflowState) -> WorkflowState:
    state["status"] = WorkflowStatus.DESIGNING_ARCHITECTURE.value
    state["current_agent"] = "ArchitectureAgent"
    state["current_step"] = 3
    state["progress_percentage"] = 30
    _log(state, "ArchitectureAgent", "Designing system architecture, module boundaries, and API specifications...")
    workflow_storage.save_workflow(state)

    use_mock = state.get("use_mock", False)
    provider_name = state.get("provider", "")
    agent = ArchitectureAgent(use_mock=use_mock, provider_name=provider_name)

    try:
        arch_result = agent.design(
            requirements=state["requirements"],
            plan=state["plan"],
        )
        state["architecture"] = arch_result
        _log(state, "ArchitectureAgent", f"Architecture finalized: {arch_result.architecture_style} with {len(arch_result.api_design)} APIs.")
    except Exception as e:
        _log(state, "ArchitectureAgent", f"Error in architecture: {e}", level="ERROR")
        if "errors" not in state:
            state["errors"] = []
        state["errors"].append(str(e))
        state["status"] = WorkflowStatus.FAILED.value
        raise

    workflow_storage.save_workflow(state)
    return state


def senior_review_node(state: WorkflowState) -> WorkflowState:
    state["status"] = WorkflowStatus.SENIOR_REVIEW.value
    state["current_agent"] = "SeniorReasoningAgent"
    state["current_step"] = 4
    state["progress_percentage"] = 40
    _log(state, "SeniorReasoningAgent", "Conducting Senior Reasoning review of requirements, plan, and architecture...")
    workflow_storage.save_workflow(state)

    use_mock = state.get("use_mock", False)
    provider_name = state.get("provider", "")
    agent = SeniorReasoningAgent(use_mock=use_mock, provider_name=provider_name)

    try:
        review_result = agent.review(
            requirements=state["requirements"],
            plan=state["plan"],
            architecture=state["architecture"],
        )
        state["senior_review"] = review_result
        approval_status = "Approved" if review_result.approved else "Revision Requested"
        _log(state, "SeniorReasoningAgent", f"Senior review: {approval_status} (Score: {review_result.overall_score}/10).")
    except Exception as e:
        _log(state, "SeniorReasoningAgent", f"Error in senior review: {e}", level="ERROR")
        if "errors" not in state:
            state["errors"] = []
        state["errors"].append(str(e))
        state["status"] = WorkflowStatus.FAILED.value
        raise

    workflow_storage.save_workflow(state)
    return state


def route_senior_review(state: WorkflowState) -> str:
    """Conditional routing based on Senior Engineer approval."""
    sr = state.get("senior_review")
    revisions = state.get("senior_review_revisions", 0)

    if sr and sr.approved:
        return "coding_node"

    if revisions < 1:
        state["senior_review_revisions"] = revisions + 1
        _log(state, "SeniorReasoningAgent", "Revising architecture per senior engineering feedback.")
        return "architecture_node"

    _log(state, "SeniorReasoningAgent", "Proceeding to coding with noted recommendations.")
    return "coding_node"


def coding_node(state: WorkflowState) -> WorkflowState:
    state["status"] = WorkflowStatus.GENERATING_CODE.value
    state["current_agent"] = "CodingAgent"
    state["current_step"] = 5
    state["progress_percentage"] = 55
    _log(state, "CodingAgent", "Generating modular source code files and automated test suites...")
    workflow_storage.save_workflow(state)

    use_mock = state.get("use_mock", False)
    provider_name = state.get("provider", "")
    agent = CodingAgent(use_mock=use_mock, provider_name=provider_name)

    try:
        code_result = agent.generate_code(
            requirements=state["requirements"],
            plan=state["plan"],
            architecture=state["architecture"],
            senior_review=state["senior_review"],
        )
        state["generated_files"] = code_result.files
        _log(state, "CodingAgent", f"Generated {len(code_result.files)} files: {', '.join(f.path for f in code_result.files)}.")
    except Exception as e:
        _log(state, "CodingAgent", f"Error in code generation: {e}", level="ERROR")
        if "errors" not in state:
            state["errors"] = []
        state["errors"].append(str(e))
        state["status"] = WorkflowStatus.FAILED.value
        raise

    workflow_storage.save_workflow(state)
    return state


def testing_node(state: WorkflowState) -> WorkflowState:
    retry_count = state.get("retry_count", 0)
    current_status = WorkflowStatus.RETESTING.value if retry_count > 0 else WorkflowStatus.TESTING.value
    state["status"] = current_status
    state["current_agent"] = "TestingAgent"
    state["current_step"] = 6
    state["progress_percentage"] = 68
    _log(state, "TestingAgent", f"Executing test suite in isolated sandbox (Attempt {retry_count + 1})...")
    workflow_storage.save_workflow(state)

    use_mock = state.get("use_mock", False)
    provider_name = state.get("provider", "")
    agent = TestingAgent(use_mock=use_mock, provider_name=provider_name)

    try:
        test_report = agent.run_tests(
            files=state["generated_files"],
            requirements=state.get("requirements"),
            architecture=state.get("architecture"),
        )
        state["test_report"] = test_report
        result_desc = "PASSED" if test_report.all_passed else "FAILED"
        _log(
            state,
            "TestingAgent",
            f"Test execution {result_desc}: {test_report.passed_count}/{test_report.total_tests} passed in {test_report.execution_time_seconds}s.",
        )
    except Exception as e:
        _log(state, "TestingAgent", f"Error during test execution: {e}", level="ERROR")
        if "errors" not in state:
            state["errors"] = []
        state["errors"].append(str(e))

    workflow_storage.save_workflow(state)
    return state


def route_test_result(state: WorkflowState) -> str:
    """Conditional routing: loop to DebuggingAgent if tests fail, or proceed to Security Review."""
    report = state.get("test_report")
    retries = state.get("retry_count", 0)
    max_retries = state.get("max_retries", MAX_DEBUG_RETRIES)

    if report and report.all_passed:
        _log(state, "TestingAgent", "All automated tests verified successfully. Moving to Security Review.")
        return "security_review_node"

    if retries >= max_retries:
        _log(
            state,
            "TestingAgent",
            f"Reached maximum debug retry limit ({max_retries}). Proceeding to Security Review with test outcomes.",
            level="WARNING",
        )
        return "security_review_node"

    _log(state, "TestingAgent", f"Test failures encountered. Dispatching to DebuggingAgent (Retry {retries + 1}/{max_retries}).")
    return "debugging_node"


def debugging_node(state: WorkflowState) -> WorkflowState:
    state["status"] = WorkflowStatus.DEBUGGING.value
    state["current_agent"] = "DebuggingAgent"
    state["current_step"] = 7
    state["progress_percentage"] = 75
    retries = state.get("retry_count", 0)
    state["retry_count"] = retries + 1

    _log(state, "DebuggingAgent", f"Analyzing test failures, root cause, and applying code fixes (Iteration {state['retry_count']})...")
    workflow_storage.save_workflow(state)

    use_mock = state.get("use_mock", False)
    provider_name = state.get("provider", "")
    agent = DebuggingAgent(use_mock=use_mock, provider_name=provider_name)

    try:
        debug_result = agent.debug(
            files=state["generated_files"],
            test_report=state["test_report"],
            requirements=state.get("requirements"),
            architecture=state.get("architecture"),
        )

        if "debugging_history" not in state or state["debugging_history"] is None:
            state["debugging_history"] = []
        state["debugging_history"].append(debug_result)

        # Apply corrected files into state["generated_files"]
        if debug_result.corrected_files:
            file_map = {f.path: f for f in state["generated_files"]}
            for cf in debug_result.corrected_files:
                file_map[cf.path] = cf
            state["generated_files"] = list(file_map.values())
            _log(state, "DebuggingAgent", f"Applied fix to: {', '.join(cf.path for cf in debug_result.corrected_files)}. Re-testing...")
        else:
            _log(state, "DebuggingAgent", "Diagnosis complete. Re-testing...")

    except Exception as e:
        _log(state, "DebuggingAgent", f"Error in debugging agent: {e}", level="ERROR")
        if "errors" not in state:
            state["errors"] = []
        state["errors"].append(str(e))

    workflow_storage.save_workflow(state)
    return state


def security_review_node(state: WorkflowState) -> WorkflowState:
    state["status"] = WorkflowStatus.SECURITY_REVIEW.value
    state["current_agent"] = "SecurityReviewAgent"
    state["current_step"] = 8
    state["progress_percentage"] = 82
    _log(state, "SecurityReviewAgent", "Conducting automated OWASP Top 10 security audit and vulnerability analysis...")
    workflow_storage.save_workflow(state)

    use_mock = state.get("use_mock", False)
    provider_name = state.get("provider", "")
    agent = SecurityReviewAgent(use_mock=use_mock, provider_name=provider_name)

    try:
        security_result = agent.review(
            requirements=state["requirements"],
            architecture=state["architecture"],
            files=state["generated_files"],
            test_report=state.get("test_report"),
        )
        state["security_review"] = security_result
        _log(
            state,
            "SecurityReviewAgent",
            f"Security audit complete: Score {security_result.security_score}/100, Status={security_result.status}, {len(security_result.vulnerabilities)} vulnerabilities flagged."
        )
    except Exception as e:
        _log(state, "SecurityReviewAgent", f"Error in security review: {e}", level="ERROR")
        if "errors" not in state:
            state["errors"] = []
        state["errors"].append(str(e))

    workflow_storage.save_workflow(state)
    return state


def code_optimization_node(state: WorkflowState) -> WorkflowState:
    state["status"] = WorkflowStatus.OPTIMIZING_CODE.value
    state["current_agent"] = "CodeOptimizationAgent"
    state["current_step"] = 9
    state["progress_percentage"] = 88
    _log(state, "CodeOptimizationAgent", "Analyzing Big-O complexity, refactoring bottlenecks, and streamlining algorithms...")
    workflow_storage.save_workflow(state)

    use_mock = state.get("use_mock", False)
    provider_name = state.get("provider", "")
    agent = CodeOptimizationAgent(use_mock=use_mock, provider_name=provider_name)

    try:
        opt_result = agent.optimize(
            requirements=state["requirements"],
            architecture=state["architecture"],
            files=state["generated_files"],
        )
        state["optimization"] = opt_result

        # Update generated_files if optimized implementations provided
        if opt_result.optimized_files:
            file_map = {f.path: f for f in state["generated_files"]}
            for opt_f in opt_result.optimized_files:
                file_map[opt_f.path] = opt_f
            state["generated_files"] = list(file_map.values())
            _log(state, "CodeOptimizationAgent", f"Applied optimized files: {', '.join(opt_f.path for opt_f in opt_result.optimized_files)}.")

        _log(
            state,
            "CodeOptimizationAgent",
            f"Code optimization complete: Rating {opt_result.performance_rating}/100. Speedup: {opt_result.estimated_speedup}."
        )
    except Exception as e:
        _log(state, "CodeOptimizationAgent", f"Error in code optimization: {e}", level="ERROR")
        if "errors" not in state:
            state["errors"] = []
        state["errors"].append(str(e))

    workflow_storage.save_workflow(state)
    return state


def final_review_node(state: WorkflowState) -> WorkflowState:
    state["status"] = WorkflowStatus.FINAL_REVIEW.value
    state["current_agent"] = "FinalReviewAgent"
    state["current_step"] = 10
    state["progress_percentage"] = 94
    _log(state, "FinalReviewAgent", "Conducting comprehensive final quality and requirements coverage audit...")
    workflow_storage.save_workflow(state)

    use_mock = state.get("use_mock", False)
    provider_name = state.get("provider", "")
    agent = FinalReviewAgent(use_mock=use_mock, provider_name=provider_name)

    try:
        final_review = agent.review(
            requirements=state["requirements"],
            architecture=state["architecture"],
            files=state["generated_files"],
            test_report=state.get("test_report"),
        )
        state["final_review"] = final_review
        _log(state, "FinalReviewAgent", f"Final audit complete: Status={final_review.status}, Quality Score={final_review.code_quality_score}/100.")
    except Exception as e:
        _log(state, "FinalReviewAgent", f"Error in final review: {e}", level="ERROR")
        if "errors" not in state:
            state["errors"] = []
        state["errors"].append(str(e))

    workflow_storage.save_workflow(state)
    return state


def documentation_node(state: WorkflowState) -> WorkflowState:
    state["status"] = WorkflowStatus.DOCUMENTATION.value
    state["current_agent"] = "DocumentationAgent"
    state["current_step"] = 11
    state["progress_percentage"] = 100
    _log(state, "DocumentationAgent", "Generating complete technical documentation and project README.md...")
    workflow_storage.save_workflow(state)

    use_mock = state.get("use_mock", False)
    provider_name = state.get("provider", "")
    agent = DocumentationAgent(use_mock=use_mock, provider_name=provider_name)

    try:
        doc_result = agent.document(
            requirements=state["requirements"],
            plan=state["plan"],
            architecture=state["architecture"],
            files=state["generated_files"],
            test_report=state.get("test_report"),
            final_review=state.get("final_review"),
        )
        state["documentation"] = doc_result

        # Append README.md to generated files for easy browsing and download
        readme_file = GeneratedFile(
            path="README.md",
            content=doc_result.readme_markdown,
            description="Autonomous project documentation and setup guide",
        )
        # Avoid duplicate README if one already exists
        state["generated_files"] = [f for f in state["generated_files"] if f.path != "README.md"] + [readme_file]

        state["status"] = WorkflowStatus.COMPLETED.value
        state["progress_percentage"] = 100
        state["end_time"] = datetime.utcnow().isoformat()
        _log(state, "DocumentationAgent", "SEAGENT 11-agent autonomous engineering workflow completed successfully!")

    except Exception as e:
        _log(state, "DocumentationAgent", f"Error in documentation agent: {e}", level="ERROR")
        if "errors" not in state:
            state["errors"] = []
        state["errors"].append(str(e))
        state["status"] = WorkflowStatus.COMPLETED.value
        state["end_time"] = datetime.utcnow().isoformat()

    workflow_storage.save_workflow(state)
    return state


# -------------------------------------------------------------
# LangGraph StateGraph Construction
# -------------------------------------------------------------

def build_seagent_workflow() -> StateGraph:
    """
    Constructs the complete LangGraph StateGraph representing SEAGENT's
    11-agent multi-agent software engineering lifecycle.
    """
    builder = StateGraph(WorkflowState)

    # 1. Add All 11 Agent Nodes
    builder.add_node("requirements_node", requirements_node)
    builder.add_node("planning_node", planning_node)
    builder.add_node("architecture_node", architecture_node)
    builder.add_node("senior_review_node", senior_review_node)
    builder.add_node("coding_node", coding_node)
    builder.add_node("testing_node", testing_node)
    builder.add_node("debugging_node", debugging_node)
    builder.add_node("security_review_node", security_review_node)
    builder.add_node("code_optimization_node", code_optimization_node)
    builder.add_node("final_review_node", final_review_node)
    builder.add_node("documentation_node", documentation_node)

    # 2. Add Requirements -> Planning -> Architecture -> Senior Review
    builder.add_edge(START, "requirements_node")
    builder.add_edge("requirements_node", "planning_node")
    builder.add_edge("planning_node", "architecture_node")
    builder.add_edge("architecture_node", "senior_review_node")

    # 3. Add Senior Review Conditional Edge (Approved -> Coding, Rejected -> Architecture revision)
    builder.add_conditional_edges(
        "senior_review_node",
        route_senior_review,
        {
            "coding_node": "coding_node",
            "architecture_node": "architecture_node",
        },
    )

    # 4. Coding to Testing
    builder.add_edge("coding_node", "testing_node")

    # 5. Add Testing Conditional Edge (Pass -> Security Review, Fail -> Debugging)
    builder.add_conditional_edges(
        "testing_node",
        route_test_result,
        {
            "security_review_node": "security_review_node",
            "debugging_node": "debugging_node",
        },
    )

    # 6. Debugging loops back to Testing
    builder.add_edge("debugging_node", "testing_node")

    # 7. Security Review -> Code Optimization -> Final Review -> Documentation -> END
    builder.add_edge("security_review_node", "code_optimization_node")
    builder.add_edge("code_optimization_node", "final_review_node")
    builder.add_edge("final_review_node", "documentation_node")
    builder.add_edge("documentation_node", END)

    return builder.compile()


# Global compiled workflow graph instance
seagent_graph = build_seagent_workflow()
