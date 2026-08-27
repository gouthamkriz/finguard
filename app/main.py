"""
FinGuard FastAPI Application Entry Point.
Source of Truth: Approved Stage 7 Specification.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from neo4j.exceptions import AuthError, ConfigurationError, ServiceUnavailable

from app.services import db_service
from app.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Initializes database driver on startup and closes driver cleanly on shutdown.
    """
    print("[STARTUP] Initializing CognoDB database connection...", flush=True)
    db_service.initialize()
    yield
    print("[SHUTDOWN] Closing CognoDB database connection...", flush=True)
    db_service.close()

app = FastAPI(
    title="FinGuard Backend API",
    description="Financial Fraud & Synthetic Identity Relationship Explorer Graph Intelligence API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# CORS Configuration for local development and the production Vercel frontend
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "https://finguard-nine.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.middleware("http")
async def reject_duplicate_query_parameters(request: Request, call_next):
    """Reject ambiguous duplicate query keys before endpoint parameter parsing."""
    seen = set()
    for key, _ in request.query_params.multi_items():
        if key in seen:
            return JSONResponse(
                status_code=422,
                content={"error": {"code": "VALIDATION_ERROR", "message": "Duplicate query parameters are not allowed."}},
            )
        seen.add(key)
    return await call_next(request)

# Global Exception Handler for safe error reporting
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail
    if isinstance(detail, dict) and "code" in detail and "message" in detail:
        error_payload = detail
    else:
        error_payload = {
            "code": "HTTP_ERROR",
            "message": str(detail) if detail else "An HTTP error occurred."
        }
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": error_payload}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Returns a stable, client-safe envelope for invalid request input."""
    return JSONResponse(
        status_code=422,
        content={"error": {"code": "VALIDATION_ERROR", "message": "Invalid request parameter."}},
    )

async def database_unavailable_exception_handler(request: Request, exc: Exception):
    """Maps connection and authentication failures to a safe service response."""
    return JSONResponse(
        status_code=503,
        content={"error": {"code": "DATABASE_UNAVAILABLE", "message": "Database is unavailable."}},
    )

app.add_exception_handler(ServiceUnavailable, database_unavailable_exception_handler)
app.add_exception_handler(AuthError, database_unavailable_exception_handler)
app.add_exception_handler(ConfigurationError, database_unavailable_exception_handler)

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Prevents unexpected internal failures from leaking implementation details."""
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "QUERY_FAILED", "message": "An unexpected error occurred while processing the request."}},
    )

# Include API router
app.include_router(router)
