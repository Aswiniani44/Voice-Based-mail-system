# ==========================================================
# UTILS.PY - Voice Engine + Email Conversion + Validation
# (NEON UI + BACKGROUND FIX - FINAL)
# ==========================================================

import base64
import io
import re
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import streamlit as st


# ==========================================================
# ⚡ NEON UI FUNCTION (FINAL WORKING)
# ==========================================================

def apply_neon_ui():

    try:
        with open("bg.png", "rb") as f:
            img = base64.b64encode(f.read()).decode()
    except:
        return  # if image missing, skip UI (avoid crash)

    st.markdown(f"""
    <style>

    /* MAIN BACKGROUND */
    [data-testid="stAppViewContainer"] {{
        background: url("data:image/png;base64,{img}") no-repeat center center fixed;
        background-size: cover;
    }}

    /* REMOVE HEADER BG */
    [data-testid="stHeader"] {{
        background: transparent;
    }}

    /* DARK OVERLAY */
    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.6);
        z-index: -1;
    }}

    /* REMOVE WHITE BLOCK */
    .block-container {{
        background: transparent;
    }}

    /* OPTIONAL SIDEBAR */
    [data-testid="stSidebar"] {{
        background: rgba(0,0,0,0.5);
    }}

    </style>
    """, unsafe_allow_html=True)


# ==========================================================
# EMAIL VALIDATION
# ==========================================================

def is_valid_email(email):

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


# ==========================================================
# TEXT TO SPEECH
# ==========================================================

def speak(text):

    if text is None:
        return

    text = str(text).strip()

    if text == "":
        return

    try:

        st.markdown(f"""
        <div style="
            background:rgba(0,255,255,0.05);
            padding:12px;
            border-radius:12px;
            border-left:4px solid #00f7ff;
            margin-bottom:8px;
            box-shadow:0 0 10px rgba(0,255,255,0.3);">
            🤖 {text}
        </div>
        """, unsafe_allow_html=True)

        tts = gTTS(text=text, lang="en")

        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)

        audio = AudioSegment.from_file(fp, format="mp3")
        play(audio)

    except Exception as e:

        st.error(f"Voice Error: {e}")


# ==========================================================
# SPEECH TO TEXT
# ==========================================================

def listen():

    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 1.5

    try:

        with sr.Microphone() as source:

            st.markdown("""
            <div style="
            background:rgba(0,255,255,0.08);
            padding:12px;
            border-radius:12px;
            border:1px solid #00f7ff;
            text-align:center;
            box-shadow:0 0 15px rgba(0,255,255,0.4);">
            🎤 Listening...
            </div>
            """, unsafe_allow_html=True)

            recognizer.adjust_for_ambient_noise(source, duration=1)

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=30
            )

        text = recognizer.recognize_google(audio)

        st.markdown(f"""
        <div style="
        background:rgba(168,85,247,0.08);
        padding:12px;
        border-radius:12px;
        border-left:4px solid #a855f7;
        box-shadow:0 0 10px rgba(168,85,247,0.4);">
        🗣 {text}
        </div>
        """, unsafe_allow_html=True)

        return text.lower()

    except sr.WaitTimeoutError:
        st.warning("No speech detected")
        return ""

    except sr.UnknownValueError:
        st.warning("Could not understand")
        return ""

    except OSError:
        st.error("🎤 Microphone not available")
        return ""

    except Exception as e:
        st.error(f"Mic Error: {e}")
        return ""


# ==========================================================
# SMART EMAIL CONVERTER
# ==========================================================

def smart_convert(text):

    if not text:
        return ""

    text = text.lower()

    replacements = {
        " at ": "@",
        " dot ": ".",
        " underscore ": "_",
        " dash ": "-",
        " hyphen ": "-",
        " point ": "."
    }

    for key, value in replacements.items():
        text = text.replace(key, value)

    text = text.replace(" dotcom", ".com")
    text = text.replace(" dotorg", ".org")
    text = text.replace(" dotedu", ".edu")
    text = text.replace(" dotin", ".in")

    text = text.replace(" ", "")

    return text


# ==========================================================
# LONG LISTEN (FOR EMAIL BODY)
# ==========================================================

def listen_long():

    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 2

    try:

        with sr.Microphone() as source:

            st.markdown("""
            <div style="
            background:rgba(0,255,255,0.08);
            padding:12px;
            border-radius:12px;
            border:1px solid #00f7ff;
            text-align:center;
            box-shadow:0 0 15px rgba(0,255,255,0.4);">
            🎤 Listening for message...
            </div>
            """, unsafe_allow_html=True)

            recognizer.adjust_for_ambient_noise(source, duration=1)

            audio = recognizer.listen(
                source,
                timeout=20,
                phrase_time_limit=60
            )

        text = recognizer.recognize_google(audio)

        st.markdown(f"""
        <div style="
        background:rgba(168,85,247,0.08);
        padding:12px;
        border-radius:12px;
        border-left:4px solid #a855f7;
        box-shadow:0 0 10px rgba(168,85,247,0.4);">
        🗣 {text}
        </div>
        """, unsafe_allow_html=True)

        return text.lower()

    except sr.WaitTimeoutError:
        st.warning("No speech detected")
        return ""

    except sr.UnknownValueError:
        st.warning("Could not understand")
        return ""

    except OSError:
        st.error("🎤 Microphone not available")
        return ""

    except Exception as e:
        st.error(f"Mic Error: {e}")
        return ""