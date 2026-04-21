"""Agno knowledge factory — single source of truth for ingestion + retrieval."""
from __future__ import annotations

import os

from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector.pgvector import PgVector


def build_knowledge(table_name: str = "b2_chunks") -> Knowledge:
    return Knowledge(
        name="b2-meister",
        max_results=5,
        vector_db=PgVector(
            table_name=table_name,
            db_url=os.environ["DATABASE_URL"],
            embedder=OllamaEmbedder(
                id=os.environ["EMBED_MODEL"],
                host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
                dimensions=768,
            ),
        ),
    )
