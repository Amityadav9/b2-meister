"""Render PDF pages as PNG images for Streamlit display.

PDF text extraction and chunking are handled by Agno's PDFKnowledgeBase.
This module is only needed for visually showing the page alongside exercises.
"""
from __future__ import annotations

from pathlib import Path

import fitz


def render_page_png(pdf_path: Path, page_num: int, zoom: float = 2.0) -> bytes:
    doc = fitz.open(pdf_path)
    mat = fitz.Matrix(zoom, zoom)
    png = doc[page_num - 1].get_pixmap(matrix=mat).tobytes("png")
    doc.close()
    return png


def page_count(pdf_path: Path) -> int:
    doc = fitz.open(pdf_path)
    try:
        return len(doc)
    finally:
        doc.close()


def page_text(pdf_path: Path, page_num: int) -> str:
    doc = fitz.open(pdf_path)
    try:
        return doc[page_num - 1].get_text()
    finally:
        doc.close()
