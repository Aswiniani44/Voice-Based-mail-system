# ==========================================================
# START.PY - Voice Start Page (NEON UI - FULL FIXED)
# ==========================================================

import streamlit as st
import time
from utils import speak, listen, apply_neon_ui


def show_start():

    # ---------------- APPLY GLOBAL UI ----------------
    apply_neon_ui()

    # ---------------- SESSION INIT ----------------
    if "step" not in st.session_state:
        st.session_state.step = 0

    if "user_choice" not in st.session_state:
        st.session_state.user_choice = ""

    # =====================================================
    # STEP 0 → Welcome
    # =====================================================

    if st.session_state.step == 0:

        speak("Welcome to Voice Based Mail System")

        time.sleep(1)

        speak("Are you a new user or registered user?")

        st.session_state.step = 1

        st.rerun()

    # =====================================================
    # STEP 1 → Listen user choice (WITH RETRY)
    # =====================================================

    elif st.session_state.step == 1:

        retry = 0
        max_retry = 3

        while retry < max_retry:

            user_input = listen()

            if not user_input:
                speak("I did not hear anything. Please say new user or registered user.")
                retry += 1
                continue

            user_input = user_input.lower()

            if "new" in user_input:
                st.session_state.user_choice = "new user"
                break

            elif "register" in user_input:
                st.session_state.user_choice = "registered user"
                break

            else:
                speak("Please say new user or registered user.")
                retry += 1

        if retry == max_retry:
            speak("Going back to start")
            st.session_state.step = 0
            st.rerun()

        speak(f"You said {st.session_state.user_choice}. Say confirm to continue or say no to repeat.")

        st.session_state.step = 2
        st.rerun()

    # =====================================================
    # STEP 2 → Confirmation (WITH RETRY)
    # =====================================================

    elif st.session_state.step == 2:

        retry = 0
        max_retry = 3

        while retry < max_retry:

            confirm = listen()

            if not confirm:
                speak("I did not hear anything. Please say confirm or no.")
                retry += 1
                continue

            confirm = confirm.lower()

            # ---------- CONFIRM ----------
            if "confirm" in confirm:

                if st.session_state.user_choice == "new user":
                    st.session_state.page = "register"
                else:
                    st.session_state.page = "login"

                st.session_state.step = 0
                st.rerun()

            # ---------- REPEAT ----------
            elif "no" in confirm:

                speak("Okay. Please say again.")
                st.session_state.step = 1
                st.rerun()

            else:

                speak("Please say confirm or no.")
                retry += 1

        # AFTER MAX RETRIES
        speak("Going back to start")
        st.session_state.step = 0
        st.rerun()