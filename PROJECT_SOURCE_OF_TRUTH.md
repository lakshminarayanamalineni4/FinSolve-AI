# FinSolve AI — Secure Enterprise RAG Chatbot

## 1. Project Overview

**Project Name:** FinSolve AI — Secure Enterprise RAG Chatbot

**Project Type:** Enterprise RAG application with Role-Based Access Control, Guardrails, Monitoring, and RAG Evaluation

**Domain:** FinTech

**Primary Goal:**

Build a production-style AI-powered internal enterprise chatbot that allows employees to ask natural-language questions and receive context-aware answers from company documents while strictly enforcing role-based access to sensitive information.

The project is based on the Codebasics GenAI Data Science Resume Project Challenge and will be extended beyond the original requirements to demonstrate practical AI Engineering, backend engineering, security, observability, and deployment skills.

---

# 2. Business Problem

FinSolve Technologies has information distributed across departments such as:

* Finance
* Marketing
* HR
* Engineering
* General company information
* Executive-level information

Employees need quick access to relevant information, but sensitive departmental information must not be exposed to unauthorized users.

The system should provide a secure conversational interface where users can ask natural-language questions and receive answers based only on information they are authorized to access.

---

# 3. Final Product Goal

The completed application should provide:

* User authentication
* Role-based authorization
* Secure document access
* Document ingestion
* Document parsing
* Document chunking
* Embedding generation
* Vector search
* Metadata-based filtering
* RAG
* LLM-based response generation
* Source attribution
* Conversation memory
* Input guardrails
* Retrieval guardrails
* Output guardrails
* Monitoring and observability
* RAG evaluation
* Streamlit chatbot UI
* Dockerized deployment
* CI/CD
* AWS deployment

---

# 4. Core Security Principle

RBAC must be enforced **before unauthorized information reaches the LLM**.

The system must NOT follow this unsafe pattern:

```text
User
  ↓
Retrieve all documents
  ↓
Send everything to LLM
  ↓
Prompt LLM not to reveal restricted information
```

Instead, the system should follow:

```text
User
  ↓
Authentication
  ↓
Role identification
  ↓
Permission determination
  ↓
Role-filtered retrieval
  ↓
Only authorized context
  ↓
LLM
  ↓
Guardrails
  ↓
Response
```

The LLM must never be treated as the primary security boundary.

---

# 5. Existing Repository

The project was cloned from an existing repository.

Current structure:

```text
ds-rpc-01/
├── pyproject.toml
├── README.md
├── PROJECT_ANALYSIS.md
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   └── utils/
│       └── __init__.py
│
└── resources/
    └── data/
        ├── engineering/
        │   └── engineering_master_doc.md
        ├── finance/
        │   ├── financial_summary.md
        │   └── quarterly_financial_report.md
        ├── general/
        │   └── employee_handbook.md
        ├── hr/
        │   └── hr_data.csv
        └── marketing/
            ├── market_report_q4_2024.md
            ├── marketing_report_2024.md
            ├── marketing_report_q1_2024.md
            ├── marketing_report_q2_2024.md
            └── marketing_report_q3_2024.md
```

---

# 6. Existing Authentication

Current implementation uses FastAPI HTTP Basic authentication with an in-memory user dictionary in `app/main.py`.

Target persistence: PostgreSQL will become the primary relational database for users, roles, permissions, RBAC mappings, and document metadata/access-control metadata. The in-memory store is temporary scaffolding and must be replaced during Phase 2 when database persistence is implemented.

Existing users:

```text
Tony      → engineering
Bruce     → marketing
Sam       → finance
Peter     → engineering
Sid       → marketing
Natasha   → hr
```

Known issue:

Natasha's password entry contains a typo and must be verified and corrected after inspecting the actual implementation.

Do not assume the existing implementation is correct. Inspect it before modifying it.

---

# 7. Existing Role Model

Current roles:

| Role              | Accessible Data             |
| ----------------- | --------------------------- |
| Engineering       | Engineering + General       |
| Finance           | Finance + General           |
| HR                | HR + General                |
| Marketing         | Marketing + General         |
| C-Level Executive | All company data            |
| Employee/General  | General company information |

The original repository may not yet contain the C-Level and Employee roles. They must be introduced only after inspecting the current implementation and determining the appropriate design.

---

# 8. Knowledge Base

Current documents:

### Engineering

```text
engineering_master_doc.md
```

