# Instant Story Starter

> One click. One opening line.

A lightweight Streamlit micro-app that generates a single cinematic, atmospheric opening line for a story — powered by the [Groq API](https://console.groq.com).

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://instant-story-starter-app-keqvpwmgp3rvgbe53tzuxl.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-View%20Source-21262d?logo=github)](https://github.com/gituserc1140/Instant-Story-Starter-App)
[![GitHub Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-Support-bf3989?logo=github-sponsors)](https://github.com/sponsors/gituserc1140)

---

## What It Does

Every click sends a request to the Groq API and returns **one powerful sentence** that could open a novel, short story, or scene. The output is always a single line — cinematic, intriguing, and full of narrative potential.

Optional genre and tone selectors let you steer the style of the opening line.

---

## Features

- Single atmospheric opening line generated per click
- Genre selector: Mystery, Sci-Fi, Fantasy, Romance, Horror, Historical
- Tone selector: Surreal, Dramatic, Dark, Whimsical, Melancholic, Tense
- API key entered directly in the app — no configuration files needed
- 2-second cooldown to prevent accidental spam
- Amber-on-dark color scheme designed for creative focus
- Clean, minimal interface — no clutter, no distractions

---

## Getting a Groq API Key

1. Go to [console.groq.com/keys](https://console.groq.com/keys)
2. Sign in or create a free account
3. Click **Create API Key** and copy the key
4. Paste the key into the sidebar when you launch the app

Groq provides a generous free tier — no credit card required to start.

---

## Local Setup

**Prerequisites:** Python 3.9 or later

```bash
# 1. Clone the repository
git clone https://github.com/gituserc1140/Instant-Story-Starter-App.git
cd Instant-Story-Starter-App

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## Deploy on Streamlit Community Cloud

1. Fork this repository to your GitHub account
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) and sign in with GitHub
3. Click **New app**, select your fork, and set the main file to `app.py`
4. Click **Deploy**

To pre-configure the API key without exposing it, add a Streamlit secret:

```toml
# .streamlit/secrets.toml  (do not commit this file)
GROQ_API_KEY = "gsk_your_key_here"
```

---

## How to Use

1. Enter your Groq API key in the sidebar
2. Optionally select a **Genre** and/or **Tone**
3. Click **Generate Story Starter**
4. Read the opening line that appears
5. Click again for a new one

Each click is a fresh generation — no two lines will be the same.

---

## Support

If you find this useful, consider [sponsoring on GitHub](https://github.com/sponsors/gituserc1140).

---

## License

MIT
