---
name: notion-upload
description: Upload a local file (image, PDF, doc, etc.) to a Notion page via the Notion API, creating a file or image block on the page and returning the download URL. Use this skill whenever the user wants to attach, upload, embed, or push a local file or image to a Notion page, even if they don't say "upload" explicitly — e.g. "put this screenshot in my Notion doc", "add report.pdf to my Notion page", "embed logo.png into Notion page 2785bbc…", or anytime a local file path appears alongside a Notion page ID or Notion page URL. Trigger aggressively when a file path and a Notion page reference co-occur.
---

# Notion Upload

Uploads a file to Notion and attaches it as a block on a page. Handles the full 3-step Notion file-upload flow (create upload → PUT bytes → attach to page) and returns a ready-to-use download URL.

## When this skill applies

- User gives a local file path plus a Notion page ID or Notion page URL.
- Phrases: "upload to Notion", "attach to my Notion page", "put this image in Notion", "add this to Notion doc <id>", "embed in Notion".
- Image files default to a Notion `image` block (renders inline); other files become `file` blocks.

## Prerequisites

- `NOTION_API_TOKEN` must be set in the environment. This is a Notion internal integration token (starts with `ntn_` or `secret_`). If missing, tell the user how to create one at https://www.notion.so/my-integrations and that the integration must be **invited to the target page** (Notion page → Share → Add connections).
- `uv` is recommended — the script uses PEP 723 inline deps, so `uv run --script` auto-installs `httpx` on first run. Falls back to plain `python3` if `httpx` is already installed.
- File must be ≤ 20 MB (Notion single-part upload limit).

## How to run it

Invoke the bundled script directly. Do not rewrite the upload logic inline — the script already handles errors, mime detection, block-type selection, and page-ID normalization.

Preferred (self-bootstrapping via `uv`):

```bash
uv run --script ~/.claude/skills/notion-upload/scripts/notion_upload.py \
  "<absolute_file_path>" \
  "<page_id_or_url_fragment>" \
  [--caption "optional caption"] \
  [--filename "display_name.ext"] \
  [--block-type auto|image|file]
```

Fallback if `uv` is unavailable but `httpx` is installed:

```bash
python3 ~/.claude/skills/notion-upload/scripts/notion_upload.py <file_path> <page_id> [...]
```

Arguments:
- `file_path` — absolute path to the local file.
- `page_id` — Notion page ID; dashes optional (`2785bbc0e5c281f4…` or `2785bbc0-e5c2-81f4-…`). If the user pastes a Notion URL, extract the 32-hex trailing segment.
- `--block-type auto` (default) picks `image` for image mimes and `file` otherwise. Override when the user explicitly wants one.

The script prints a JSON object on success:

```json
{
  "status": "success",
  "file_upload_id": "…",
  "file_block_id": "…",
  "block_type": "image",
  "download_url": "https://prod-files-secure.s3…",
  "expiry_time": "2026-04-23T…Z",
  "filename": "screenshot.png",
  "content_type": "image/png",
  "file_size": 284719
}
```

Parse that and surface `download_url`, `block_type`, and `file_block_id` to the user. Warn them `download_url` expires in ~1 hour; the file itself persists on the page indefinitely, and a fresh URL can be fetched by re-reading the block.

## Extracting a page ID from a Notion URL

Notion URLs look like `https://www.notion.so/workspace/Title-2785bbc0e5c281f48dfae9a48f53f6a6`. The last 32 hex characters are the page ID. Pass that directly; the script normalizes dashes.

## Common failure modes

- **401 / unauthorized**: token missing or wrong. Re-check `NOTION_API_TOKEN`.
- **404 on attach step**: the integration is not shared with the page. The user must open the page in Notion, click Share, and add the integration as a connection.
- **400 `body.children[0]…`**: page ID is malformed or points to a non-page (e.g. a database row URL). Confirm it's a page ID.
- **File too large**: split it, or compress images before upload.

## Multiple files

For several files, call the script once per file. Each call is independent; the page_id can be reused.

## Do not

- Do not echo the token into the terminal or into the JSON output.
- Do not attempt to upload files larger than 20 MB — stop and tell the user.
- Do not invent block types beyond `image` or `file` — Notion's file_upload attachment supports only those via this flow.
