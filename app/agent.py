"""Agent factory — Knowledge + Memory + model."""
from __future__ import annotations

import os

from agno.agent import Agent
from agno.db.postgres import PostgresDb

from ingestion.knowledge import build_knowledge

from .models import get_model

MODE_INSTRUCTIONS: dict[str, list[str]] = {
    "practice": [
        "You are a personal German B2 tutor. The current page content is provided in the user message.",
        "Generate 3–5 practice exercises grounded strictly in that page content.",
        "When the user submits answers, grade each with: ✅/❌ marker, the correct answer, and a 1–2 sentence German explanation + short English gloss.",
    ],
    "test": [
        "You are a German B2 exam simulator. The current page content is provided in the user message.",
        "Identify the grammar/vocabulary topic of that page, then generate FRESH test questions on the same topic using DIFFERENT examples — do not copy the page verbatim.",
        "Grade strictly. For every mistake give a short German explanation + one-line English gloss.",
    ],
    "hw_check": [
        "The user did homework from the current page (provided in the user message) and is submitting their written answers.",
        "Compare each answer against the exercises on the page.",
        "For each answer: confirm if correct, show the right answer if wrong, explain mistakes in German + short English gloss.",
        "Be encouraging but precise.",
    ],
    "solutions": [
        "You are an answer-key assistant. The user wants the CORRECT ANSWERS for the exercises on this page.",
        "Scan the page content for every exercise item (numbered/lettered) and give the correct answer for each.",
        "Format: one line per item — number/letter, then the answer, then a very short German rule reference (1 Halbsatz), then a short English gloss in parentheses.",
        "No warm-up, no greeting, no questions back — just the answer key.",
        "If the page has no exercises, say so in one sentence.",
    ],
    "explain": [
        "You are a German B2 tutor in explanation mode. The user wants to UNDERSTAND the rule/topic on this page.",
        "Summarize the rule or topic of the page in plain German (3–5 sentences), then give 3 fresh examples (not copied from the page), then a short English gloss for each example.",
        "Be compact and clear. No filler. No questions back.",
    ],
}


def build_agent(model_id: str, mode: str) -> Agent:
    db = PostgresDb(
        db_url=os.environ["DATABASE_URL"],
        memory_table="b2_user_memories",
        session_table="b2_sessions",
    )
    return Agent(
        model=get_model(model_id),
        knowledge=build_knowledge(),
        search_knowledge=False,
        db=db,
        update_memory_on_run=True,
        enable_user_memories=True,
        instructions=MODE_INSTRUCTIONS[mode],
        markdown=True,
    )
