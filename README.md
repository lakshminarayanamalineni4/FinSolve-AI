# DS RPC 01: FinSolve AI

FinSolve AI is an internal chatbot project for the Codebasics GenAI Data Science Resume Project Challenge. The target product is a retrieval-augmented generation (RAG) chatbot with role-based access control (RBAC) over departmental company documents.

The repository is currently in the **API and authentication scaffold phase**. The FastAPI service, HTTP Basic authentication, structured project layout, settings, logging, and global exception handling are implemented. Document ingestion, retrieval, LLM responses, and RBAC-filtered chat are planned but are not implemented yet.

Challenge: [DS RPC-01](https://codebasics.io/challenge/codebasics-gen-ai-data-science-resume-project-challenge)

## Current Architecture

```text
Client
	|
	v
FastAPI application (app/main.py)
	|
	+-- HTTP Basic authentication
	|     +-- in-memory users_db
	|     +-- username/password validation
	|     +-- username and role dependency
	|
	+-- Protected endpoints: /login, /test, /chat
	+-- Global exception handler -> generic HTTP 500 response
	+-- Logging configured from app settings
	|
	+-- resources/data/ (departmental knowledge base; not connected yet)
```

### Application modules

| Path | Responsibility |
| --- | --- |
| `app/main.py` | Creates the FastAPI app, configures authentication, stores development users, and defines the current endpoints. |
| `app/core/config.py` | Loads `app_name`, `app_env`, and `log_level` from defaults or an optional `.env` file. |
| `app/core/logging.py` | Configures the Python root logger using `LOG_LEVEL`. |
| `app/core/exceptions.py` | Registers the generic unhandled-exception handler. |
| `app/schemas/` | Reserved for request and response models. |
| `app/services/` | Reserved for application and RAG services. |
| `app/utils/` | Reserved for shared utilities. |
| `resources/data/` | Department-organized source documents for the future knowledge base. |

## Setup

Requirements:

- Python 3.10 or newer
- [uv](https://docs.astral.sh/uv/)

From the repository root, create the environment and install the project:

```bash
uv venv
uv sync
```

Activate the environment when using a shell directly:

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

The application has development defaults, so no `.env` file is required. Optional settings can be provided in `.env`:

```env
APP_NAME=FinSolve AI
APP_ENV=development
LOG_LEVEL=INFO
```

## Run the API

Start the development server with:

```bash
uv run uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. FastAPI's interactive documentation is available at `http://127.0.0.1:8000/docs`, with the OpenAPI schema at `http://127.0.0.1:8000/openapi.json`.

## Current API

All endpoints use HTTP Basic authentication.

| Method | Path | Current behavior |
| --- | --- | --- |
| `GET` | `/login` | Validates credentials and returns a welcome message and the user's role. |
| `GET` | `/test` | Validates credentials and returns a protected test response. |
| `POST` | `/chat` | Authenticates the user, but currently returns the placeholder `Implement this endpoint.`. |

Example request:

```bash
curl -u Tony:password123 http://127.0.0.1:8000/login
```

Invalid or missing credentials return HTTP 401. The current chat parameter is a simple query parameter, not a JSON request body:

```bash
curl -u Tony:password123 -X POST "http://127.0.0.1:8000/chat?message=Hello"
```

## Development Users

These credentials are hard-coded in `app/main.py` for local development only. They must be replaced with a secure identity and credential store before deployment.

| Username | Password | Role |
| --- | --- | --- |
| Tony | `password123` | engineering |
| Peter | `pete123` | engineering |
| Bruce | `securepass` | marketing |
| Sid | `sidpass123` | marketing |
| Sam | `financepass` | finance |
| Natasha | `hrpass123` | hr |

The available department labels are `engineering`, `finance`, `general`, `hr`, and `marketing`. The current authentication layer identifies a user's role, but does not yet enforce document permissions.

## Knowledge Base

Source data is organized by department:

```text
resources/data/
├── engineering/engineering_master_doc.md
├── finance/
│   ├── financial_summary.md
│   └── quarterly_financial_report.md
├── general/employee_handbook.md
├── hr/hr_data.csv
└── marketing/
		├── market_report_q4_2024.md
		├── marketing_report_2024.md
		├── marketing_report_q1_2024.md
		├── marketing_report_q2_2024.md
		└── marketing_report_q3_2024.md
```

These files are currently static resources. No parser, chunker, embedding model, vector store, retrieval filter, or LLM is connected to them yet.

## Planned RAG and RBAC Flow

The intended security boundary is role-filtered retrieval before context is sent to an LLM:

```text
Authenticate user
	-> resolve role and permissions
	-> retrieve only authorized document chunks
	-> generate an answer from authorized context
	-> return the answer with source attribution
```

Planned work includes document ingestion for Markdown and CSV files, embeddings and a vector store, role-to-document permission mapping, chat request/response schemas, LLM integration, guardrails, conversation history, tests, and deployment configuration.
