import html
import os
import time

import streamlit as st
from groq import Groq

# ── Constants ──────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are the Instant Story Starter. Your job is to generate a single, vivid, "
    "atmospheric opening line for a story. The output must always be ONE sentence only. "
    "It should feel cinematic, intriguing, and full of potential. Do NOT write a paragraph. "
    "Do NOT continue the story. Do NOT explain anything. Just deliver one powerful first "
    "sentence that could begin a novel, short story, or scene."
)
BASE_USER_PROMPT = "Generate a single atmospheric opening line for a story."

GENRE_OPTIONS = ["Any", "Mystery", "Sci-Fi", "Fantasy", "Romance", "Horror", "Historical"]
TONE_OPTIONS  = ["Any", "Surreal", "Dramatic", "Dark", "Whimsical", "Melancholic", "Tense"]

GROQ_MODEL    = "llama-3.1-8b-instant"
COOLDOWN_SECS = 2

REPO_URL      = "https://github.com/gituserc1140/Instant-Story-Starter-App"
SPONSORS_URL  = "https://github.com/sponsors/gituserc1140"
STREAMLIT_URL = "https://streamlit.io/cloud"

# ── CSS ────────────────────────────────────────────────────────────────────────

_CSS = """
<style>
/* Page background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #0d0800 0%, #1a0e00 55%, #0d0600 100%);
    min-height: 100vh;
}
[data-testid="stHeader"] { background: transparent; }

/* Hero */
.hero {
    text-align: center;
    padding: 2.8rem 1rem 1.4rem;
}
.hero h1 {
    font-size: 2.7rem;
    font-weight: 800;
    background: linear-gradient(90deg, #f59e0b 0%, #ef4444 50%, #f59e0b 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
    margin-bottom: 0.3rem;
    animation: shimmer 4s linear infinite;
}
@keyframes shimmer {
    0%   { background-position: 0%   center; }
    100% { background-position: 200% center; }
}
.hero p {
    color: #d4a96a;
    font-size: 1.05rem;
    font-style: italic;
    margin-top: 0;
}

/* Story output card */
.story-card {
    background: rgba(245, 158, 11, 0.07);
    border: 1px solid rgba(245, 158, 11, 0.35);
    border-radius: 16px;
    padding: 1.8rem 2.2rem;
    color: #fef9ef;
    font-size: 1.2rem;
    line-height: 1.85;
    font-style: italic;
    text-align: center;
    margin-top: 1.4rem;
    box-shadow: 0 0 40px rgba(245, 158, 11, 0.07);
    word-break: break-word;
}
.story-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #f59e0b;
    text-align: center;
    margin-bottom: 0.5rem;
    margin-top: 1.4rem;
}

/* Error card */
.error-card {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.4);
    border-radius: 14px;
    padding: 1.2rem 1.6rem;
    color: #fca5a5;
    font-size: 0.97rem;
    margin-top: 1.2rem;
}

/* Generate button */
[data-testid="stButton"] button {
    background: linear-gradient(135deg, #d97706, #b45309) !important;
    color: #0d0800 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    width: 100% !important;
    transition: opacity 0.2s, transform 0.1s !important;
}
[data-testid="stButton"] button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* Labels */
label { color: #d4a96a !important; }

/* Selectbox text */
[data-testid="stSelectbox"] span { color: #fef3c7 !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(13, 8, 0, 0.94);
    border-right: 1px solid rgba(245, 158, 11, 0.18);
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div { color: #d4a96a !important; }
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #f59e0b !important; }

/* Link buttons in sidebar */
.sidebar-link {
    display: block;
    text-align: center;
    padding: 0.45rem 0.8rem;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 600;
    text-decoration: none !important;
    margin-bottom: 0.55rem;
    transition: opacity 0.2s;
    cursor: pointer;
}
.sidebar-link:hover { opacity: 0.8; }
.btn-github    { background: #21262d; color: #f0f6fc !important; border: 1px solid #30363d; }
.btn-sponsor   { background: #bf3989; color: #ffffff !important; border: 1px solid #a0306e; }
.btn-streamlit { background: #ff4b4b; color: #ffffff !important; border: 1px solid #d93d3d; }

/* Alerts */
[data-testid="stAlert"] p { color: #fef3c7 !important; }

/* Spinner */
[data-testid="stSpinner"] p { color: #f59e0b !important; }

/* Divider */
hr { border-color: rgba(245, 158, 11, 0.18) !important; }
</style>
"""


