"""Model registry + factory. Prefix IDs with `groq:` or `ollama:`."""
from __future__ import annotations

import os

from agno.models.groq import Groq
from agno.models.ollama import Ollama

GROQ_MODELS: dict[str, str] = {
    "qwen/qwen3-32b": "Qwen3 32B — fast, strong German",
    "openai/gpt-oss-120b": "GPT-OSS 120B — deep accuracy",
    "meta-llama/llama-4-scout-17b-16e-instruct": "Llama 4 Scout 17B — long outputs",
}

OLLAMA_MODELS: dict[str, str] = {
    "qwen3.5:latest": "Qwen3.5 local (6.6 GB)",
    "qwen3:latest": "Qwen3 local (5.2 GB)",
    "gemma4:latest": "Gemma4 local (9.6 GB)",
}


def all_models() -> dict[str, str]:
    return {
        **{f"groq:{k}": f"☁️  {v}" for k, v in GROQ_MODELS.items()},
        **{f"ollama:{k}": f"🖥️  {v}" for k, v in OLLAMA_MODELS.items()},
    }


def get_model(model_id: str):
    provider, _, name = model_id.partition(":")
    if provider == "groq":
        return Groq(id=name)
    if provider == "ollama":
        return Ollama(
            id=name,
            host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
        )
    raise ValueError(f"Unknown model provider in '{model_id}' (use 'groq:' or 'ollama:')")


def default_model_id() -> str:
    return os.environ.get("DEFAULT_MODEL", "groq:qwen/qwen3-32b")
