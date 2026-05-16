# ==========================================================
# voice_compose.py - NEON VOICE COMPOSE UI
# ==========================================================

import streamlit as st
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils import speak, listen, smart_convert, listen_long, apply_neon_ui


def show_compose():

    apply_neon_ui()   # ✅ Neon theme

    page = st.container()

    with page:

        # ------------------------------------------------------
        # GET LOGIN DETAILS
        # ------------------------------------------------------

        from_email = st.session_state.get("user_email")
        from_password = st.session_state.get("user_password")

        if not from_email or not from_password:
            speak("Session expired. Please login again.")
            st.session_state.page = "login"
            st.rerun()

        # ------------------------------------------------------
        # UI STYLE
        # ------------------------------------------------------

        st.markdown("""
        <style>

        .title{
            font-size:40px;
            font-weight:900;
            margin-bottom:10px;
            color:#00f7ff;
            text-shadow:0 0 20px #00f7ff;
        }

        .subtitle{
            color:#9ca3af;
            margin-bottom:20px;
        }

        .preview-box{
            background: rgba(0,0,0,0.6);
            padding:20px;
            border-radius:15px;
            border:1px solid rgba(0,255,255,0.3);
            margin-top:20px;
            text-align:left;
            color:#e5e7eb;
            box-shadow:0 0 15px rgba(0,255,255,0.3);
        }

        </style>
        """, unsafe_allow_html=True)

        # ------------------------------------------------------
        # HEADER UI
        # ------------------------------------------------------

        st.markdown("""
        <div>
            <div class="title">Voice Compose</div>
            <div class="subtitle">Speak recipient, subject and message</div>
        </div>
        """, unsafe_allow_html=True)

        speak("Voice compose started.")

        # ======================================================
        # RECIPIENT EMAIL
        # ======================================================

        while True:

            speak("Who are the recipients? You can say multiple emails separated by and.")

            recipient_voice = listen()

            if not recipient_voice:
                speak("I did not hear any email. Please say the email again.")
                continue

            converted = smart_convert(recipient_voice)

            raw_emails = re.split(r",| and ", converted)

            recipients = [email.strip() for email in raw_emails if email.strip()]

            valid_emails = []

            for email in recipients:
                if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    valid_emails.append(email)

            if not valid_emails:
                speak("That email is not valid. Please say the email again.")
                continue

            speak(f"You said {', '.join(valid_emails)}. Is this correct? Say please to confirm or say no to repeat.")

            confirm = listen()

            if confirm and ("please" in confirm or "yes" in confirm):
                break

            elif confirm and "no" in confirm:
                speak("Okay, please say the email again.")

            else:
                speak("Please say please to confirm or say no to repeat.")

        # ======================================================
        # SUBJECT
        # ======================================================

        while True:

            speak("What is the subject?")

            subject = listen()

            if not subject:
                speak("I did not hear the subject. Please say again.")
                continue

            speak(f"You said {subject}. Is this correct? Say please to confirm.")

            confirm = listen()

            if confirm and ("please" in confirm or "yes" in confirm):
                break

            speak("Okay please say the subject again.")

        # ======================================================
        # BODY
        # ======================================================

        while True:

            speak("What is the message?")

            body = listen_long()

            if not body:
                speak("I did not hear the message. Please say again.")
                continue

            speak("You said the following message.")
            speak(body)

            speak("Is this correct? Say please to confirm or say no to repeat.")

            confirm = listen()

            if confirm and ("please" in confirm or "yes" in confirm):
                break

            speak("Okay please say the message again.")

        # ======================================================
        # MAIL PREVIEW UI
        # ======================================================

        st.markdown(f"""
        <div class="preview-box">

        <b>From:</b> {from_email} <br><br>

        <b>To:</b> {", ".join(valid_emails)} <br><br>

        <b>Subject:</b> {subject} <br><br>

        <b>Message:</b> {body}

        </div>
        """, unsafe_allow_html=True)

        # ======================================================
        # SEND CONFIRMATION
        # ======================================================

        speak(f"You are sending mail to {len(valid_emails)} recipients. Say please to send or say cancel.")

        confirm = listen()

        if not confirm or ("cancel" in confirm):
            speak("Mail cancelled.")
            go_home()
            return

        if "please" not in confirm and "yes" not in confirm:
            speak("Mail cancelled.")
            go_home()
            return

        # ======================================================
        # SEND EMAIL
        # ======================================================

        try:

            msg = MIMEMultipart()

            msg["From"] = from_email
            msg["To"] = ", ".join(valid_emails)
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:

                server.starttls()

                server.login(from_email, from_password)

                server.sendmail(from_email, valid_emails, msg.as_string())

            st.success("✅ Email Sent Successfully")

            speak("Email sent successfully.")

        except Exception as e:

            st.error(f"Error: {str(e)}")

            speak("There was an error sending the email.")

        go_home()


# ======================================================
# RETURN HOME
# ======================================================

def go_home():

    speak("Returning to dashboard.")

    st.session_state.page = "home"

    st.rerun()