### Finance

```text
financial_summary.md
quarterly_financial_report.md
```

### HR

```text
hr_data.csv
```

### Marketing

```text
market_report_q4_2024.md
marketing_report_2024.md
marketing_report_q1_2024.md
marketing_report_q2_2024.md
marketing_report_q3_2024.md
```

### General

```text
employee_handbook.md
```

Total current documents:

```text
10
```

The actual contents of these files must be inspected before designing the final ingestion/chunking strategy.

---

# 9. Target Architecture

Target architecture:

```text
                         ┌──────────────────┐
                         │   Streamlit UI   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     FastAPI      │
                         │    API Layer     │
                         └────────┬─────────┘
                                  │
                     ┌────────────┴────────────┐
                     ▼                         ▼
              Authentication              Input Guardrail
                     │                         │
                     └────────────┬────────────┘
                                  ▼
                                 RBAC
                                  │
                                  ▼
                            PostgreSQL
                     (users, roles, permissions,
                      RBAC mappings, document metadata,
                      access-control metadata)
                                  │
                                  ▼
                           Query Processing
                     │
                     ▼
            Role-Filtered Retrieval
                     │
                     ▼
                Vector DB
           (embeddings + retrieval metadata)
                     │
                     ▼
                 Reranking
                     │
                     ▼
              Context Builder
                     │
                     ▼
                    LLM
                     │
                     ▼
              Output Guardrail
                     │
                     ▼
             Source Attribution
                     │
                     ▼
                 Response

                  Monitoring
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
        Logs      Metrics     Traces
```

### Data storage responsibilities

| Store | Responsibility |
| ----- | -------------- |
| **PostgreSQL** | Primary relational database for users, roles, permissions, RBAC mappings, document metadata, and access-control metadata |
| **Vector DB** | Embeddings and retrieval-optimized metadata for semantic search and role-filtered retrieval |

PostgreSQL is the source of truth for identity, authorization, and document access metadata. The vector database supports semantic retrieval and may hold denormalized metadata copies for efficient filtering, but authorization decisions must not depend on the vector database alone.

This architecture is a target. It must evolve based on implementation decisions rather than being blindly implemented all at once.

---

# 10. Technology Direction

Current/project technologies:

* Python
* FastAPI
* Pydantic
* uv
* PostgreSQL (primary relational database for users, roles, permissions, RBAC mappings, and document/access-control metadata)
* LLM API
* Embedding model/API
* Vector database
* Streamlit
* Docker
* GitHub Actions
* AWS

Potential technologies:

* Qdrant
* ChromaDB
* OpenAI
* Gemini
* Hugging Face
* LangChain
* LangGraph
* Redis
* OpenTelemetry
* Prometheus
* Grafana
* LangSmith

Do NOT introduce a technology merely because it is listed here.

Each technology should be introduced when it provides a clear engineering or learning benefit.

Prefer simple implementations before adding frameworks.

---

# 11. Development Philosophy

This project is both:

1. A real portfolio project
2. A learning project

Therefore, implementation must prioritize understanding.

Do not blindly generate large amounts of code.

For every implementation step:

```text
Understand
    ↓
Inspect existing code
    ↓
Design
    ↓
Implement
    ↓
Run
    ↓
Test
    ↓
Explain
    ↓
Update source of truth
    ↓
Move to next step
```

---

# 12. Strict One-Step-at-a-Time Rule

This is a mandatory project rule.

Only ONE development step may be implemented at a time.

Do NOT:

* Implement multiple roadmap phases together
* Create the entire RAG pipeline at once
* Add multiple unrelated features in one step
* Skip ahead because a future feature is obvious
* Rewrite the repository unnecessarily
* Introduce technologies before their planned stage

After completing one step:

1. Test the step
2. Explain what changed
3. Record the result
4. Update this source-of-truth file
5. Identify the next step
6. STOP

The next step must not be implemented until explicitly continued.

---

# 13. Development Phases

## Phase 0 — Repository Understanding & Stabilization

Goal: Understand the existing project before implementing AI functionality.

### Steps

* [x] 0.1 Inspect the complete existing repository
* [x] 0.2 Run the existing application
* [x] 0.3 Test existing `/login`
* [x] 0.4 Test existing `/test`
* [x] 0.5 Inspect authentication implementation
* [x] 0.6 Inspect existing user database and role mapping
* [x] 0.7 Fix Natasha password typo if confirmed
* [x] 0.8 Inspect all knowledge-base files
* [x] 0.9 Verify existing dependencies
* [x] 0.10 Document the current architecture

