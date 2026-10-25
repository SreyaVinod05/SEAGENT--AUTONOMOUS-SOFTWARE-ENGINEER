"""
Explicit Mock Provider for SEAGENT test and dry-run mode.
Used only when explicitly enabled (e.g., during offline testing, unit test suites,
or when testing without API credits).
Provides realistic, syntactically valid code and tests to verify the entire
multi-agent pipeline, safe execution engine, and UI visualization.
Dynamically tailors generated deliverables based on the requirement context (e.g. Period Tracker, Task Management).
"""

from typing import Type, TypeVar, Optional
from pydantic import BaseModel

from app.models.schemas import (
    RequirementAnalysisResult,
    DevelopmentPlanResult,
    DevelopmentStep,
    ArchitectureResult,
    APIEndpoint,
    ModuleDesign,
    SeniorReviewResult,
    GeneratedFile,
    CodeGenerationResult,
    DebuggingResult,
    SecurityReviewResult,
    SecurityVulnerability,
    CodeOptimizationResult,
    OptimizedFileDetail,
    FinalReviewResult,
    DocumentationResult,
)

T = TypeVar("T", bound=BaseModel)


class MockGeminiProvider:
    """
    Explicit test/mock provider for validating agent schemas and execution pipelines.
    Supports dynamic context detection (Period Tracker, Task Manager, etc.) to ensure
    realistic deliverables for viva evaluations even when offline.
    """

    def __init__(self):
        self.call_count = 0

    def generate_structured(
        self,
        prompt: str,
        schema: Type[T],
        system_instruction: Optional[str] = None,
        temperature: float = 0.2,
    ) -> T:
        self.call_count += 1
        prompt_lower = prompt.lower()
        is_period = any(k in prompt_lower for k in ["period", "cycle", "tracker", "fertility", "ovulation", "women", "menstrual"])

        # -------------------------------------------------------------
        # 1. Requirement Analysis
        # -------------------------------------------------------------
        if schema == RequirementAnalysisResult:
            if is_period:
                return RequirementAnalysisResult(
                    project_name="CycleFlow - Period & Fertility Tracker",
                    summary="A clean, privacy-first menstrual cycle and fertility tracking application for women. Calculates cycle days, forecasts next period dates, and estimates fertile windows.",
                    functional_requirements=[
                        "Record and save the first day of menstrual cycle",
                        "Configure average cycle length (default 28 days, range 20-45 days)",
                        "Configure average period length (default 5 days, range 2-10 days)",
                        "Calculate and display the next expected period date",
                        "Compute the current cycle day relative to the latest period start date",
                        "Estimate the fertile window and approximate ovulation date",
                        "View historical period records and cycle duration metrics",
                    ],
                    non_functional_requirements=[
                        "Privacy-First: Zero external tracking or third-party telemetry of sensitive health data",
                        "Performance: Instant mathematical calculations (<10ms)",
                        "Clean modular service layer with 100% unit test coverage",
                        "Explicit Medical Disclaimer: Cycles vary; tool is purely informational and not a contraceptive device",
                    ],
                    assumptions=[
                        "User tracks regular or moderately regular menstrual cycles",
                        "Calculations utilize standard clinical cycle arithmetic (14-day luteal phase assumption)",
                    ],
                    constraints=[
                        "No external database required; run with pure standard library Python",
                        "Must include explicit medical disclaimer across interfaces",
                    ],
                    actors=["User (Primary)", "Healthcare Provider (Observer)"],
                    use_cases=[
                        "User logs the start date of a new period",
                        "User checks current cycle day and predicted next period date",
                        "User checks estimated fertile window and ovulation day",
                        "User reviews historical cycle logs",
                    ],
                    acceptance_criteria=[
                        "Period start dates must be valid calendar dates",
                        "Cycle length must be validated between 20 and 45 days",
                        "Period duration must be validated between 2 and 10 days",
                        "Next period date equals start_date + cycle_length days",
                        "Ovulation date equals next_period_date - 14 days",
                        "All unit tests pass with zero assertion errors",
                    ],
                )
            else:
                return RequirementAnalysisResult(
                    project_name="TaskMaster Pro",
                    summary="A robust task management application enabling users to create, view, update, delete, and mark tasks as completed.",
                    functional_requirements=[
                        "Create new tasks with title, description, priority, and status",
                        "List all tasks with filtering by priority and completion state",
                        "Update task details and mark status as completed",
                        "Delete tasks safely by identifier",
                    ],
                    non_functional_requirements=[
                        "Fast response times (< 100ms for in-memory operations)",
                        "Data validation for all input fields",
                        "Clean RESTful API conventions",
                    ],
                    assumptions=[
                        "Single user or lightweight team environment",
                        "Storage is persistent or memory-backed with export capabilities",
                    ],
                    constraints=[
                        "Must run locally on standard Python without heavy external database setup",
                        "Pure Python standard library testable suite",
                    ],
                    actors=["Task Owner", "Team Member", "System Administrator"],
                    use_cases=[
                        "User creates a new high-priority task",
                        "User marks an existing task as completed",
                        "User filters tasks by completion status",
                        "User deletes a completed task",
                    ],
                    acceptance_criteria=[
                        "Tasks cannot be created with an empty title",
                        "Priority defaults to 'Medium' if unspecified, supports 'Low', 'Medium', 'High'",
                        "Completion status toggles cleanly between True and False",
                        "All unit tests pass with zero errors",
                    ],
                )

        # -------------------------------------------------------------
        # 2. Development Planning
        # -------------------------------------------------------------
        elif schema == DevelopmentPlanResult:
            if is_period:
                return DevelopmentPlanResult(
                    project_objective="Deliver an autonomous, tested cycle tracking engine with domain models, fertility forecasting, and automated test suite.",
                    steps=[
                        DevelopmentStep(
                            step_number=1,
                            title="Domain Model & Cycle Validation",
                            description="Define CycleLog, CyclePrediction dataclasses, and boundary validation for cycle length.",
                            deliverable="cycle_model.py",
                            dependencies=[],
                            priority="High",
                        ),
                        DevelopmentStep(
                            step_number=2,
                            title="Cycle Tracking & Forecasting Service",
                            description="Implement period logging, next period date projection, current cycle day calculation, and ovulation window estimation.",
                            deliverable="cycle_service.py",
                            dependencies=["Domain Model & Cycle Validation"],
                            priority="High",
                        ),
                        DevelopmentStep(
                            step_number=3,
                            title="Automated Test Suite",
                            description="Create rigorous unit tests covering cycle predictions, default 28-day calculations, ovulation estimates, and input validations.",
                            deliverable="test_cycle_tracker.py",
                            dependencies=["Cycle Tracking & Forecasting Service"],
                            priority="High",
                        ),
                    ],
                    milestones=[
                        "M1: Domain Models & Date Validation Complete",
                        "M2: Cycle Forecasting Algorithms Implemented",
                        "M3: Unit Tests Verified & Passing",
                    ],
                    deliverables=[
                        "Cycle domain models with date validation",
                        "Forecasting service with fertility estimation",
                        "Automated test suite",
                    ],
                    dependencies=["Python 3.10+", "datetime", "unittest"],
                    implementation_priorities=["Accuracy of date arithmetic", "Input boundary validation", "Privacy-first design"],
                )
            else:
                return DevelopmentPlanResult(
                    project_objective="Deliver a complete, tested task management core engine with domain models, service operations, and unit test suite.",
                    steps=[
                        DevelopmentStep(
                            step_number=1,
                            title="Domain Model & Enums",
                            description="Define Task schema, TaskPriority enum, and validation rules.",
                            deliverable="models/task.py",
                            dependencies=[],
                            priority="High",
                        ),
                        DevelopmentStep(
                            step_number=2,
                            title="Task Repository & Service",
                            description="Implement CRUD operations, search, and state transitions.",
                            deliverable="services/task_service.py",
                            dependencies=["Domain Model & Enums"],
                            priority="High",
                        ),
                        DevelopmentStep(
                            step_number=3,
                            title="Automated Test Suite",
                            description="Create comprehensive unittest test cases for CRUD, edge cases, and validation.",
                            deliverable="tests/test_tasks.py",
                            dependencies=["Task Repository & Service"],
                            priority="High",
                        ),
                    ],
                    milestones=[
                        "M1: Core Domain Models Verified",
                        "M2: Business Logic & CRUD Implemented",
                        "M3: Unit Tests Verified & Passed",
                    ],
                    deliverables=[
                        "Core domain models with validation",
                        "Service layer handling task management lifecycle",
                        "Automated unit test suite",
                    ],
                    dependencies=["Python 3.10+", "unittest"],
                    implementation_priorities=["Validation robustness", "Modular separation", "Test coverage"],
                )

        # -------------------------------------------------------------
        # 3. Architecture Decision
        # -------------------------------------------------------------
        elif schema == ArchitectureResult:
            if is_period:
                return ArchitectureResult(
                    architecture_style="Modular Clean Architecture (Domain Models -> Forecasting Service -> API/Client)",
                    frontend_architecture="Minimal, feminine-themed responsive interface with monthly calendar visualizer and cycle day ring indicator",
                    backend_architecture="Python modular service architecture with strict date arithmetic encapsulation",
                    database_storage="Thread-safe memory repository with JSON export capabilities and local storage caching",
                    api_design=[
                        APIEndpoint(
                            method="POST",
                            path="/api/cycles/log",
                            description="Log the start date of a new period",
                            request_body="CycleLogCreate(start_date, cycle_length, period_length, notes)",
                            response="CycleLog entry with unique ID",
                        ),
                        APIEndpoint(
                            method="GET",
                            path="/api/cycles/prediction",
                            description="Get next period forecast, current cycle day, and fertile window",
                            request_body=None,
                            response="CyclePrediction object with dates and medical disclaimer",
                        ),
                        APIEndpoint(
                            method="GET",
                            path="/api/cycles/history",
                            description="Retrieve past period records sorted chronologically",
                            request_body=None,
                            response="List of CycleLog objects",
                        ),
                    ],
                    major_modules=[
                        ModuleDesign(name="cycle_model", responsibility="Domain entities and cycle length boundary validation"),
                        ModuleDesign(name="cycle_service", responsibility="Cycle forecasting, ovulation calculation, and history management"),
                        ModuleDesign(name="test_cycle_tracker", responsibility="Automated unit testing suite for all cycle projections"),
                    ],
                    component_responsibilities=[
                        "cycle_model.py: Validates start dates and enforces standard cycle duration ranges",
                        "cycle_service.py: Performs calendar arithmetic for next period, ovulation, and fertile window",
                        "test_cycle_tracker.py: Asserts mathematical correctness across edge cases and leap years",
                    ],
                    data_flow=[
                        "1. User submits period start date and cycle length",
                        "2. Model validates input boundaries (20 <= cycle_length <= 45)",
                        "3. Service records log and updates predictions",
                        "4. Service computes next period date (start_date + cycle_length) and ovulation (next_period - 14 days)",
                        "5. Predictions returned with medical disclaimer",
                    ],
                    security_considerations=[
                        "Strict data privacy: no third-party tracking of intimate health data",
                        "Local-only storage support for complete user confidentiality",
                        "Input bounds validation preventing invalid calendar operations",
                    ],
                    scalability_considerations=[
                        "Stateless date calculation logic scales to millions of concurrent calculations with zero database overhead",
                    ],
                    architectural_decisions_rationale="Opted for pure standard-library date arithmetic to guarantee zero-dependency execution and 100% privacy.",
                )
            else:
                return ArchitectureResult(
                    architecture_style="Modular Layered Architecture (Domain Model -> Service Layer -> API/CLI)",
                    frontend_architecture="React SPA with componentized task board and status filter tabs",
                    backend_architecture="Python modular service architecture with clean separation of concerns",
                    database_storage="In-memory repository with thread-safe dictionary storage and JSON export",
                    api_design=[
                        APIEndpoint(
                            method="GET",
                            path="/api/tasks",
                            description="Retrieve all tasks, optionally filtered by status",
                            request_body=None,
                            response="List of Task objects",
                        ),
                        APIEndpoint(
                            method="POST",
                            path="/api/tasks",
                            description="Create a new task",
                            request_body="TaskCreate(title, description, priority)",
                            response="Task object with generated id and timestamps",
                        ),
                    ],
                    major_modules=[
                        ModuleDesign(name="task_model", responsibility="Entity definition and field validation"),
                        ModuleDesign(name="task_service", responsibility="In-memory task store and operations"),
                        ModuleDesign(name="test_tasks", responsibility="Unit test suite"),
                    ],
                    component_responsibilities=["task_model.py: Task entity", "task_service.py: CRUD operations", "test_tasks.py: Test suite"],
                    data_flow=["1. Client submits Task payload", "2. Model validates fields", "3. Service stores task", "4. Queries retrieve filtered results"],
                    security_considerations=["Strict input validation to avoid injection", "Safe error handling without exposing internal stack traces"],
                    scalability_considerations=["In-memory design can be easily swapped for SQLite or PostgreSQL repository pattern"],
                    architectural_decisions_rationale="Opted for a clean Layered Repository pattern: lightweight, fully testable without external services.",
                )

        # -------------------------------------------------------------
        # 4. Senior Reasoning Review
        # -------------------------------------------------------------
        elif schema == SeniorReviewResult:
            return SeniorReviewResult(
                approved=True,
                overall_score=9,
                strengths=[
                    "Clean separation of concerns between domain entities, service layer, and tests",
                    "Zero external database dependency for instant testability",
                    "Explicit medical disclaimer included in prediction contract",
                    "Robust boundary checks on cycle duration and date validity",
                ],
                issues=[],
                recommendations=[
                    "Ensure calculations handle leap years and month transitions cleanly using datetime.timedelta",
                    "Keep medical disclaimer prominent on all prediction responses",
                ],
                revision_target="none",
            )

        # -------------------------------------------------------------
        # 5. Code Generation
        # -------------------------------------------------------------
        elif schema == CodeGenerationResult:
            if is_period:
                model_code = '''"""
Domain models for Period and Menstrual Cycle Tracking.
"""
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional


@dataclass
class CycleLog:
    id: int
    start_date: date
    cycle_length: int = 28
    period_length: int = 5
    notes: str = ""

    def __post_init__(self):
        if not isinstance(self.start_date, date):
            raise ValueError("start_date must be a valid datetime.date object.")
        if self.cycle_length < 20 or self.cycle_length > 45:
            raise ValueError("cycle_length must be between 20 and 45 days.")
        if self.period_length < 2 or self.period_length > 10:
            raise ValueError("period_length must be between 2 and 10 days.")


@dataclass
class CyclePrediction:
    next_period_date: date
    current_cycle_day: int
    ovulation_date: date
    fertile_window_start: date
    fertile_window_end: date
    disclaimer: str = (
        "Important: Predictions are estimates based on standard clinical cycle averages. "
        "Cycles can vary due to stress, hormonal changes, and lifestyle. This is an informational "
        "tool and not a medical or contraceptive device."
    )
'''
                service_code = '''"""
Cycle Tracking Service providing period forecasting, current cycle day calculations,
and estimated fertility window tracking.
"""
from datetime import date, timedelta
from typing import List, Optional
from cycle_model import CycleLog, CyclePrediction


class CycleTrackerService:
    """
    Manages menstrual cycle history and forecasts future cycle milestones.
    """

    def __init__(self):
        self._logs: List[CycleLog] = []
        self._next_id: int = 1

    def log_period(
        self,
        start_date: date,
        cycle_length: int = 28,
        period_length: int = 5,
        notes: str = "",
    ) -> CycleLog:
        """Record the start of a period with customizable cycle and period durations."""
        entry = CycleLog(
            id=self._next_id,
            start_date=start_date,
            cycle_length=cycle_length,
            period_length=period_length,
            notes=notes,
        )
        self._logs.append(entry)
        self._next_id += 1
        return entry

    def get_latest_log(self) -> Optional[CycleLog]:
        """Retrieve the most recent period record."""
        if not self._logs:
            return None
        return sorted(self._logs, key=lambda x: x.start_date, reverse=True)[0]

    def get_all_logs(self) -> List[CycleLog]:
        """Retrieve all cycle logs sorted newest first."""
        return sorted(self._logs, key=lambda x: x.start_date, reverse=True)

    def predict_cycle(self, as_of_date: Optional[date] = None) -> Optional[CyclePrediction]:
        """
        Calculates next expected period date, current cycle day,
        and estimated fertile window based on the latest logged cycle.
        """
        latest = self.get_latest_log()
        if not latest:
            return None

        today = as_of_date or date.today()

        # Forecast next period date: start_date + cycle_length
        next_period = latest.start_date + timedelta(days=latest.cycle_length)

        # Ovulation is typically ~14 days before the next period starts
        ovulation = next_period - timedelta(days=14)

        # Fertile window is approximately 5 days before ovulation through 1 day after
        fertile_start = ovulation - timedelta(days=5)
        fertile_end = ovulation + timedelta(days=1)

        # Calculate current cycle day (1-indexed)
        days_diff = (today - latest.start_date).days
        if days_diff >= 0:
            cycle_day = (days_diff % latest.cycle_length) + 1
        else:
            cycle_day = 1

        return CyclePrediction(
            next_period_date=next_period,
            current_cycle_day=cycle_day,
            ovulation_date=ovulation,
            fertile_window_start=fertile_start,
            fertile_window_end=fertile_end,
        )
'''
                test_code = '''"""
Rigorous automated unit test suite for CycleTrackerService.
"""
import unittest
from datetime import date, timedelta
from cycle_model import CycleLog, CyclePrediction
from cycle_service import CycleTrackerService


class TestCycleTracker(unittest.TestCase):
    def setUp(self):
        self.service = CycleTrackerService()

    def test_log_period_valid(self):
        log = self.service.log_period(date(2026, 10, 1), cycle_length=28, period_length=5)
        self.assertEqual(log.id, 1)
        self.assertEqual(log.start_date, date(2026, 10, 1))
        self.assertEqual(log.cycle_length, 28)
        self.assertEqual(log.period_length, 5)
        self.assertEqual(len(self.service.get_all_logs()), 1)

    def test_predict_next_period_and_ovulation(self):
        self.service.log_period(date(2026, 10, 1), cycle_length=28)
        pred = self.service.predict_cycle(as_of_date=date(2026, 10, 10))
        self.assertIsNotNone(pred)
        # 2026-10-01 + 28 days = 2026-10-29
        self.assertEqual(pred.next_period_date, date(2026, 10, 29))
        # 2026-10-29 - 14 days = 2026-10-15
        self.assertEqual(pred.ovulation_date, date(2026, 10, 15))
        # Fertile window: 2026-10-10 to 2026-10-16
        self.assertEqual(pred.fertile_window_start, date(2026, 10, 10))
        self.assertEqual(pred.fertile_window_end, date(2026, 10, 16))
        self.assertIn("not a medical or contraceptive device", pred.disclaimer)

    def test_current_cycle_day(self):
        self.service.log_period(date(2026, 10, 1), cycle_length=28)
        pred = self.service.predict_cycle(as_of_date=date(2026, 10, 6))
        self.assertEqual(pred.current_cycle_day, 6)

    def test_invalid_cycle_length_raises(self):
        with self.assertRaises(ValueError):
            self.service.log_period(date(2026, 10, 1), cycle_length=15)
        with self.assertRaises(ValueError):
            self.service.log_period(date(2026, 10, 1), cycle_length=50)

    def test_invalid_period_length_raises(self):
        with self.assertRaises(ValueError):
            self.service.log_period(date(2026, 10, 1), period_length=1)
        with self.assertRaises(ValueError):
            self.service.log_period(date(2026, 10, 1), period_length=15)

    def test_history_ordering(self):
        self.service.log_period(date(2026, 8, 1))
        self.service.log_period(date(2026, 9, 1))
        self.service.log_period(date(2026, 10, 1))
        logs = self.service.get_all_logs()
        self.assertEqual(logs[0].start_date, date(2026, 10, 1))
        self.assertEqual(logs[-1].start_date, date(2026, 8, 1))


if __name__ == '__main__':
    unittest.main()
'''
                return CodeGenerationResult(
                    project_summary="CycleFlow period tracking engine generated with domain dataclasses, prediction algorithms, and test suite.",
                    files=[
                        GeneratedFile(path="cycle_model.py", content=model_code, description="Domain models for cycle logs and predictions"),
                        GeneratedFile(path="cycle_service.py", content=service_code, description="Cycle forecasting and fertility window algorithms"),
                        GeneratedFile(path="test_cycle_tracker.py", content=test_code, description="Automated unit test suite verifying cycle calculations"),
                    ],
                )
            else:
                task_model_code = '''"""
Domain models and enums for Task Management.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    priority: TaskPriority = TaskPriority.MEDIUM
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty.")
        if isinstance(self.priority, str):
            try:
                self.priority = TaskPriority(self.priority)
            except ValueError:
                self.priority = TaskPriority.MEDIUM
'''
                task_service_code = '''"""
Task Service layer managing task operations.
"""
from typing import List, Optional
from task_model import Task, TaskPriority


class TaskService:
    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def create_task(self, title: str, description: str = "", priority: str = "Medium") -> Task:
        task = Task(id=self._next_id, title=title, description=description, priority=priority)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def list_tasks(self, completed: Optional[bool] = None, priority: Optional[str] = None) -> List[Task]:
        results = self._tasks
        if completed is not None:
            results = [t for t in results if t.completed == completed]
        if priority is not None:
            results = [t for t in results if t.priority == priority or t.priority.value == priority]
        return results

    def complete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task:
            task.completed = True
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        initial_len = len(self._tasks)
        self._tasks = [t for t in self._tasks if t.id != task_id]
        return len(self._tasks) < initial_len
'''
                test_tasks_code = '''"""
Automated unit test suite for TaskService and Task models.
"""
import unittest
from task_model import Task, TaskPriority
from task_service import TaskService


class TestTaskService(unittest.TestCase):
    def setUp(self):
        self.service = TaskService()

    def test_create_task_valid(self):
        task = self.service.create_task("Write thesis proposal", priority="High")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Write thesis proposal")
        self.assertEqual(task.priority, TaskPriority.HIGH)
        self.assertFalse(task.completed)

    def test_empty_title_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.service.create_task("   ")

    def test_complete_task(self):
        task = self.service.create_task("Implement testing agent")
        self.assertFalse(task.completed)
        success = self.service.complete_task(task.id)
        self.assertTrue(success)
        self.assertTrue(task.completed)

    def test_delete_task(self):
        task = self.service.create_task("Temporary debug task")
        self.assertTrue(self.service.delete_task(task.id))
        self.assertIsNone(self.service.get_task(task.id))

    def test_filter_by_completed(self):
        t1 = self.service.create_task("Task 1")
        t2 = self.service.create_task("Task 2")
        self.service.complete_task(t1.id)
        completed = self.service.list_tasks(completed=True)
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0].id, t1.id)

    def test_invalid_priority_falls_back_to_medium(self):
        task = self.service.create_task("Task with unknown priority", priority="SuperUrgent")
        self.assertEqual(task.priority, TaskPriority.MEDIUM)


if __name__ == '__main__':
    unittest.main()
'''
                return CodeGenerationResult(
                    project_summary="Modular task management platform with domain model, service layer, and comprehensive unit tests.",
                    files=[
                        GeneratedFile(path="task_model.py", content=task_model_code, description="Domain models and priority enums"),
                        GeneratedFile(path="task_service.py", content=task_service_code, description="Business logic service managing task mutations and filtering"),
                        GeneratedFile(path="test_tasks.py", content=test_tasks_code, description="Automated unit test suite exercising full task lifecycle"),
                    ],
                )

        # -------------------------------------------------------------
        # 6. Debugging Agent (Fallback)
        # -------------------------------------------------------------
        elif schema == DebuggingResult:
            return DebuggingResult(
                root_cause="None. All unit tests executed cleanly in sandboxed environment.",
                affected_files=[],
                proposed_fix="No patches required.",
                corrected_files=[],
            )

        # -------------------------------------------------------------
        # 7. Security Review Agent
        # -------------------------------------------------------------
        elif schema == SecurityReviewResult:
            return SecurityReviewResult(
                security_score=97 if is_period else 96,
                status="PASSED",
                vulnerabilities=[],
                owasp_compliance=[
                    "A01:2021-Broken Access Control: COMPLIANT (Isolated memory space)",
                    "A02:2021-Cryptographic Failures: COMPLIANT (No hardcoded secrets or keys)",
                    "A03:2021-Injection: COMPLIANT (Safe in-memory date arithmetic, no unsafe eval/exec)",
                    "A04:2021-Insecure Design: COMPLIANT (Layered architecture with boundary validation)",
                    "A05:2021-Security Misconfiguration: COMPLIANT (Explicit defaults used)",
                    "A08:2021-Software and Data Integrity: COMPLIANT (Standard library only)",
                ],
                secure_design_patterns=[
                    "Strict type validation via Python dataclasses",
                    "Privacy-preserving in-memory operations with zero data leakage",
                    "Clean exception hierarchies without internal tracebacks exposed",
                ],
                remediation_steps=[
                    "Keep health data encrypted at rest if storing in persistent media",
                    "Ensure medical disclaimer remains visible across all UI views",
                ],
                summary="Application security analysis passed with high rating. No vulnerabilities identified.",
            )

        # -------------------------------------------------------------
        # 8. Code Optimization Agent
        # -------------------------------------------------------------
        elif schema == CodeOptimizationResult:
            return CodeOptimizationResult(
                overall_improvement_summary="Optimized date calculation algorithms and history lookups with O(1) mathematical projections.",
                performance_rating=95,
                estimated_speedup="Instant sub-millisecond execution (<5ms)",
                file_optimizations=[
                    OptimizedFileDetail(
                        path="cycle_service.py" if is_period else "task_service.py",
                        optimization_type="O(1) Date Projections & Generator Comprehensions",
                        time_complexity_before="O(N)",
                        time_complexity_after="O(1)",
                        space_complexity_before="O(1)",
                        space_complexity_after="O(1)",
                        changes_made="Applied direct timedelta mathematical projection avoiding iterative loops.",
                    )
                ],
                optimized_files=[],
                best_practices_applied=[
                    "O(1) calendar arithmetic via datetime.timedelta",
                    "Immutable dataclass properties for prediction responses",
                    "Clean boundary validation during initialization",
                ],
            )

        # -------------------------------------------------------------
        # 9. Final Review Agent
        # -------------------------------------------------------------
        elif schema == FinalReviewResult:
            return FinalReviewResult(
                status="SUCCESS",
                requirements_coverage_score=98,
                code_quality_score=95,
                test_coverage_summary="100% test coverage over cycle models, prediction calculations, and boundary validation.",
                security_assessment="Privacy-first architecture with zero third-party telemetry or credentials.",
                maintainability_assessment="High maintainability: cleanly divided into domain entities, service layer, and test suites.",
                strengths=[
                    "Complete implementation of all specified requirements",
                    "100% automated test suite passing in sandbox",
                    "Comprehensive medical disclaimer protecting users and compliance",
                ],
                limitations_or_known_issues=[],
                future_improvements=[
                    "Add symptoms and mood tracking notes",
                    "Add export to PDF or CSV",
                ],
            )

        # -------------------------------------------------------------
        # 10. Documentation Agent
        # -------------------------------------------------------------
        elif schema == DocumentationResult:
            title = "CycleFlow - Period & Fertility Tracker" if is_period else "TaskMaster Pro"
            readme_text = f"""# {title} - Multi-Agent Engineered Application

Created autonomously by **SEAGENT** (Multi-Agent Agentic AI Software Engineering Framework).

## Overview
{title} is a lightweight, reliable, privacy-first software system designed to carry out the complete software development lifecycle autonomously.

## Architecture
- **Domain Layer**: Clean dataclasses with boundary validation.
- **Service Layer**: High-performance algorithms and state management.
- **Test Suite**: Automated `unittest` test suite verified in isolated sandbox.

## Getting Started
1. Run the test suite:
   ```bash
   python -m unittest
   ```

## Automated Verification
- Total Tests: 6
- Status: PASSED (100%)
- Sandboxed Execution: Verified in isolated temporary workspace
"""
            return DocumentationResult(
                project_overview=f"{title} is an automated multi-agent engineered system.",
                architecture_explanation="Layered architecture separating domain entities, service logic, and automated tests.",
                setup_instructions="Execute tests via `python -m unittest`.",
                api_documentation="Methods: log_period, get_all_logs, predict_cycle.",
                agent_workflow_description="Requirements -> Planning -> Architecture -> Senior Review -> Code Generation -> Testing -> Debugging -> Security -> Optimization -> Final Review -> Documentation.",
                testing_guide="Run `python -m unittest` inside workspace.",
                known_limitations="Operates with standard clinical averages; cycles naturally vary.",
                future_improvements="Add persistent database adapter and mobile client.",
                readme_markdown=readme_text,
            )

        raise ValueError(f"MockGeminiProvider: Unhandled schema {schema}")
