from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, scans, reports
from app.config import settings
from trust_wedo.parsers.playwright_parser import async_playwright

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize global playwright browser
    print("[INFO] Starting global Playwright browser...")
    app.state.playwright = await async_playwright().start()
    app.state.browser = await app.state.playwright.chromium.launch(
        headless=True,
        args=[
            '--no-sandbox', 
            '--disable-setuid-sandbox',
            '--disable-blink-features=AutomationControlled'
        ]
    )
    yield
    # Shutdown: Close browser
    print("[INFO] Closing global Playwright browser...")
    await app.state.browser.close()
    await app.state.playwright.stop()

app = FastAPI(
    title="Trust WEDO API",
    version="1.0.0",
    description="Trust WEDO SaaS Platform API",
    lifespan=lifespan
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由註冊
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(scans.router, prefix="/api/scans", tags=["scans"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])

@app.get("/")
def read_root():
    return {"message": "Trust WEDO API v1.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