### Phase completion criteria

The existing application is understood, runs successfully, and known issues are documented/fixed.

---

# Phase 1 — Project Foundation

Goal: Establish clean application configuration and engineering foundations.

### Steps

* [x] 1.1 Review project configuration
* [x] 1.2 Establish environment configuration
* [x] 1.3 Introduce Pydantic Settings if required
* [x] 1.4 Establish application logging
* [x] 1.5 Establish configuration conventions
* [x] 1.6 Establish error-handling foundation
* [x] 1.7 Clean and document project structure

### Phase completion criteria

The application has a clean and maintainable foundation for further development.

---

# Phase 2 — Authentication & RBAC

Goal: Build a proper authorization system independent of RAG, backed by PostgreSQL for users, roles, permissions, and RBAC mappings.

### Steps

* [x] 2.1 Review authentication vs authorization
* [x] 2.2 Define role model
* [x] 2.3 Define permissions
* [x] 2.4 Define role-to-resource mapping
* [x] 2.5 Design PostgreSQL schema for users, roles, permissions, and RBAC mappings
* [x] 2.6 Configure PostgreSQL connection and database settings
* [x] 2.7 Implement PostgreSQL-backed user and role persistence
* [x] 2.8 Implement authorization dependency
* [x] 2.9 Implement access-denied behavior
* [x] 2.10 Add C-Level role
* [x] 2.11 Add Employee/General role
* [x] 2.12 Secure passwords appropriately
* [x] 2.13 Test every role/resource combination

### Phase completion criteria

Users can authenticate against PostgreSQL and access only resources permitted by their roles.

---

# Phase 3 — Document Ingestion

Goal: Convert the existing knowledge base into structured documents with metadata persisted in PostgreSQL.

### Steps

* [x] 3.1 Design document metadata model (PostgreSQL as canonical store)

  Document metadata is stored in PostgreSQL as the canonical metadata store.

  `documents`:
  - id
  - name
  - source_path
  - file_type
  - department
  - description
  - is_active
  - created_at
  - updated_at

  `document_permissions`:
  - document_id
  - permission_id

  The existing RBAC permission model is reused for document access control.
  Document content is not stored in PostgreSQL at this stage.
  Chunks and embeddings will be introduced in later phases.
* [x] 3.2 Implement Markdown loader
* [x] 3.3 Implement CSV loader
* [x] 3.4 Create normalized document representation
* [x] 3.5 Add department metadata
* [x] 3.6 Add access-control metadata
* [x] 3.7 Persist document metadata and access-control metadata in PostgreSQL
* [x] 3.8 Design chunking strategy

  Initial chunking strategy:
  - Target chunk size: approximately 800 characters.
  - Overlap: approximately 150 characters.
  - Markdown documents will use structure-aware chunking,
    preferring headings and paragraphs as boundaries.
  - CSV documents will preserve complete rows and group rows
    into chunks without splitting individual records.
  - Each generated chunk will inherit:
    - document_id
    - department
    - required_permission
  - Chunking parameters are initial baselines and may be tuned
    after retrieval evaluation.
  - Security metadata must be preserved on every chunk so that
    RBAC filtering can occur before retrieval results reach the LLM.  
* [x] 3.9 Implement chunking
* [x] 3.10 Validate generated chunks

### Phase completion criteria

All knowledge-base files can be converted into clean, metadata-rich chunks with document and access-control metadata stored in PostgreSQL.

---

# Phase 4 — Embeddings & Vector Database

Goal: Build semantic retrieval infrastructure.

### Steps

* [x] 4.1 Understand embeddings
* [x] 4.2 Select embedding model

  - Embedding Model Decision: Qwen/Qwen3-Embedding-0.6B
  - Deployment: Local inference
  - Initial output dimension: 1024
  - Rationale: Selected for its retrieval capabilities, instruction-aware embedding support, multilingual coverage, configurable embedding dimensions, local deployment capability, and suitability for the project's 16 GB RAM development environment.
* [x] 4.3 Generate embeddings
* [x] 4.4 Select vector database
  - Vector Database Decision: Qdrant
  - Deployment: Local/self-hosted initially
  - Rationale: Selected as a dedicated vector retrieval engine with strong metadata filtering, local deployment support, Python integration, and a clear separation between PostgreSQL's canonical document/RBAC data and semantic retrieval infrastructure.
