from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.core.seed import seed_roles
from app.modules.topics.service import seed_fixed_categories, seed_auto_topics
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.domains.router import router as domains_router
from app.modules.topics.router import router as topics_router
from app.modules.sports.router import router as sports_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSessionLocal() as db:
        await seed_roles(db)
        await seed_fixed_categories(db)
        await seed_auto_topics(db)
    yield


app = FastAPI(
    title="Suite SEO API",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

_origins = settings.cors_origins_list
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials="*" not in _origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(domains_router, prefix="/api/domains", tags=["domains"])
app.include_router(topics_router, prefix="/api/topics", tags=["topics"])
app.include_router(sports_router, prefix="/api/sports", tags=["sports"])


@app.get("/api/health", tags=["system"])
async def health():
    async with AsyncSessionLocal() as db:
        await db.execute(text("SELECT 1"))
    return {"status": "ok"}
