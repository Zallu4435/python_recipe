
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load Environment FIRST, before importing services that use env vars
load_dotenv()

from backend.app.database.db import load_db
from backend.app.routes import recipes

# Initialize App
app = FastAPI(title="Become-A-Cook AI")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup Event
@app.on_event("startup")
def startup_event():
    load_db()

# Include Routes
app.include_router(recipes.router, prefix="/recipes", tags=["recipes"])

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
