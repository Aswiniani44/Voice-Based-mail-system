# ==========================================================
# APP.PY - NEON UI (NO LOGIC CHANGE)
# ==========================================================

import streamlit as st
import time
import start

from utils import speak, listen, smart_convert, is_valid_email, apply_neon_ui
import face_utils
from database import save_user, email_exists
import face_login
import home
import voice_compose
from voice_read import show_read_mail
from voice_delete import show_delete_mail


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Voice Mail System",
    page_icon="🎙",
    layout="centered"
)

# ==========================================================
# ⚡ NEON UI (FULL OVERRIDE)
# ==========================================================

st.markdown("""
<style>

/* DARK BASE */
html, body, [class*="css"]  {
    background-color: #0ffbf7 !important;
}

/* MAIN BACKGROUND */
.stApp{
    background: radial-gradient(circle at top,#0f172a,#020617,#000000) !important;
    background-size:400% 400%;
    animation:bgMove 15s ease infinite;
    color:white !important;
    font-family:'Segoe UI',sans-serif;
}

/* ANIMATION */
@keyframes bgMove{
    0%{background-position:0% 50%}
    50%{background-position:100% 50%}
    100%{background-position:0% 50%}
}

/* REMOVE DEFAULT */
header{visibility:hidden;}
footer{visibility:hidden;}

/* REMOVE SIDEBAR */
section[data-testid="stSidebar"]{
    display:none;
}

.block-container{
    padding-top:1rem;
    max-width:900px;
}

/* TITLE */
.header-title{
    font-size:48px;
    font-weight:900;
    text-align:center;
    margin-top:10px;
    letter-spacing:1px;
    color:#00008B;
    text-shadow:
        0 0 10px #00f7ff,
        0 0 20px #00f7ff;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HEADER
# ==========================================================

st.markdown("""
<div class="header-title">
Voice Based Mail System
</div>

""", unsafe_allow_html=True)
apply_neon_ui()
# ==========================================================
# SESSION INIT
# ==========================================================

if "page" not in st.session_state:
    st.session_state.page = "start"

# ==========================================================
# ROUTING (UNCHANGED)
# ==========================================================

if st.session_state.page == "start":

    start.show_start()


elif st.session_state.page == "register":

    st.title("🆕 Voice Registration")

    if "reg_step" not in st.session_state:
        st.session_state.reg_step = 0


    if st.session_state.reg_step == 0:

        speak("Please say your name")
        name = listen()

        if name == "":
            speak("I did not understand.")
            st.rerun()

        st.session_state.temp_name = name

        speak(f"You said {name}. Is this correct? Say please to confirm")

        st.session_state.reg_step = 1
        st.rerun()


    elif st.session_state.reg_step == 1:

        confirm = listen()

        if confirm and "confirm" in confirm.lower():
            st.session_state.reg_step = 2
            st.rerun()

        speak("Please say your name again")

        st.session_state.reg_step = 0
        st.rerun()


    elif st.session_state.reg_step == 2:

        speak("Please say your Gmail address")

        email_voice = listen()

        if email_voice == "":
            speak("I did not understand.")
            st.rerun()

        email = smart_convert(email_voice)

        if not is_valid_email(email):
            speak("Invalid Gmail address. Please say again.")
            st.rerun()

        st.session_state.temp_email = email

        speak(f"You said {email}. Is this correct? Say please to confirm")

        st.session_state.reg_step = 3
        st.rerun()


    elif st.session_state.reg_step == 3:

        confirm = listen()

        if confirm and "confirm" in confirm.lower():
            st.session_state.reg_step = 4
            st.rerun()

        speak("Please say your email again")

        st.session_state.reg_step = 2
        st.rerun()


    elif st.session_state.reg_step == 4:

        speak("Please say your password")

        password = listen()

        if password == "":
            speak("I did not understand.")
            st.rerun()

        st.session_state.temp_password = password

        speak("Is this password correct? Say please to confirm")

        st.session_state.reg_step = 5
        st.rerun()


    elif st.session_state.reg_step == 5:

        confirm = listen()

        if confirm and "confirm" in confirm.lower():
            st.session_state.reg_step = 6
            st.rerun()

        speak("Please say your password again")

        st.session_state.reg_step = 4
        st.rerun()


    elif st.session_state.reg_step == 6:

        speak("Please look at the camera for face capture")

        face = face_utils.capture_face()

        if face:

            st.session_state.face_data = face

            speak("Face captured successfully")

            st.session_state.reg_step = 7
            st.rerun()

        speak("Camera error. Please try again.")
        st.rerun()


    elif st.session_state.reg_step == 7:

        email = st.session_state.temp_email

        if email_exists(email):

            speak("This email is already registered.")
            speak("Please login using your face.")

            st.error("Email already registered")

            st.session_state.page = "login"
            st.rerun()

        save_user(
            st.session_state.temp_name,
            st.session_state.temp_email,
            st.session_state.temp_password,
            st.session_state.face_data
        )

        speak("Registration successful")

        time.sleep(2)

        st.session_state.page = "login"
        st.session_state.reg_step = 0
        st.rerun()


elif st.session_state.page == "login":

    face_login.show_login_page()


elif st.session_state.page == "home":

    home.show_home()


elif st.session_state.page == "compose":

    voice_compose.show_compose()


elif st.session_state.page == "read":

    show_read_mail()


elif st.session_state.page == "delete":

    show_delete_mail()