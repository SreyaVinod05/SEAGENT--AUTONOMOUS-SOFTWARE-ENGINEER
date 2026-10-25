import logging
import threading
import uuid
from datetime import datetime
from typing import Optional, Dict, Any

from app.config import (
    MAX_DEBUG_RETRIES,
    is_gemini_configured,
    is_openai_configured,
    get_default_provider_name,
)
from app.models.schemas import WorkflowStatus, WorkflowRunRequest
from app.workflows.state import WorkflowState
from app.workflows.engine import seagent_graph
from app.services.workflow_storage import workflow_storage

logger = logging.getLogger("seagent.runner")


class WorkflowRunner:
    """
    Asynchronous executor for SEAGENT LangGraph workflows.
    Runs workflows in background worker threads, manages state transitions,
    and updates persistent storage.
    """

    def __init__(self):
        self._active_threads: Dict[str, threading.Thread] = {}

    def start_workflow(self, request: WorkflowRunRequest) -> Dict[str, Any]:
        """
        Validates request and spawns a background workflow thread.
        """
        requirement_clean = request.requirement.strip()
        if not requirement_clean:
            raise ValueError("Requirement cannot be empty.")

        # Resolve provider
        requested_provider = (request.provider or "").strip().lower()
        if request.use_mock:
            resolved_provider = "mock"
        elif requested_provider in ("openai", "gemini", "mock"):
            resolved_provider = requested_provider
        else:
            resolved_provider = get_default_provider_name()

        # Validate that chosen provider has credentials
        if resolved_provider == "gemini" and not is_gemini_configured():
            if is_openai_configured():
                resolved_provider = "openai"
                logger.info("Falling back to configured OpenAI provider since GEMINI_API_KEY is not set.")
            else:
                raise ValueError(
                    "GEMINI_API_KEY is not configured in backend/.env. "
                    "Please configure your Google Gemini API key, configure OpenAI, or enable 'Test Mode'."
                )
        elif resolved_provider == "openai" and not is_openai_configured():
            if is_gemini_configured():
                resolved_provider = "gemini"
                logger.info("Falling back to configured Gemini provider since OPENAI_API_KEY is not set.")
            else:
                raise ValueError(
                    "OPENAI_API_KEY is not configured in backend/.env. "
                    "Please configure your OpenAI API key, configure Gemini, or enable 'Test Mode'."
                )

        workflow_id = f"wf-{uuid.uuid4().hex[:8]}"
        project_name = (request.project_name or "Untitled Project").strip()

        initial_state: WorkflowState = {
            "workflow_id": workflow_id,
            "project_name": project_name,
            "user_requirement": requirement_clean,
            "tech_preferences": (request.tech_preferences or "").strip(),
            "provider": resolved_provider,
            "use_mock": resolved_provider == "mock" or bool(request.use_mock),
            "status": WorkflowStatus.IDLE.value,
            "current_agent": "WorkflowCoordinatorAgent",
            "current_step": 0,
            "progress_percentage": 0,
            "requirements": None,
            "plan": None,
            "architecture": None,
            "senior_review": None,
            "senior_review_revisions": 0,
            "generated_files": [],
            "test_report": None,
            "debugging_history": [],
            "retry_count": 0,
            "max_retries": MAX_DEBUG_RETRIES,
            "security_review": None,
            "optimization": None,
            "final_review": None,
            "documentation": None,
            "errors": [],
            "logs": [],
            "start_time": datetime.utcnow().isoformat(),
            "end_time": None,
        }

        # Persist initial state
        workflow_storage.save_workflow(initial_state)

        # Spawn background worker thread
        thread = threading.Thread(
            target=self._run_workflow_worker,
            args=(workflow_id, initial_state),
            daemon=True,
        )
        self._active_threads[workflow_id] = thread
        thread.start()

        logger.info(f"Started background workflow {workflow_id} with provider '{resolved_provider}' for requirement: '{requirement_clean[:60]}...'")
        return {
            "workflow_id": workflow_id,
            "project_name": project_name,
            "provider": resolved_provider,
            "status": WorkflowStatus.IDLE.value,
            "message": f"Workflow started successfully using {resolved_provider} provider.",
        }

    def _run_workflow_worker(self, workflow_id: str, state: WorkflowState) -> None:
        """Worker thread entrypoint executing the compiled LangGraph workflow."""
        try:
            logger.info(f"Executing LangGraph for workflow {workflow_id}")
            final_state = seagent_graph.invoke(state)
            workflow_storage.save_workflow(final_state)
            logger.info(f"Completed LangGraph execution for workflow {workflow_id}")
        except Exception as e:
            logger.error(f"Fatal error in workflow {workflow_id}: {e}", exc_info=True)
            existing = workflow_storage.get_workflow(workflow_id) or state
            existing["status"] = WorkflowStatus.FAILED.value
            existing["current_agent"] = "WorkflowCoordinatorAgent"
            existing["end_time"] = datetime.utcnow().isoformat()
            if "errors" not in existing or existing["errors"] is None:
                existing["errors"] = []
            existing["errors"].append(str(e))
            workflow_storage.save_workflow(existing)
        finally:
            self._active_threads.pop(workflow_id, None)


# Global singleton runner
workflow_runner = WorkflowRunner()
