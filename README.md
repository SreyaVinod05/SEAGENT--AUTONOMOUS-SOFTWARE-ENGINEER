# SEAGENT - Agentic AI Software Engineering Platform

> **B.Tech Final-Year Computer Science Project**  
> An autonomous multi-agent software engineering framework that transforms natural-language software requirements into analyzed specifications, development plans, architectures, production-grade source code, automated test suites, debugging patches, and documentation using **Google Gemini** and **LangGraph**.

---

## 1. Project Overview

**SEAGENT** models a complete software engineering team rather than a single conversational chatbot. When given a natural-language requirement, SEAGENT coordinates 9 specialized autonomous agents to advance the project through the complete software development lifecycle (SDLC):

```
User Requirement
      ↓
[1. Requirements Agent]
      ↓
[2. Planning Agent]
      ↓
[3. Architecture Agent]
      ↓
[4. Senior Engineer Review] ── (Revision Loop if Rejected)
      ↓ Approved
[5. Coding Agent]
      ↓
[6. Testing Agent] (Safe Sandboxed Subprocess)
      ↓
 Test Result ── (FAIL) ──→ [7. Debugging Agent]
      │                           ↓ (Patches Code)
      │ (PASS / Max Retries)    [6. Testing Agent] (Re-test)
      ↓
[8. Final Review Agent]
      ↓
[9. Documentation Agent]
      ↓
Final Deliverables (Multi-File Code, Test Reports, ZIP Download, README)
```

---

## 2. System Architecture

- **Backend Framework**: Python 3.10+ / FastAPI with asynchronous background worker threads.
- **Workflow Orchestration**: **LangGraph** `StateGraph` coordinating nodes and conditional edges.
- **LLM Engine**: **Google Gemini** (`gemini-2.5-flash`, `gemini-1.5-flash`, `gemini-2.0-flash`) via the official `google-genai` SDK with strict Pydantic structured schemas.
- **Isolated Code Execution**: `SafeCodeExecutor` running tests inside ephemeral sandbox workspaces with execution timeouts, path sanitization, secret stripping, and automatic cleanup.
- **Persistence**: Thread-safe file & memory persistence saving all workflow stages, code deliverables, and test reports to `data/workflows/`.
- **Frontend Dashboard**: React 18, Vite, Modern CSS design system, Lucide icons, visual pipeline monitoring, file tree code viewer, test dashboard, debugging history, and markdown viewer.

---

## 3. Specialized Software Engineering Agents

| Agent | Specialized Role | Structured Output Schema |
| :--- | :--- | :--- |
| **1. Requirements Agent** | Analyzes user goals, extracts functional/non-functional requirements, constraints, assumptions, user actors, and acceptance criteria. | `RequirementAnalysisResult` |
| **2. Planning Agent** | Deconstructs requirements into ordered development steps, milestones, deliverables, dependencies, and priorities. | `DevelopmentPlanResult` |
| **3. Architecture Agent** | Formulates system style, presentation/backend layers, storage, REST API endpoints, module decomposition, data flow, and security safeguards. | `ArchitectureResult` |
| **4. Senior Engineer Agent** | Evaluates plan and architecture for over-engineering, contradictions, and security; issues an approval gate decision and quality score. | `SeniorReviewResult` |
| **5. Coding Agent** | Generates complete, multi-file source code and automated `unittest` test files according to the approved architecture. | `CodeGenerationResult` |
| **6. Testing Agent** | Executes test cases in an isolated subprocess sandbox; measures execution duration, pass/fail status, and captures stdout/stderr. | `TestExecutionReport` |
| **7. Debugging Agent** | Analyzes failed test assertions and stack traces; locates root causes and emits corrected code for iterative re-testing. | `DebuggingResult` |
| **8. Final Review Agent** | Conducts comprehensive quality audit; evaluates requirements coverage, code quality score (1-100), and maintainability. | `FinalReviewResult` |
| **9. Documentation Agent** | Authors technical documentation, setup guides, API reference, and a production-ready `README.md`. | `DocumentationResult` |

---

## 4. Folder Structure

