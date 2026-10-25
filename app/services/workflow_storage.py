import json
import logging
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from app.config import DATA_DIR
from app.models.schemas import WorkflowStatus

logger = logging.getLogger("seagent.storage")


class WorkflowStorage:
    """
    Thread-safe storage manager for SEAGENT workflow states and executions.
    Persists runs to local JSON files in DATA_DIR for survival across restarts
    and maintains an in-memory cache for fast status queries.
    """

    def __init__(self, storage_dir: Path = DATA_DIR):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._cache: Dict[str, dict] = {}
        self._load_existing()

    def _load_existing(self):
        """Pre-populate in-memory cache with persisted workflows on startup."""
        try:
            for file_path in self.storage_dir.glob("*.json"):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        wid = data.get("workflow_id")
                        if wid:
                            self._cache[wid] = data
                except Exception as e:
                    logger.warning(f"Failed to load workflow file {file_path}: {e}")
        except Exception as e:
            logger.error(f"Error accessing storage directory {self.storage_dir}: {e}")

    def save_workflow(self, state: dict) -> None:
        """Save or update a workflow state in cache and on disk."""
        wid = state.get("workflow_id")
        if not wid:
            return

        with self._lock:
            # Create a serializable dictionary
            serializable_state = self._serialize_state(state)
            self._cache[wid] = serializable_state

            file_path = self.storage_dir / f"{wid}.json"
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(serializable_state, f, indent=2, default=str)
            except Exception as e:
                logger.error(f"Failed to write workflow {wid} to disk: {e}")

    def get_workflow(self, workflow_id: str) -> Optional[dict]:
        """Retrieve workflow state by ID."""
        with self._lock:
            if workflow_id in self._cache:
                return self._cache[workflow_id]

        file_path = self.storage_dir / f"{workflow_id}.json"
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    with self._lock:
                        self._cache[workflow_id] = data
                    return data
            except Exception as e:
                logger.error(f"Failed to read workflow {workflow_id} from file: {e}")

        return None

    def list_workflows(self) -> List[dict]:
        """List summary of all recorded workflows, sorted newest first."""
        with self._lock:
            runs = list(self._cache.values())

        runs.sort(key=lambda x: x.get("start_time", ""), reverse=True)
        return runs

    def _serialize_state(self, state: Any) -> Any:
        """Recursively convert Pydantic models and Enums to plain JSON-serializable types."""
        if hasattr(state, "model_dump"):
            return state.model_dump()
        if hasattr(state, "value"):
            return state.value
        if isinstance(state, dict):
            return {k: self._serialize_state(v) for k, v in state.items()}
        if isinstance(state, list):
            return [self._serialize_state(item) for item in state]
        return state


# Global singleton instance
workflow_storage = WorkflowStorage()
