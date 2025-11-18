"""
Game Data Hub - FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.exceptions import GDHException
from app.api.v1 import auth, projects, tables, data, versions, columns, code
from app.di.container import Container

# Initialize settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Game Data Hub API",
    description="Oyun Veri Merkezi - Veri Orkestrasyon Katmanı",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DI container (for stateless services only)
container = Container()
container.wire()


# Exception handler
@app.exception_handler(GDHException)
async def gdh_exception_handler(request, exc: GDHException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(tables.router, prefix="/api/v1/tables", tags=["Tables"])
app.include_router(columns.router, prefix="/api/v1", tags=["Columns"])
app.include_router(data.router, prefix="/api/v1/data", tags=["Data"])
app.include_router(versions.router, prefix="/api/v1/versions", tags=["Versions"])
app.include_router(code.router, prefix="/api/v1/code", tags=["Code Generation"])


@app.get("/")
async def root():
    return {"message": "Game Data Hub API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