```
backend/
├── app/
│   ├── agents/                   # 9 specialized software engineering agents
│   │   ├── base.py               # Base agent with Gemini structured output execution
│   │   ├── requirements_agent.py # Requirements analyst
│   │   ├── planning_agent.py     # Project planning lead
│   │   ├── architecture_agent.py # Principal system architect
│   │   ├── senior_engineer_agent.py # Staff reviewer & gate approval
│   │   ├── coding_agent.py       # Multi-file source code generator
│   │   ├── testing_agent.py      # Automated test runner agent
│   │   ├── debugging_agent.py    # Diagnostic and patching engineer
│   │   ├── final_review_agent.py # Final deliverable auditor
│   │   ├── documentation_agent.py # Technical documentation writer
│   │   └── Requirement.py        # Backward-compatible requirement module
│   ├── models/                   # Pydantic schemas for all agent deliverables
│   │   └── schemas.py
│   ├── providers/                # Gemini LLM & test providers
│   │   ├── gemini_provider.py    # Google GenAI SDK integration
│   │   └── mock_provider.py      # Test mode provider for offline evaluation
│   ├── routers/                  # FastAPI REST endpoints
│   │   └── workflow_router.py
│   ├── services/                 # Business logic and execution engines
│   │   ├── code_executor.py      # Isolated sandbox test runner
│   │   ├── workflow_runner.py    # Async background workflow coordinator
│   │   └── workflow_storage.py   # Thread-safe persistent run storage
│   ├── workflows/                # LangGraph StateGraph orchestration
│   │   ├── state.py              # TypedDict workflow state definition
│   │   └── engine.py             # Compiled LangGraph pipeline with conditional loops
│   └── config.py                 # Environment configuration loader
├── frontend/                     # React + Vite Dashboard
│   ├── src/
│   │   ├── components/           # UI tabs, pipeline visualizer, header, modal
│   │   ├── services/api.js       # Backend REST API client
│   │   ├── App.jsx               # Main dashboard controller
│   │   └── index.css             # Dark modern design system
│   ├── dist/                     # Production static build
│   └── vite.config.js
├── tests/                        # Automated backend test suite
│   └── test_backend.py
├── data/workflows/               # Persisted JSON workflow deliverables
├── .env.example                  # Environment configuration template
├── .env                          # Local environment secrets (not committed)
├── main.py                       # FastAPI entrypoint
└── requirements.txt              # Backend dependencies
```

---

## 5. Environment & Gemini Setup

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` and set your Google Gemini API key:
   ```ini
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-2.5-flash
   MAX_DEBUG_RETRIES=3
   CODE_EXECUTION_TIMEOUT_SECONDS=25
   ```
   > Obtain a free Gemini API key from [Google AI Studio](https://aistudio.google.com/).

---

## 6. Running the Application

### Option A: Unified FastAPI Serving (Backend + Built Frontend)
FastAPI automatically serves the built React frontend at `http://127.0.0.1:8000/`:

```powershell
# Inside backend directory with venv activated
.\venv\Scripts\uvicorn.exe main:app --reload --host 127.0.0.1 --port 8000
```
Open your browser at **`http://127.0.0.1:8000`** to view the SEAGENT Dashboard.  
FastAPI Interactive API docs: **`http://127.0.0.1:8000/docs`**

### Option B: Development Mode (Vite Hot Reload + FastAPI)
Run the backend in terminal 1:
```powershell
.\venv\Scripts\uvicorn.exe main:app --reload --port 8000
```

Run Vite dev server in terminal 2:
```powershell
cd frontend
npm run dev
```
Open **`http://localhost:5173`** for live React development with Vite proxy forwarding API requests to port 8000.

---

## 7. Running Backend Tests

Run the comprehensive automated unit test suite:
```powershell
.\venv\Scripts\python.exe -m unittest tests/test_backend.py
```

Tests verify:
- Health and system configuration endpoints (`/health`, `/api/v1/config`)
- Safe code sandbox execution (capturing pass and fail conditions)
- Multi-agent LangGraph workflow lifecycle, state transitions, and ZIP project export
- Debugging loop patching mechanics

---

## 8. Example Workflow Scenario

1. Click **"New Project"** in the top navigation bar.
2. Select the **"Task Management Engine"** preset:
   > *"Build a task management web application where users can create, update, delete and complete tasks. Each task should have a title, description, priority and completion status."*
3. Click **"Start SEAGENT Pipeline"**.
4. Watch the 9 agents execute sequentially on the interactive pipeline visualizer:
   - **Requirements Agent** extracts functional rules and acceptance criteria.
   - **Planning Agent** structures development steps and milestones.
   - **Architecture Agent** defines modular layers and REST APIs.
   - **Senior Engineer Agent** audits the architecture and issues approval.
   - **Coding Agent** generates `task_model.py`, `task_service.py`, and `test_tasks.py`.
   - **Testing Agent** runs the tests in an isolated sandbox and collects pass/fail metrics.
   - **Debugging Agent** intervenes if tests fail to supply automated patches.
   - **Final Review Agent** computes quality and coverage scores.
   - **Documentation Agent** generates the final project `README.md`.
5. Switch between tabs to explore each deliverable, view source code with the file explorer, or click **"Download Project"** to save a `.zip` archive.

---

## 9. Security & Isolated Code Execution

- **Environment Isolation**: Subprocess execution cleanses all sensitive tokens (`GEMINI_API_KEY`, etc.) before executing generated code.
- **Path Traversal Protection**: Relative paths with `..` or absolute paths are rejected.
- **Execution Timeout**: Enforces a strict 25-second timeout to prevent runaway infinite loops or resource starvation.
- **Sandboxed Cleanup**: Ephemeral temporary workspace folders are destroyed immediately upon test completion.
