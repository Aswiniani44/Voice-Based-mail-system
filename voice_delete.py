# ==========================================================
# voice_delete_mail.py - Delete Mail by Voice (NEON UI)
# ==========================================================

import streamlit as st
import imaplib
import email
from email.header import decode_header
from utils import speak, listen, apply_neon_ui


# ----------------------------------------------------------
# Decode Subject Safely
# ----------------------------------------------------------

def decode_text(text):

    if not text:
        return "Unknown"

    decoded, charset = decode_header(text)[0]

    if isinstance(decoded, bytes):

        try:
            return decoded.decode(charset or "utf-8")

        except:
            return decoded.decode("utf-8", errors="ignore")

    return decoded


# ----------------------------------------------------------
# MAIN PAGE
# ----------------------------------------------------------

def show_delete_mail():

    apply_neon_ui()   # ✅ Neon theme

    page = st.container()

    with page:

        # ---------------- UI STYLE ----------------

        st.markdown("""
        <style>

        .delete-title{
            text-align:center;
            font-size:36px;
            font-weight:800;
            color:#00f7ff;
            margin-bottom:20px;
            text-shadow:0 0 20px #00f7ff;
        }

        .mail-card{
            background: rgba(0,0,0,0.6);
            padding:20px;
            border-radius:12px;
            margin-bottom:15px;
            box-shadow:0px 0px 25px rgba(0,255,255,0.4);
            border:1px solid rgba(0,255,255,0.3);
        }

        .mail-from{
            font-weight:600;
            color:#00f7ff;
            font-size:18px;
        }

        .mail-subject{
            color:#9ca3af;
            margin-top:5px;
        }

        .voice-box{
            background: rgba(0,255,255,0.08);
            padding:12px;
            border-radius:10px;
            text-align:center;
            font-weight:600;
            margin-top:15px;
            border:1px solid rgba(0,255,255,0.3);
            color:#00f7ff;
            box-shadow:0 0 10px rgba(0,255,255,0.3);
        }

        </style>
        """, unsafe_allow_html=True)

        st.markdown(
            '<div class="delete-title">🗑 Delete Mail</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="voice-box">🎤 Say: Delete | Next | Home</div>',
            unsafe_allow_html=True
        )

        # ----------- CONTAINER FOR MAIL CARD (GHOST FIX) -----------

        mail_container = st.empty()

        user_email = st.session_state.get("user_email")
        user_password = st.session_state.get("user_password")

        if not user_email or not user_password:

            speak("Session expired. Please login again.")

            st.session_state.page = "login"
            st.rerun()

        try:

            # ---------------- CONNECT TO GMAIL ----------------

            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(user_email, user_password)
            mail.select("inbox")

            status, data = mail.search(None, "ALL")

            mail_ids = data[0].split()

            if not mail_ids:

                speak("Your inbox is empty.")
                go_home()
                return

            speak(f"You have {len(mail_ids)} emails in your inbox.")

            # Reverse order (latest first)
            mail_ids = mail_ids[::-1]

            # --------------------------------------------------
            # LOOP THROUGH EMAILS
            # --------------------------------------------------

            for email_id in mail_ids:

                status, msg_data = mail.fetch(email_id, "(RFC822)")

                for response_part in msg_data:

                    if isinstance(response_part, tuple):

                        msg = email.message_from_bytes(response_part[1])

                        sender = decode_text(msg.get("From"))
                        subject = decode_text(msg.get("Subject"))

                        # --------- RENDER MAIL CARD (GHOST FIX) ---------

                        speak(f"Email from {sender}")
                        speak(f"Subject {subject}")

                        speak("Say delete to delete this email. Say next to skip. Say home to return.")

                        command = listen()

                        if not command:

                            speak("Command not detected. Moving to next email.")
                            continue

                        command = command.lower()

                        # ---------------- DELETE ----------------

                        if "delete" in command:

                            try:

                                mail.copy(email_id, "[Gmail]/Trash")
                                mail.store(email_id, "-X-GM-LABELS", "\\Inbox")

                                speak("Email moved to trash")

                                st.success("Email deleted successfully")

                                speak("Moving to next email")

                                continue

                            except Exception as e:

                                st.error(str(e))
                                speak("Failed to delete email")

                        # ---------------- NEXT ----------------

                        elif "next" in command:

                            speak("Moving to next email.")
                            continue

                        # ---------------- HOME ----------------

                        elif "home" in command:

                            speak("Returning to dashboard.")
                            mail.logout()
                            go_home()
                            return

                        else:

                            speak("Command not recognized. Moving to next email.")

            mail.logout()

        except Exception as e:

            st.error(str(e))
            speak("There was an error accessing your mailbox.")

        go_home()


# ----------------------------------------------------------
# RETURN HOME
# ----------------------------------------------------------

def go_home():

    st.session_state.page = "home"
    st.rerun()