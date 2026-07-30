"""Multimodal helper: analyze a local image and upload it to the LangSmith trace.

Used by Modules 1 (Deep Agents) and 3 (LangSmith) to demo LangSmith's
file-attachment support. The agent calls the `analyze_image` tool with a local
image path; the underlying vision call is wrapped in a `@traceable` function that
receives the picture as a `langsmith.schemas.Attachment`, so the exact image the
model saw is uploaded to that run and rendered inline in the trace.

Docs: https://docs.langchain.com/langsmith/upload-files-with-traces
"""

from __future__ import annotations

import base64
import mimetypes
from pathlib import Path

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langsmith import traceable
from langsmith.schemas import Attachment

from utils.models import model

# --- Guards for an LLM-supplied file path --------------------------------------
# The agent chooses `image_path`, so we treat it as untrusted: confine reads to
# the workshop repo, allow only image extensions, and cap the size. This keeps a
# deployed agent from reading arbitrary files (and shipping their bytes to the
# model / trace).
BASE_DIR = Path(__file__).resolve().parent.parent  # workshop repo root
ALLOWED_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif"}
MAX_BYTES = 10 * 1024 * 1024  # 10 MB
_MIME_FALLBACK = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".avif": "image/avif",
}


@traceable(name="describe_image")
def _describe_image(question: str, image: Attachment) -> str:
    """Vision model call. The `image: Attachment` argument is what LangSmith
    uploads to this run — that's the whole point of the demo."""
    b64 = base64.b64encode(image.data).decode()
    message = HumanMessage(
        content_blocks=[
            {"type": "text", "text": question},
            {"type": "image", "base64": b64, "mime_type": image.mime_type},
        ]
    )
    content = model.invoke([message]).content
    if isinstance(content, list):  # some providers return a list of blocks
        content = " ".join(
            part.get("text", "") for part in content if isinstance(part, dict)
        ).strip()
    return content


@tool(parse_docstring=True)
def analyze_image(
    image_path: str,
    question: str = "Describe this image in detail.",
) -> str:
    """Analyze a local image file with a vision model and return a text description.

    Use this to inspect diagrams, screenshots, or photos the user refers to. The
    image is uploaded to the LangSmith trace so it can be reviewed alongside the run.

    Args:
        image_path: Path to a local image file (png, jpg, jpeg, gif, webp, or avif).
        question: What to ask the vision model about the image.
    """
    path = Path(image_path).expanduser()
    if not path.is_absolute():
        path = BASE_DIR / path
    try:
        path = path.resolve()
    except OSError:
        return f"Could not resolve path: {image_path!r}"

    if BASE_DIR != path and BASE_DIR not in path.parents:
        return f"Refused: {image_path!r} is outside the workshop directory."
    if path.suffix.lower() not in ALLOWED_EXT:
        return (
            f"Refused: {path.suffix!r} is not an allowed image type "
            f"({', '.join(sorted(ALLOWED_EXT))})."
        )
    if not path.is_file():
        return f"No such image file: {path}"
    size = path.stat().st_size
    if size > MAX_BYTES:
        return f"Refused: image is {size:,} bytes (limit {MAX_BYTES:,})."

    mime = mimetypes.guess_type(str(path))[0] or _MIME_FALLBACK.get(
        path.suffix.lower(), "application/octet-stream"
    )
    return _describe_image(question, Attachment(mime_type=mime, data=path.read_bytes()))
