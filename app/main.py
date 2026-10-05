from typing import Dict

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exceptions import register_exception_handlers
import logging

from sqlalchemy import select

from app.core.database import get_db
from app.core.security import verify_password
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import RolePermission

from app.core.auth import authenticate
from app.core.permissions import require_permission

from app.schemas.chat import ChatRequest, ChatResponse

from qdrant_client import QdrantClient

from app.services.context.builder import ContextBuilder
from app.services.embeddings.qwen import QwenEmbeddingService
from app.services.query.processor import QueryProcessor
from app.services.retrieval.service import RetrievalService

from qdrant_client.models import Filter, FieldCondition, MatchValue
from sqlalchemy.orm import Session

from app.core.permissions import get_user_permissions

from app.services.rag.prompt import RAGPrompt
from app.services.rag.attribution import SourceAttributor
from app.services.llm.factory import get_llm_client

setup_logging()

logger = logging.getLogger(__name__)
logger.info("FinSolve AI application initialized")
logger.info("Application started")

app = FastAPI()
security = HTTPBasic()
register_exception_handlers(app)

qdrant_client = QdrantClient(path="./qdrant_data")
embedding_service = QwenEmbeddingService()

query_processor = QueryProcessor()
retrieval_service = RetrievalService(
    client=qdrant_client,
    embedding_service=embedding_service,
)
context_builder = ContextBuilder()

rag_prompt = RAGPrompt()
source_attributor = SourceAttributor()
llm_client = get_llm_client()
# Authentication dependency
# def authenticate(
#     credentials: HTTPBasicCredentials = Depends(security),
#     db=Depends(get_db),
# ):
#     username = credentials.username
#     password = credentials.password
#     user = db.scalar(
#         select(User)
#         .where(User.username == username)
#     )

#     if user is None or not user.is_active:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid credentials",
#             headers={"WWW-Authenticate": "Basic"},
#         )

#     if not verify_password(
#         password,
#         user.password_hash,
#     ):
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid credentials",
#             headers={"WWW-Authenticate": "Basic"},
#         )

#     return {
#         "username": user.username,
#         "role": user.role.name,
#     }


# Login endpoint
@app.get("/login")
def login(user=Depends(authenticate)):
    return {
        "message": f"Welcome {user.username}",
        "role": user.role,
    }


# Protected test endpoint
@app.get("/test")
def test(user=Depends(authenticate)):
    return {
        "message": f"Hello {user['username']}! You can now chat.",
        "role": user["role"],
    }


@app.get("/resources/finance")
def finance_resources(
    user=Depends(require_permission("read_finance")),
):
    return {
        "message": "Finance resources accessible",
        "user": user.username,
    }


@app.get("/resources/marketing")
def marketing_resources(
    user=Depends(require_permission("read_marketing")),
):
    return {
        "message": "Marketing resources accessible",
        "user": user.username,
    }


@app.get("/resources/hr")
def hr_resources(
    user=Depends(require_permission("read_hr")),
):
    return {
        "message": "HR resources accessible",
        "user": user.username,
    }


@app.get("/resources/engineering")
def engineering_resources(
    user=Depends(require_permission("read_engineering")),
):
    return {
        "message": "Engineering resources accessible",
        "user": user.username,
    }


@app.get("/resources/general")
def general_resources(
    user=Depends(require_permission("read_general")),
):
    return {
        "message": "General resources accessible",
        "user": user.username,
    }


@app.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    user = Depends(authenticate),
    db: Session = Depends(get_db),
):
    query = query_processor.process(request.message)

    allowed_permissions = get_user_permissions(user.user_id, db)

    print(
        f"User={user.username}, "
        f"Permissions={sorted(allowed_permissions)}"
    )

    query_filter = Filter(
        should=[
            FieldCondition(
                key="required_permission",
                match=MatchValue(value=permission),
            )
            for permission in sorted(allowed_permissions)
        ]
    )

    results = retrieval_service.retrieve(
        query=query,
        limit=5,
        query_filter=query_filter,
    )

    for result in results:
        print(
            f"Document={result.document_id}, "
            f"Chunk={result.chunk_index}, "
            f"Permission={result.required_permission}"
        )

    context = context_builder.build(results)

    prompt = rag_prompt.build(
        retrieved_context=context.text,
        user_question=query.processed,
    )

    answer = llm_client.generate(prompt)

    sources = source_attributor.build(context.sources)

    return ChatResponse(
        answer=answer,
        sources=sources,
    )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host='127.0.0.1',
        port='8000',
        reload=True,
    )