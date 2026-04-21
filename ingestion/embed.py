"""Ingest all PDFs in pdfs/ into pgvector.

Run:  uv run python -m ingestion.embed
"""
from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv

from .knowledge import build_knowledge

load_dotenv()

PDF_DIR = Path(__file__).resolve().parent.parent / "pdfs"


def main() -> None:
    kb = build_knowledge()
    for pdf in sorted(PDF_DIR.glob("*.pdf")):
        print(f"→ ingesting {pdf.name}")
        kb.insert(path=str(pdf), name=pdf.stem, skip_if_exists=True)
    print("done.")


if __name__ == "__main__":
    main()
