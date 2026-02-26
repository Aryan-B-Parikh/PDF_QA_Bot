"""
main.py
~~~~~~~
Application entry-point.

Responsibilities (and *only* these):
  - Create the FastAPI application instance.
  - Register global middleware (CORS, rate-limit error handler).
  - Include the API router.
  - Run ``uvicorn`` when executed directly.

All business logic lives in the ``api``, ``services``, ``models``, and ``core``
packages.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from api.routes import router
from core.config import _rate_limit_exceeded_handler, limiter

app = FastAPI(
    title="PDF QA Bot API",
    description="PDF Question-Answering Bot (Session-based)",
    version="3.0.0",
)

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(router)


# ---------------------------------------------------------------------------
# Dev runner
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=False)