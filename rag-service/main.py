"""
main.py
~~~~~~~
Application entry-point: create FastAPI app, register middleware, mount router.

All business logic lives in `api`, `services`, `models`, and `core` packages.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from api.routes import router
from core.config import limiter

app = FastAPI(
    title="PDF QA Bot API",
    description="PDF Question-Answering Bot (Session-based)",
    version="3.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# Mount API router
app.include_router(router)
>>>>>>> upstream/master


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=False)
