#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx>=0.28"]
# ///
"""
Upload a file to Notion and attach it to a page.

Adapted from https://github.com/goonoo/mcp_notion_upload (MIT-style, public).
MCP server wrapper removed; this is a standalone CLI.

Usage:
    python notion_upload.py <file_path> <page_id> [--caption TEXT] [--filename NAME] [--block-type auto|image|file]

Env:
    NOTION_API_TOKEN  Notion integration token (required)

Output:
    Prints JSON to stdout with: file_upload_id, file_block_id, download_url,
    expiry_time, filename, content_type, file_size, block_type.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
from pathlib import Path
from typing import Any

import httpx

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
MAX_SIZE = 20 * 1024 * 1024  # 20MB — Notion single-part upload limit

IMAGE_MIME_PREFIX = "image/"


def resolve_block_type(requested: str, content_type: str) -> str:
    if requested == "auto":
        return "image" if content_type.startswith(IMAGE_MIME_PREFIX) else "file"
    return requested


def build_block_payload(block_type: str, file_upload_id: str, caption_text: str) -> dict[str, Any]:
    caption = (
        [{"type": "text", "text": {"content": caption_text}}]
        if caption_text
        else []
    )
    return {
        "children": [
            {
                "object": "block",
                "type": block_type,
                block_type: {
                    "type": "file_upload",
                    "file_upload": {"id": file_upload_id},
                    "caption": caption,
                },
            }
        ]
    }


def upload_and_attach(
    file_path: Path,
    page_id: str,
    token: str,
    filename: str | None,
    caption: str | None,
    block_type_request: str,
) -> dict[str, Any]:
    if not file_path.exists():
        raise SystemExit(f"File not found: {file_path}")

    size = file_path.stat().st_size
    if size > MAX_SIZE:
        raise SystemExit(f"File size {size / 1024 / 1024:.2f}MB exceeds 20MB limit")

    upload_name = filename or file_path.name
    content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
    block_type = resolve_block_type(block_type_request, content_type)

    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
    }

    with httpx.Client(timeout=60.0) as client:
        create = client.post(
            f"{NOTION_API}/file_uploads",
            headers={**headers, "Content-Type": "application/json"},
            json={"name": upload_name},
        )
        create.raise_for_status()
        created = create.json()
        file_upload_id = created.get("id")
        upload_url = created.get("upload_url")
        if not file_upload_id or not upload_url:
            raise SystemExit(f"Notion did not return upload id/url: {created}")

        with file_path.open("rb") as f:
            up = client.post(
                upload_url,
                headers=headers,
                files={"file": (upload_name, f, content_type)},
            )
            up.raise_for_status()

        normalized_page = page_id.replace("-", "")
        attach = client.patch(
            f"{NOTION_API}/blocks/{normalized_page}/children",
            headers={**headers, "Content-Type": "application/json"},
            json=build_block_payload(block_type, file_upload_id, caption or ""),
        )
        attach.raise_for_status()
        attached = attach.json()

        results = attached.get("results") or []
        if not results:
            raise SystemExit(f"Block attach returned no results: {attached}")
        block = results[0]
        block_id = block.get("id")
        block_payload = block.get(block_type, {})
        file_data = block_payload.get("file", {})
        download_url = file_data.get("url")
        expiry = file_data.get("expiry_time")

        return {
            "status": "success",
            "file_upload_id": file_upload_id,
            "file_block_id": block_id,
            "block_type": block_type,
            "download_url": download_url,
            "expiry_time": expiry,
            "filename": upload_name,
            "content_type": content_type,
            "file_size": size,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Upload a file to Notion and attach it to a page.")
    parser.add_argument("file_path", type=Path)
    parser.add_argument("page_id")
    parser.add_argument("--caption", default=None)
    parser.add_argument("--filename", default=None)
    parser.add_argument(
        "--block-type",
        choices=("auto", "image", "file"),
        default="auto",
        help="Block type to create. 'auto' picks image for image/* mimes, else file.",
    )
    args = parser.parse_args()

    token = os.environ.get("NOTION_API_TOKEN")
    if not token:
        print("NOTION_API_TOKEN env var is required", file=sys.stderr)
        return 2

    try:
        result = upload_and_attach(
            args.file_path,
            args.page_id,
            token,
            args.filename,
            args.caption,
            args.block_type,
        )
    except httpx.HTTPStatusError as e:
        detail = e.response.text
        try:
            detail = e.response.json().get("message", detail)
        except Exception:
            pass
        print(f"Notion API error {e.response.status_code}: {detail}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
