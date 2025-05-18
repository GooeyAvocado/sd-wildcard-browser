import os
import gradio as gr
from fastapi import FastAPI, APIRouter
from modules import script_callbacks  # A1111's callback system

# Set the wildcards folder (symlinked in your extension)
WILDCARDS_DIR = os.path.join(os.path.dirname(__file__), "../wildcards")

# Create API Router
router = APIRouter()

@router.get("/wildcards")
async def get_all_wildcards():
    """Retrieve all wildcard files and their contents as a dictionary."""
    if not os.path.exists(WILDCARDS_DIR):
        return {"error": "Wildcards folder not found"}

    wildcards_map = {}

    for filename in os.listdir(WILDCARDS_DIR):
        filepath = os.path.join(WILDCARDS_DIR, filename)
        
        if os.path.isfile(filepath):
            with open(filepath, "r", encoding="utf-8") as file:
                wildcards_map[filename[:-4]] = [line.strip() for line in file]  # Trim newlines

    return wildcards_map

# Corrected function signature
def on_app_started(demo: gr.Blocks, app: FastAPI):
    """Register API routes when A1111 starts."""
    app.include_router(router, prefix="/sd-wildcard-browser", tags=["Wildcards"])

# Hook into A1111 startup
script_callbacks.on_app_started(on_app_started)
