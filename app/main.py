"""b2-meister — Streamlit UI."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st  # noqa: E402
from dotenv import load_dotenv  # noqa: E402

load_dotenv()

from app.agent import build_agent  # noqa: E402
from app.models import all_models, default_model_id  # noqa: E402
from ingestion.extract import page_count, page_text, render_page_png  # noqa: E402

PDF_DIR = Path(__file__).resolve().parent.parent / "pdfs"
USER_ID = "amit"

MODE_LABELS = {
    "practice": "📝 Practice",
    "test": "🧪 Test",
    "hw_check": "✅ HW Check",
    "solutions": "🔑 Lösungen",
    "explain": "📖 Erklären",
}

MODE_HINTS = {
    "practice": "Tippe **„Start“** für Übungen zu dieser Seite, oder stell eine gezielte Frage.",
    "test": "Tippe **„Gib mir 5 Testfragen zu dieser Seite“**.",
    "hw_check": "Tippe deine Antworten aus dem Heft (z. B. „1. ging, 2. hat gesagt, …“).",
    "solutions": "Tippe **„Lösungen“** — der Agent gibt dir die richtigen Antworten für alle Übungen auf dieser Seite.",
    "explain": "Tippe **„Erkläre“** oder frag gezielt nach einer Regel auf dieser Seite.",
}

st.set_page_config(page_title="b2-meister", layout="wide")

# ───────────────── Sidebar ─────────────────
with st.sidebar:
    st.title("⚙️ b2-meister")

    models = all_models()
    model_keys = list(models.keys())
    default_idx = model_keys.index(default_model_id()) if default_model_id() in model_keys else 0
    model_id = st.selectbox(
        "Model", options=model_keys, index=default_idx, format_func=lambda k: models[k]
    )

    pdfs = {p.stem: p for p in sorted(PDF_DIR.glob("*.pdf"))}
    pdf_choice = st.selectbox("PDF", list(pdfs))
    pdf_path = pdfs[pdf_choice]

    total = page_count(pdf_path)
    page = st.number_input("Seite", min_value=1, max_value=total, value=1, step=1)

    mode = st.radio("Modus", list(MODE_LABELS), format_func=lambda m: MODE_LABELS[m])

    if st.button("🗑️ Chat zurücksetzen"):
        st.session_state.pop("messages", None)
        st.session_state.pop("chat_key", None)
        st.rerun()

# ───────────────── Main ─────────────────
col_pdf, col_chat = st.columns([1, 1], gap="large")

with col_pdf:
    st.image(render_page_png(pdf_path, int(page)), caption=f"{pdf_choice} — Seite {page}")

with col_chat:
    st.subheader(f"{MODE_LABELS[mode]} · Seite {page}")

    chat_key = f"{model_id}|{pdf_choice}|{page}|{mode}"
    if st.session_state.get("chat_key") != chat_key:
        st.session_state.chat_key = chat_key
        st.session_state.messages = []

    if not st.session_state.messages:
        st.info(MODE_HINTS[mode])

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    @st.cache_resource(show_spinner=False)
    def _get_agent(model_id: str, mode: str):
        return build_agent(model_id, mode)

    if prompt := st.chat_input("Frage oder Antwort …"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        current_page = page_text(pdf_path, int(page)).strip()
        context = (
            f"[Kontext: Quelle='{pdf_choice}', Seite={page}, Modus={mode}]\n"
            f"Arbeite AUSSCHLIESSLICH mit dem folgenden Seiteninhalt. "
            f"Nutze die Wissensdatenbank nur, wenn Grammatikregeln zur Erklärung fehlen.\n\n"
            f"--- SEITENINHALT (Seite {page}) ---\n{current_page}\n--- ENDE SEITENINHALT ---\n\n"
            f"Nutzer-Eingabe: {prompt}"
        )
        with st.chat_message("assistant"):
            with st.spinner("Denke nach …"):
                agent = _get_agent(model_id, mode)
                response = agent.run(context, user_id=USER_ID)
                answer = response.content or "_(keine Antwort)_"
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})