* [x] 4.5 Create collection/index
* [x] 4.6 Store embeddings and retrieval metadata (aligned with PostgreSQL document/access-control metadata)
* [x] 4.7 Implement similarity search
* [x] 4.8 Test semantic retrieval
* [x] 4.9 Validate metadata filtering

### Phase completion criteria

Relevant documents/chunks can be retrieved semantically from the vector database.

---

# Phase 5 — Basic RAG

Goal: Build a working RAG pipeline without advanced security features.

### Steps

* [x] 5.1 Implement query processing
* [x] 5.2 Implement retrieval service
* [x] 5.3 Design context builder
* [x] 5.4 Design and implement LLM abstraction + configuration
* [x] 5.5 Create RAG prompt
* [x] 5.6 Implement LLM generation
* [x] 5.7 Implement source attribution
* [x] 5.8 Connect RAG to `/chat`
* [x] 5.9 Test end-to-end RAG

### Phase completion criteria

A user can ask a question and receive a grounded answer with document sources.

---

# Phase 6 — Secure RAG / RBAC Retrieval

Goal: Integrate authorization directly into retrieval.

### Steps

* [ ] 6.1 Define retrieval authorization policy
* [ ] 6.2 Implement metadata-based filtering
* [ ] 6.3 Apply role filtering before retrieval
* [ ] 6.4 Prevent unauthorized chunks from entering context
* [ ] 6.5 Implement C-Level unrestricted access
* [ ] 6.6 Implement general employee restrictions
* [ ] 6.7 Test cross-department access
* [ ] 6.8 Test prompt-based authorization bypass attempts

### Phase completion criteria

Unauthorized information cannot reach the RAG context through normal or adversarial queries.

---

# Phase 7 — Guardrails

Goal: Protect the system against unsafe or invalid interactions.

### Input Guardrails

* [ ] 7.1 Validate query input
* [ ] 7.2 Handle empty/invalid queries
* [ ] 7.3 Handle excessively long queries
* [ ] 7.4 Detect prompt injection patterns
* [ ] 7.5 Define off-topic behavior

### Retrieval Guardrails

* [ ] 7.6 Validate retrieved metadata
* [ ] 7.7 Validate role/resource compatibility
* [ ] 7.8 Reject unauthorized context

### Output Guardrails

* [ ] 7.9 Detect unsupported answers
* [ ] 7.10 Require source attribution
* [ ] 7.11 Handle insufficient context
* [ ] 7.12 Prevent sensitive-data leakage
* [ ] 7.13 Implement safe refusal behavior

### Phase completion criteria

The system handles malicious, invalid, unsupported, and unauthorized requests safely.

---

# Phase 8 — Conversation Memory

Goal: Support multi-turn conversations.

### Steps

* [ ] 8.1 Define conversation/session model
* [ ] 8.2 Implement chat history
* [ ] 8.3 Add conversation-aware retrieval
* [ ] 8.4 Manage context size
* [ ] 8.5 Introduce Redis if justified
* [ ] 8.6 Test multi-turn conversations

### Phase completion criteria

Users can have useful multi-turn conversations without uncontrolled context growth.

---

# Phase 9 — Monitoring & Observability

Goal: Make the application measurable and debuggable.

### Steps

* [ ] 9.1 Define observability requirements
* [ ] 9.2 Implement structured logging
* [ ] 9.3 Add request IDs
* [ ] 9.4 Track authentication events
* [ ] 9.5 Track retrieval latency
* [ ] 9.6 Track LLM latency
* [ ] 9.7 Track token usage where available
* [ ] 9.8 Track guardrail violations
* [ ] 9.9 Track errors
* [ ] 9.10 Evaluate tracing tools
* [ ] 9.11 Add monitoring dashboard if justified

### Phase completion criteria

Important application behavior can be observed, diagnosed, and measured.

---

# Phase 10 — RAG Evaluation

Goal: Quantitatively evaluate the RAG system.

### Steps

* [ ] 10.1 Create evaluation dataset
* [ ] 10.2 Define expected sources
* [ ] 10.3 Evaluate retrieval quality
* [ ] 10.4 Evaluate answer relevance
* [ ] 10.5 Evaluate faithfulness/groundedness
* [ ] 10.6 Evaluate source correctness
* [ ] 10.7 Evaluate RBAC correctness
* [ ] 10.8 Evaluate guardrails
* [ ] 10.9 Document baseline results
* [ ] 10.10 Improve weak areas

