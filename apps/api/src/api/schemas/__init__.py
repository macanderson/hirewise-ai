# __init__.py
from api.schemas.auth import (
    Token,
    TokenData,
    UserRegister,
    UserLogin,
    PasswordChange,
    PasswordResetRequest,
    PasswordReset,
    UserResponse
)
from api.schemas.candidate import (
    CandidateBase,
    CandidateCreate,
    CandidateResponse,
    CareerLevel,
    EducationLevel,
    CandidateStatus,
    CandidateSource
)
from api.schemas.chat import (
    ChatMessage,
    ChatMessageCreate,
    ChatMessageResponse,
    ChatSessionCreate,
    ChatSessionResponse,
    ChatCompletionRequest,
    ChatCompletionResponse
)
from api.schemas.document import (
    DocumentBase,
    DocumentCreate,
    DocumentResponse,
    DocumentURLUpload,
    DocumentChunkResponse
)
from api.schemas.project import (
    ProjectCreate,
    ProjectResponse
)
from api.schemas.tenant import (
    TenantCreate,
    TenantResponse
)
from api.schemas.agent import (
    AgentBase,
    AgentCreate,
    AgentResponse
)
from api.schemas.job import (
    JobBase,
    JobCreate,
    JobResponse,
    JobStatus
)

__all__ = [
    # Auth schemas
    "Token",
    "TokenData",
    "UserRegister",
    "UserLogin",
    "PasswordChange",
    "PasswordResetRequest",
    "PasswordReset",
    "UserResponse",

    # Candidate schemas
    "CandidateBase",
    "CandidateCreate",
    "CandidateResponse",
    "CareerLevel",
    "EducationLevel",
    "CandidateStatus",
    "CandidateSource",

    # Chat schemas
    "ChatMessage",
    "ChatMessageCreate",
    "ChatMessageResponse",
    "ChatSessionCreate",
    "ChatSessionResponse",
    "ChatCompletionRequest",
    "ChatCompletionResponse",

    # Document schemas
    "DocumentBase",
    "DocumentCreate",
    "DocumentResponse",
    "DocumentURLUpload",
    "DocumentChunkResponse",

    # Job schemas
    "JobBase",
    "JobCreate",
    "JobResponse",
    "JobStatus",

    # Project schemas
    "ProjectCreate",
    "ProjectResponse",

    # Tenant schemas
    "TenantCreate",
    "TenantResponse",

    # Agent schemas
    "AgentBase",
    "AgentCreate",
    "AgentResponse"
]
