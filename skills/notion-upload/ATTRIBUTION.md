# Attribution

The core Notion upload logic in `scripts/notion_upload.py` is adapted from:

- **Source**: https://github.com/goonoo/mcp_notion_upload
- **File**: `mcp_notion_upload.py`
- **Author**: github.com/goonoo
- **License**: Not declared in upstream repo at time of import (2026-04-23).

## Changes from upstream

- Removed the `FastMCP` server wrapper; repackaged as a standalone CLI script invokable from a Claude Code skill.
- Converted from `async`/`httpx.AsyncClient` to sync `httpx.Client` (simpler for one-shot CLI use).
- Added `--block-type {auto,image,file}` with auto-detection via MIME type, so image uploads render inline as Notion `image` blocks instead of generic `file` blocks.
- Added PEP 723 inline dependency declaration so `uv run --script` bootstraps `httpx` automatically.
- Added mimetypes detection; passes the detected content-type to the upload multipart.
- Tightened error surfaces; consolidated the two upstream tools into a single upload-and-attach operation.

## Security note

Upstream script was reviewed before import. It only makes HTTPS calls to `api.notion.com` and Notion's S3 presigned upload URLs. No shell execution, subprocess use, pickling, or non-Notion network endpoints.
