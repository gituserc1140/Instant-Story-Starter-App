import streamlit as st
import time
import requests

# Groq API endpoint and key
GROQ_API_URL = "https://api.groq.com/v1/generate"
GROQ_API_KEY = "your_groq_api_key_here"

# System prompt for the Groq API
SYSTEM_PROMPT = "You are the Instant Story Starter. Your job is to generate a single, vivid, atmospheric opening line for a story. The output must always be ONE sentence only. It should feel cinematic, intriguing, and full of potential. Do NOT write a paragraph. Do NOT continue the story. Do NOT explain anything. Just deliver one powerful first sentence that could begin a novel, short story, or scene."

# User prompt for the Groq API
USER_PROMPT = "Generate a single atmospheric opening line for a story."

# Initialize session state for cooldown
if 'last_request_time' not in st.session_state:
    st.session_state.last_request_time = 0

def generate_story_starter(genre=None, tone=None):
    user_prompt = USER_PROMPT
    if genre or tone:
        user_prompt += f" in the style of {genre if genre else ''} {tone if tone else ''}"

    response = requests.post(
        GROQ_API_URL,
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "system_prompt": SYSTEM_PROMPT,
            "user_prompt": user_prompt,
            "max_tokens": 50,
            "temperature": 0.7
        }
    )
    return response.json().get('generated_text', 'Error generating story starter.')

# Streamlit app
st.title("Instant Story Starter")
st.subheader("One click. One opening line.")

# Optional genre and tone dropdowns
col1, col2 = st.columns(2)
with col1:
    genre = st.selectbox("Genre", ["", "Mystery", "Sci-Fi", "Fantasy", "Romance"])
with col2:
    tone = st.selectbox("Tone", ["", "Surreal", "Dramatic", "Dark", "Whimsical"])

# Generate button with cooldown
if st.button("Generate Story Starter"):
    current_time = time.time()
    if current_time - st.session_state.last_request_time < 2:
        st.warning("Please wait a moment before generating another story starter.")
    else:
        st.session_state.last_request_time = current_time
        with st.spinner("Generating your story starter..."):
            story_starter = generate_story_starter(genre, tone)
        st.success(story_starter, icon="✨")