### Phase completion criteria

The RAG system has measurable quality and security evaluation results.

---

# Phase 11 — Streamlit UI

Goal: Build a usable chatbot interface.

### Steps

* [ ] 11.1 Create Streamlit application
* [ ] 11.2 Implement login
* [ ] 11.3 Display user role
* [ ] 11.4 Implement chat interface
* [ ] 11.5 Display source documents
* [ ] 11.6 Display access-denied responses
* [ ] 11.7 Display conversation history
* [ ] 11.8 Improve UX

### Phase completion criteria

Users can interact with the complete system through a usable chatbot UI.

---

# Phase 12 — Productionization & Deployment

Goal: Deploy the project as a production-style application.

### Steps

* [ ] 12.1 Create Dockerfile
* [ ] 12.2 Create Docker Compose configuration (including PostgreSQL service)
* [ ] 12.3 Containerize application
* [ ] 12.4 Add health checks
* [ ] 12.5 Add CI pipeline
* [ ] 12.6 Add automated tests to CI
* [ ] 12.7 Configure AWS infrastructure
* [ ] 12.8 Deploy backend
* [ ] 12.9 Deploy UI
* [ ] 12.10 Configure production environment
* [ ] 12.11 Validate deployed application
* [ ] 12.12 Document deployment

### Phase completion criteria

The application is reproducibly deployable and accessible in a production-like environment.

---

# 14. Testing Strategy

Testing must happen continuously rather than only at the end.

Testing categories:

### Unit Tests

Test individual:

* Authentication
* RBAC
* Document loaders
* Chunking
* Retrieval
* Guardrails
* Services

### Integration Tests

Test:

```text
Authentication → RBAC → Retrieval → RAG
```

### Security Tests

Test:

* Unauthorized roles
* Cross-department queries
* Prompt injection
* Permission bypass
* Sensitive-data leakage

### RAG Tests

Test:

* Retrieval relevance
* Source attribution
* Groundedness
* Insufficient context

---

# 15. Important Architectural Principles

## Principle 1 — Security before generation

Authorization must happen before sensitive data reaches the LLM.

## Principle 2 — Metadata is security-critical

Document chunks should contain authorization metadata. PostgreSQL is the canonical store for document metadata and access-control metadata; retrieval layers must stay consistent with that source of truth.

## Principle 3 — LLM is not a security boundary

Never rely only on prompts to enforce access control.

## Principle 4 — Retrieval and generation are separate concerns

Keep retrieval logic independent from LLM generation.

## Principle 5 — Simple before complex

Implement the basic solution first, then optimize.

## Principle 6 — Measure before optimizing

Use evaluation and monitoring data before introducing complexity.

## Principle 7 — Every feature must be testable

A feature is not complete merely because the code runs.

---

# 16. Current Project Status

## Current Phase

Phase 0 — Repository Understanding & Stabilization

## Current Step

0.1 — Inspect the complete existing repository

## Status

NOT STARTED

## Completed Steps

None yet.

## Next Step

Inspect the existing repository files and understand the current implementation before modifying anything.

---

# 17. Change Log

## 2026-08-21

Architectural decision: PostgreSQL is the primary relational database for users, roles, permissions, RBAC mappings, and document metadata/access-control metadata.

Updated target architecture, technology direction, Phase 2 (Authentication & RBAC), Phase 3 (Document Ingestion), Phase 4 (embeddings storage alignment), Phase 12 (Docker Compose), and architectural principles to reflect PostgreSQL persistence. No implementation changes have been made yet.

## 2026-08-18

Created the project Source of Truth.

Initial project roadmap established.

No implementation changes have been made yet.

---

# 18. Rules for Updating This Document

After completing every development step:

1. Update the checkbox for the completed step.
2. Update `Current Phase`.
3. Update `Current Step`.
4. Update `Status`.
5. Record important architectural decisions.
6. Record important implementation changes.
7. Record tests performed.
8. Record the next step.
9. Do not mark future steps as completed.
10. Do not modify the roadmap without discussing the architectural reason.

This document is the authoritative project state.

If other documents conflict with this document, this document should be treated as the current project state unless a newer architectural decision explicitly changes it.
