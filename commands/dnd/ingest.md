---
name: "dnd:ingest"
description: "Ingest D&D source material into the RAG vector database. Copies files to the NUC, runs the chunking/embedding pipeline, and verifies results. Use when adding new books, PDFs, or text files to the knowledge base."
---

# /dnd:ingest — Source Material Ingestion

Ingest D&D source material (PDFs or plain text) into the Qdrant vector database on the home server NUC. Handles file transfer, chunking, embedding, and verification.

## Input

$ARGUMENTS — one of:
- A file path to ingest (e.g., `/path/to/book.pdf` or a vault path)
- `status` — show what's been ingested
- `search {query}` — test search the vector DB

If no arguments, ask what file to ingest.

## Setup

1. Read RAG config: `~/docs/Documents/2. Areas/2.2 Dungeons & Dragons/_Config/RAG Config.md`
2. Verify NUC is reachable: `ssh -o ConnectTimeout=5 jared@192.168.0.211 "echo ok"`
3. Verify Qdrant is running: `curl -s http://192.168.0.211:6333/healthz`

If NUC or Qdrant unreachable, report the issue and stop.

## Infrastructure Details

- **NUC:** `192.168.0.211` (SSH as `jared`)
- **Qdrant:** `http://192.168.0.211:6333`, collection `dnd-source-material`
- **Pipeline:** `/home/jared/dnd-rag/` on NUC
- **Venv:** `/home/jared/dnd-rag/.venv/`
- **Pipeline source:** `/home/jared/dev/dnd-rag/` (local)

## Workflows

### Ingest a File

1. **Resolve the file path**
   - If path is relative to the vault, resolve against `~/docs/Documents/`
   - If path is in `7. Source Material/`, use the full vault path
   - Verify the file exists locally

2. **Ask for the book title**
   - Use AskUserQuestion: "What's the book title for this source material?"
   - This becomes the `--book` parameter and the `book` metadata field in Qdrant

3. **Sync pipeline updates** (in case local code changed)
   ```bash
   rsync -av --exclude='.venv' --exclude='__pycache__' --exclude='*.pyc' \
     /home/jared/dev/dnd-rag/ jared@192.168.0.211:~/dnd-rag/
   ```

4. **Copy the source file to NUC**
   ```bash
   scp "{file_path}" jared@192.168.0.211:~/dnd-rag/books/
   ```

5. **Dry run first** — show chunk breakdown without uploading
   ```bash
   ssh jared@192.168.0.211 "cd ~/dnd-rag && source .venv/bin/activate && \
     python ingest.py ingest 'books/{filename}' --book '{book_title}' --dry-run"
   ```

   Present the chunk summary table to the user. Ask if they want to proceed with the full ingest.

6. **Full ingest** — embed and upload
   ```bash
   ssh jared@192.168.0.211 "cd ~/dnd-rag && source .venv/bin/activate && \
     python ingest.py ingest 'books/{filename}' --book '{book_title}'"
   ```

7. **Verify with a test search**
   - Pick a distinctive term from the book (a location name, NPC, or creature)
   - Run a search to confirm results come back with correct book metadata
   ```bash
   ssh jared@192.168.0.211 "cd ~/dnd-rag && source .venv/bin/activate && \
     python ingest.py search '{test_query}' --limit 3"
   ```

8. **Update RAG Config**
   - Edit `_Config/RAG Config.md` — add a row to the Ingested Books table with:
     - Book name, source type (PDF/text + size), chunk count, breakdown by type, date

### Status

Show current state of the RAG system:

1. Check Qdrant health: `curl -s http://192.168.0.211:6333/healthz`
2. Get collection info: `curl -s http://192.168.0.211:6333/collections/dnd-source-material`
3. Read `_Config/RAG Config.md` for the ingested books table
4. Present: health status, total vectors, books ingested, chunk breakdown

### Search

Test the vector database with a query:

1. Run search on NUC:
   ```bash
   ssh jared@192.168.0.211 "cd ~/dnd-rag && source .venv/bin/activate && \
     python ingest.py search '{query}' --limit {limit} {--type filter if specified}"
   ```
2. Present results with scores, content types, and text previews

## Supported File Types

| Extension | Extractor | Notes |
|-----------|-----------|-------|
| `.pdf` | PyMuPDF (`pdf_extractor.py`) | Best with formatted PDFs — uses font info for heading detection |
| `.txt`, `.md`, no extension | Text extractor (`text_extractor.py`) | Pattern-based heading detection, works with plain text dumps |

## Chunking Pipeline

Chunks are created in this priority order (each chunker consumes matched blocks):

1. **Stat blocks** — creature stat blocks (AC/HP/Speed pattern)
2. **Spells** — spell descriptions (level/school pattern)
3. **Items** — magic items (type + rarity pattern)
4. **DM notes** — read-aloud text, DM guidance sections
5. **Rules** — mechanical rules text (DC references, saving throws)
6. **Narrative** — everything remaining, split at heading boundaries with 500-token chunks

## Error Handling

- **NUC unreachable:** "Can't reach the NUC at 192.168.0.211. Is it powered on and on the same network?"
- **Qdrant down:** "Qdrant is not responding. Check with: `ssh jared@192.168.0.211 'docker ps | grep qdrant'`"
- **File not found:** Verify the path and suggest looking in `7. Source Material/`
- **Ingest fails:** Show the error output, suggest `--dry-run` to debug chunking