# ── Helpers ────────────────────────────────────────────────────────────────────

def get_preconfigured_api_key() -> str:
    """Return an API key from Streamlit secrets or environment, if available."""
    if "GROQ_API_KEY" in st.secrets:
        return st.secrets["GROQ_API_KEY"]
    return os.getenv("GROQ_API_KEY", "")


def build_user_prompt(genre: str, tone: str) -> str:
    """Append genre/tone qualifiers to the base user prompt if selected."""
    prompt = BASE_USER_PROMPT
    parts = []
    if genre and genre != "Any":
        parts.append(f"genre: {genre}")
    if tone and tone != "Any":
        parts.append(f"tone: {tone}")
    if parts:
        prompt += " (" + ", ".join(parts) + ")"
    return prompt


def call_groq(client: Groq, user_prompt: str) -> str:
    """Call the Groq chat completions API and return the story opening line."""
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt},
        ],
        model=GROQ_MODEL,
        max_tokens=120,
        temperature=0.82,
    )
    return response.choices[0].message.content.strip()


# ── App ────────────────────────────────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="Instant Story Starter",
        page_icon=":books:",
        layout="centered",
    )
    st.markdown(_CSS, unsafe_allow_html=True)

    # ── Hero ───────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="hero">
            <h1>Instant Story Starter</h1>
            <p>One click. One opening line.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Sidebar ────────────────────────────────────────────────────
    st.sidebar.header("Settings")

    api_key_input = st.sidebar.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Enter your Groq API key. Get one free at console.groq.com/keys",
    )

    stripped_key = api_key_input.strip()
    api_key = stripped_key if stripped_key else get_preconfigured_api_key()

    if not api_key:
        st.warning(
            "Enter your Groq API key in the sidebar to get started. "
            "Get a free key at console.groq.com/keys"
        )
        st.stop()

    st.sidebar.divider()

    # ── Sidebar link buttons ───────────────────────────────────────
    st.sidebar.markdown(
        f"""
        <a class="sidebar-link btn-github" href="{REPO_URL}" target="_blank" rel="noopener noreferrer">
            GitHub — View Source
        </a>
        <a class="sidebar-link btn-sponsor" href="{SPONSORS_URL}" target="_blank" rel="noopener noreferrer">
            GitHub Sponsors — Support
        </a>
        <a class="sidebar-link btn-streamlit" href="{STREAMLIT_URL}" target="_blank" rel="noopener noreferrer">
            Deploy on Streamlit Cloud
        </a>
        """,
        unsafe_allow_html=True,
    )

    # ── Session state ──────────────────────────────────────────────
    if "last_request_time" not in st.session_state:
        st.session_state.last_request_time = 0.0
    if "story_line" not in st.session_state:
        st.session_state.story_line = None
    if "story_error" not in st.session_state:
        st.session_state.story_error = None

    # Re-create client only when the key changes
    if st.session_state.get("groq_client_key") != api_key:
        st.session_state.groq_client = Groq(api_key=api_key)
        st.session_state.groq_client_key = api_key

    # ── Genre / Tone selectors ─────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        genre = st.selectbox("Genre (optional)", GENRE_OPTIONS)
    with col2:
        tone = st.selectbox("Tone (optional)", TONE_OPTIONS)

    st.write("")

    # ── Generate button ────────────────────────────────────────────
    if st.button("Generate Story Starter"):
        elapsed = time.time() - st.session_state.last_request_time
        if elapsed < COOLDOWN_SECS:
            wait = round(COOLDOWN_SECS - elapsed, 1)
            st.warning(f"Please wait {wait}s before generating again.")
        else:
            st.session_state.last_request_time = time.time()
            st.session_state.story_line  = None
            st.session_state.story_error = None
            user_prompt = build_user_prompt(genre, tone)
            with st.spinner("Crafting your opening line..."):
                try:
                    result = call_groq(st.session_state.groq_client, user_prompt)
                    st.session_state.story_line = result
                except Exception as exc:
                    st.session_state.story_error = str(exc)

    # ── Output ─────────────────────────────────────────────────────
    if st.session_state.story_error:
        st.markdown(
            f'<div class="error-card">Error: {html.escape(st.session_state.story_error)}</div>',
            unsafe_allow_html=True,
        )
    elif st.session_state.story_line:
        st.markdown('<div class="story-label">Opening Line</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="story-card">{html.escape(st.session_state.story_line)}</div>',
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
