# DS-RPC-01: Project Analysis & Architecture

## Project Overview

**Project Name:** DS RPC 01 - Internal Chatbot with Role Based Access Control  
**Type:** RAG-based (Retrieval-Augmented Generation) Internal Chatbot  
**Challenge Source:** Codebasics Gen AI Data Science Resume Project Challenge  
**Python Version:** >=3.10  
**Status:** Early Development Phase

## Current Progress

### Completed Components
1. **Basic Authentication System**
   - HTTPBasic authentication implemented in FastAPI
   - User database with credentials and role mapping
   - 6 sample users with different roles

2. **Project Structure**
   - FastAPI application scaffold
   - Modular folder organization for services, schemas, and utilities
   - Resource data repository organized by department

3. **API Endpoints (Skeleton)**
   - `/login` - Authentication endpoint
   - `/test` - Protected test endpoint  
   - `/chat` - Protected chat endpoint (NOT YET IMPLEMENTED)

### Current User Database
```
- Tony (engineering) | password: password123
- Bruce (marketing) | password: securepass
- Sam (finance) | password: financepass
- Peter (engineering) | password: pete123
- Sid (marketing) | password: sidpass123
- Natasha (hr) | password: hrpass123
```

### Not Yet Implemented
- RAG (Retrieval-Augmented Generation) functionality
- LLM integration
- Role-based access control for chat queries
- Vector database/embeddings for document retrieval
- Chat logic and message processing
- Document parsing and ingestion

---

## Architecture

### Technology Stack
- **Framework:** FastAPI
- **Authentication:** HTTPBasic
- **Python Version:** >=3.10
- **Package Manager:** uv (based on user preference)

### Project Structure
```
ds-rpc-01/
├── pyproject.toml                 # Project configuration
├── README.md                       # Project description
├── PROJECT_ANALYSIS.md            # This file
│
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application with auth
│   ├── schemas/                   # Pydantic models for request/response
│   │   └── __init__.py
│   ├── services/                  # Business logic (RAG, LLM)
│   │   └── __init__.py
│   └── utils/                     # Utility functions
│       └── __init__.py
│
└── resources/
    └── data/                      # Knowledge base organized by role
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

### Authentication Flow
```
User Request → HTTPBasic Credentials → Authenticate Dependency
    ↓
    Verify against users_db
    ↓
    Return {username, role} or Raise 401 HTTPException
    ↓
    Protected Endpoint Access
```

### Role-Based Access Control (RBAC)
The system defines 5 roles with corresponding resource access:

| Role | Users | Resources | Purpose |
|------|-------|-----------|---------|
| **engineering** | Tony, Peter | engineering_master_doc.md | Engineering team queries |
| **finance** | Sam | financial_summary.md, quarterly_financial_report.md | Financial team queries |
| **hr** | Natasha | hr_data.csv | HR team queries |
| **marketing** | Bruce, Sid | market_report_q4_2024.md, marketing_report_*.md | Marketing team queries |
| **general** | All users | employee_handbook.md | All-access resources |

### Current API Endpoints

#### 1. **GET /login**
- **Auth:** HTTPBasic (username, password)
- **Purpose:** User authentication and role verification
- **Response:** `{"message": "Welcome {username}!", "role": "{role}"}`
- **Status:** ✅ Implemented

#### 2. **GET /test**
- **Auth:** HTTPBasic (username, password)
- **Purpose:** Test authenticated access
- **Response:** `{"message": "Hello {username}! You can now chat.", "role": "{role}"}`
- **Status:** ✅ Implemented

#### 3. **POST /chat**
- **Auth:** HTTPBasic (username, password)
- **Purpose:** Main RAG chatbot endpoint
- **Parameters:** 
  - `message` (string, default: "Hello")
  - `user` (dependency-injected from auth)
- **Response:** "Implement this endpoint."
- **Status:** ⏳ NOT IMPLEMENTED

---

## Implementation Roadmap

### Phase 1: Core Infrastructure (Current)
- [x] Project structure
- [x] Authentication system
- [x] API skeleton
- [ ] Fix Natasha's password typo

### Phase 2: RAG Implementation (Next)
- [ ] Document ingestion pipeline (parsing MD and CSV files)
- [ ] Vector embeddings generation (OpenAI, HuggingFace, or local model)
- [ ] Vector database setup (Pinecone, Weaviate, ChromaDB, or Milvus)
- [ ] Document chunking strategy

### Phase 3: LLM Integration
- [ ] LLM API integration (OpenAI, Hugging Face, Claude, or local model)
- [ ] Prompt template design
- [ ] Context window management

### Phase 4: Role-Based Filtering
- [ ] Access control middleware for /chat endpoint
- [ ] Role-to-resource mapping enforcement
- [ ] Query filtering based on user role

### Phase 5: Chat Endpoint Implementation
- [ ] Message processing logic
- [ ] Retrieval from vector database
- [ ] LLM response generation
- [ ] Context management (conversation history)

### Phase 6: Testing & Deployment
- [ ] Unit tests for auth
- [ ] Integration tests for chat
- [ ] API documentation (FastAPI auto-docs at /docs)
- [ ] Docker containerization
- [ ] Deployment setup

---

## Data Resources Available

### By Role:
- **Engineering:** 1 document (master doc)
- **Finance:** 2 documents (summary + quarterly report)
- **HR:** 1 CSV dataset
- **Marketing:** 5 documents (quarterly + annual reports)
- **General:** 1 document (employee handbook) - accessible to all

**Total:** 10 knowledge base documents across 5 functional areas

---

## Key Dependencies

Currently declared in `pyproject.toml`:
- `fastapi[standard]>=0.115.12` - Web framework with built-in validation

**Will likely need to add:**
- `uvicorn` - ASGI server
- `pydantic` - Data validation (comes with FastAPI)
- `openai` or similar - LLM API client
- `langchain` or `llama-index` - RAG framework (optional, for orchestration)
- `numpy`, `scikit-learn` - Embeddings and utilities
- `chromadb` or `pinecone-client` - Vector database

---

## Known Issues

1. **Typo in users_db:** Natasha's entry has `"passwoed"` instead of `"password"`
2. **Chat endpoint incomplete:** `/chat` returns placeholder string

---

## Next Steps for Development

1. Fix the password typo for Natasha
2. Add Pydantic schemas for chat request/response
3. Implement document loader service
4. Set up vector database and embeddings
5. Integrate LLM
6. Implement role-based filtering logic
7. Complete `/chat` endpoint implementation
