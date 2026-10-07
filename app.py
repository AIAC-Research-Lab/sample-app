"""
Greeting App
------------
A single-page FastAPI app that asks for a user's name and displays a greeting.

Teaching notes:
- Input is validated to accept ONLY alphabetic characters (no digits), on purpose,
  so students can see how input validation + error handling works.
- Logging is configured to write to a proper log directory (./logs/app.log)
  alongside console output, using Python's standard `logging` module.
"""

import logging
import os
import re

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

os.makedirs(LOG_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------
logger = logging.getLogger("greeting_app")
logger.setLevel(logging.DEBUG)

log_format = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(log_format)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(log_format)

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
# Deliberately restrictive: letters and spaces only, no digits, no symbols.
NAME_PATTERN = re.compile(r"^[A-Za-z ]+$")


def is_valid_name(name: str) -> bool:
    """Return True only if the name contains letters/spaces (no digits)."""
    return bool(name) and bool(NAME_PATTERN.match(name))


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(title="Greeting App")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "greeting": None, "error": None}
    )


@app.post("/", response_class=HTMLResponse)
async def submit(request: Request, username: str = Form("")):
    username = username.strip()
    greeting = None
    error = None

    logger.info("Received submission: raw_input=%r", username)

    if not username:
        error = "Name cannot be empty."
        logger.warning("Validation failed: empty input")
    elif not is_valid_name(username):
        error = "Invalid name: only letters (no digits or symbols) are allowed."
        logger.error("Validation failed: non-alphabetic input=%r", username)
    else:
        greeting = f"Hello, {username}! Welcome."
        logger.info("Greeting generated for user=%r", username)

    return templates.TemplateResponse(
        "index.html", {"request": request, "greeting": greeting, "error": error}
    )


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Greeting App on http://127.0.0.1:5000")
    uvicorn.run(app, host="127.0.0.1", port=5000)
