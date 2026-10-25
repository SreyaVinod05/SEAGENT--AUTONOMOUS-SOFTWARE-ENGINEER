import io
import zipfile
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from app.config import (
    GEMINI_MODEL,
    OPENAI_MODEL,
    MAX_DEBUG_RETRIES,
    CODE_EXECUTION_TIMEOUT_SECONDS,
    is_gemini_configured,
    is_openai_configured,
    get_default_provider_name,
)
from app.models.schemas import (
    WorkflowStatus,
    WorkflowRunRequest,
    WorkflowStatusResponse,
    WorkflowFullResponse,
    WorkflowLogEntry,
    GeneratedFile,
    TestExecutionReport,
)
from app.services.workflow_storage import workflow_storage
from app.services.workflow_runner import workflow_runner

router = APIRouter(prefix="/api/v1", tags=["Workflows"])


@router.get("/config")
def get_system_config():
    """
    Returns public system configuration without exposing secrets.
    """
    return {
        "gemini_configured": is_gemini_configured(),
        "gemini_model": GEMINI_MODEL,
        "openai_configured": is_openai_configured(),
        "openai_model": OPENAI_MODEL,
        "default_provider": get_default_provider_name(),
        "max_debug_retries": MAX_DEBUG_RETRIES,
        "timeout_seconds": CODE_EXECUTION_TIMEOUT_SECONDS,
        "supported_agents": [
            "RequirementsAgent",
            "PlanningAgent",
            "ArchitectureAgent",
            "SeniorReasoningAgent",
            "CodingAgent",
            "TestingAgent",
            "DebuggingAgent",
            "SecurityReviewAgent",
            "CodeOptimizationAgent",
            "FinalReviewAgent",
            "DocumentationAgent",
        ],
    }


@router.post("/projects")
@router.post("/workflows/run", status_code=status.HTTP_202_ACCEPTED)
def run_workflow(request: WorkflowRunRequest):
    """
    Start a new multi-agent software engineering workflow run.
    """
    if not request.requirement or not request.requirement.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The software requirement cannot be empty.",
        )

    try:
        result = workflow_runner.start_workflow(request)
        return result
    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(val_err),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate workflow: {str(e)}",
        )


@router.get("/workflows")
def list_workflows():
    """
    List all recorded workflow runs (sorted newest first).
    """
    runs = workflow_storage.list_workflows()
    summaries = []
    for r in runs:
        summaries.append({
            "workflow_id": r.get("workflow_id"),
            "project_name": r.get("project_name", "Untitled"),
            "requirement": r.get("user_requirement", "")[:120],
            "provider": r.get("provider", "mock"),
            "status": r.get("status", WorkflowStatus.IDLE.value),
            "progress_percentage": r.get("progress_percentage", 0),
            "current_agent": r.get("current_agent", ""),
            "start_time": r.get("start_time"),
            "end_time": r.get("end_time"),
            "files_count": len(r.get("generated_files") or []),
            "all_tests_passed": bool((r.get("test_report") or {}).get("all_passed", False)),
            "security_score": (r.get("security_review") or {}).get("security_score"),
            "performance_rating": (r.get("optimization") or {}).get("performance_rating"),
        })
    return summaries


@router.get("/workflows/{workflow_id}")
def get_workflow_details(workflow_id: str):
    """
    Get complete workflow state and all agent deliverables.
    """
    data = workflow_storage.get_workflow(workflow_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow '{workflow_id}' not found.",
        )
    return data


@router.get("/workflows/{workflow_id}/status", response_model=WorkflowStatusResponse)
def get_workflow_status(workflow_id: str):
    """
    Get lightweight progress status, current agent, and recent logs.
    """
    data = workflow_storage.get_workflow(workflow_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow '{workflow_id}' not found.",
        )

    logs_raw = data.get("logs", [])
    recent_logs = [WorkflowLogEntry(**log) if isinstance(log, dict) else log for log in logs_raw[-15:]]
    errors = data.get("errors", [])
    err_msg = errors[-1] if errors else None

    return WorkflowStatusResponse(
        workflow_id=workflow_id,
        project_name=data.get("project_name", "Untitled Project"),
        status=data.get("status", WorkflowStatus.IDLE.value),
        current_agent=data.get("current_agent", "WorkflowCoordinatorAgent"),
        current_step=data.get("current_step", 0),
        total_steps=11,
        progress_percentage=data.get("progress_percentage", 0),
        start_time=data.get("start_time"),
        end_time=data.get("end_time"),
        retry_count=data.get("retry_count", 0),
        max_retries=data.get("max_retries", MAX_DEBUG_RETRIES),
        error_message=err_msg,
        recent_logs=recent_logs,
    )


@router.get("/workflows/{workflow_id}/result")
def get_workflow_result(workflow_id: str):
    """
    Get the finalized result when the workflow completes.
    """
    data = workflow_storage.get_workflow(workflow_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow '{workflow_id}' not found.",
        )

    return {
        "workflow_id": workflow_id,
        "project_name": data.get("project_name"),
        "status": data.get("status"),
        "provider": data.get("provider", "mock"),
        "progress_percentage": data.get("progress_percentage"),
        "requirements": data.get("requirements"),
        "plan": data.get("plan"),
        "architecture": data.get("architecture"),
        "senior_review": data.get("senior_review"),
        "generated_files": data.get("generated_files", []),
        "test_report": data.get("test_report"),
        "debugging_history": data.get("debugging_history", []),
        "security_review": data.get("security_review"),
        "optimization": data.get("optimization"),
        "final_review": data.get("final_review"),
        "documentation": data.get("documentation"),
        "start_time": data.get("start_time"),
        "end_time": data.get("end_time"),
    }


@router.get("/workflows/{workflow_id}/files")
def get_workflow_files(workflow_id: str):
    """
    Get the generated source code and test files.
    """
    data = workflow_storage.get_workflow(workflow_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow '{workflow_id}' not found.",
        )

    return {
        "workflow_id": workflow_id,
        "project_name": data.get("project_name"),
        "files": data.get("generated_files", []),
    }


@router.get("/workflows/{workflow_id}/tests")
def get_workflow_tests(workflow_id: str):
    """
    Get detailed test execution report and individual test outcomes.
    """
    data = workflow_storage.get_workflow(workflow_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow '{workflow_id}' not found.",
        )

    return {
        "workflow_id": workflow_id,
        "project_name": data.get("project_name"),
        "test_report": data.get("test_report"),
        "debugging_history": data.get("debugging_history", []),
        "retry_count": data.get("retry_count", 0),
    }


@router.get("/workflows/{workflow_id}/download")
def download_project_zip(workflow_id: str):
    """
    Download all generated source code and tests as a ZIP archive.
    """
    data = workflow_storage.get_workflow(workflow_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow '{workflow_id}' not found.",
        )

    files = data.get("generated_files", [])
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files have been generated yet for this workflow.",
        )

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for f in files:
            path = f.get("path", "file.txt").replace("\\", "/")
            content = f.get("content", "")
            zip_file.writestr(path, content)

    zip_buffer.seek(0)
    project_slug = data.get("project_name", "seagent_project").lower().replace(" ", "_")
    filename = f"{project_slug}_{workflow_id}.zip"

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
