# ==========================================================
# FACE_LOGIN.PY - Secure Face Authentication (Auto Recapture)
# ==========================================================

import streamlit as st
import pickle
import face_recognition

from database import fetch_all_users
from face_utils import capture_face
from utils import speak, listen, smart_convert, apply_neon_ui


def show_login_page():

    st.empty()   # Ghost text fix

    # ------------------------------------------------------
    # UI STYLE
    # ------------------------------------------------------

    st.markdown("""
    <style>

    .login-title{
        text-align:center;
        font-size:34px;
        font-weight:700;
        color:#1e3a8a;
        margin-bottom:15px;
    }

    .login-sub{
        text-align:center;
        color:#475569;
        margin-bottom:20px;
    }

    .scan-box{
        background:white;
        padding:25px;
        border-radius:15px;
        text-align:center;
        box-shadow:0px 8px 25px rgba(0,0,0,0.15);
        margin-bottom:20px;
    }

    .voice-box{
        background:#f199ff;
        padding:12px;
        border-radius:10px;
        text-align:center;
        font-weight:600;
        margin-bottom:20px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="login-title">🔐 Face Login</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-sub">Authenticate using face recognition</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="voice-box">📷 Please look at the camera for face authentication</div>',
        unsafe_allow_html=True
    )

    speak("Please look at the camera for face login")

    # ------------------------------------------------------
    # CAPTURE FACE (AUTO RETRY)
    # ------------------------------------------------------

    while True:

        captured_binary = capture_face()

        if captured_binary is None:

            speak("Face capture failed. Please look at the camera again.")

            st.warning("Face not detected. Trying again...")

            continue

        break

    captured_encoding = pickle.loads(captured_binary)

    speak("Matching your face with database")

    users = fetch_all_users()

    matched_accounts = []

    # ------------------------------------------------------
    # FACE MATCHING
    # ------------------------------------------------------

    for user in users:

        user_id, name, email, password, encoding_blob = user

        stored_encoding = pickle.loads(encoding_blob)

        distance = face_recognition.face_distance(
            [stored_encoding],
            captured_encoding
        )[0]

        # Strict threshold
        if distance < 0.45:

            matched_accounts.append({
                "email": email,
                "password": password
            })

    # ------------------------------------------------------
    # NO MATCH
    # ------------------------------------------------------

    if len(matched_accounts) == 0:

        speak("Face not recognized")

        speak("You are not registered. Please register first.")

        st.error("User not registered")

        st.session_state.page = "register"

        st.rerun()

    # ------------------------------------------------------
    # SINGLE ACCOUNT
    # ------------------------------------------------------

    if len(matched_accounts) == 1:

        account = matched_accounts[0]

        st.session_state["user_email"] = account["email"]
        st.session_state["user_password"] = account["password"]

        speak("Face recognized. Logging you in.")

        st.success(f"Logged in as {account['email']}")

        st.session_state.page = "home"

        st.rerun()

    # ------------------------------------------------------
    # MULTIPLE EMAILS
    # ------------------------------------------------------

    speak("Multiple accounts found")

    for acc in matched_accounts:
        speak(acc["email"])

    while True:

        speak("Please say the email you want to login")

        voice_email = listen()

        if not voice_email:

            speak("I did not hear anything. Please say again.")
            continue

        email_text = smart_convert(voice_email)

        speak(f"You said {email_text}. Is this correct? Say confirm.")

        confirm = listen()

        if confirm and ("confirm" in confirm or "S" in confirm):

            for acc in matched_accounts:

                if acc["email"] == email_text:

                    st.session_state["user_email"] = acc["email"]
                    st.session_state["user_password"] = acc["password"]

                    speak("Login successful")

                    st.success(f"Logged in as {acc['email']}")

                    st.session_state.page = "home"

                    st.rerun()

            speak("This email does not match the detected accounts")

        elif confirm and "no" in confirm:

            speak("Okay, say the email again")

        