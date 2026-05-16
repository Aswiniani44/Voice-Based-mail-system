# ==========================================================
# HOME.PY - NEON DASHBOARD UI (NO LOGIC CHANGE)
# ==========================================================

import streamlit as st
import utils


def show_home():

    # ---------------- APPLY GLOBAL UI ----------------
    utils.apply_neon_ui()

    # ---------------- PAGE PLACEHOLDER ----------------
    page = st.empty()

    with page.container():

        # ---------------- SESSION INIT ----------------
        if "home_initialized" not in st.session_state:
            st.session_state.home_initialized = False

        if "waiting_for_command" not in st.session_state:
            st.session_state.waiting_for_command = False


        # ---------------- UI STYLE ----------------
        st.markdown("""
        <style>

        .title{
            font-size:40px;
            font-weight:800;
            margin-bottom:10px;
            color:#00f7ff;
            text-shadow:
                0 0 10px #00f7ff,
                0 0 20px #00f7ff;
        }

        .subtitle{
            color:#a1a1aa;
            margin-bottom:25px;
        }

        .option-box{
            padding:16px;
            border-radius:14px;
            margin:12px;
            font-weight:700;
            border:1px solid rgba(168,85,247,0.4);
            background: rgba(168,85,247,0.08);
            box-shadow:0px 0px 15px rgba(168,85,247,0.3);
            transition:0.3s;
        }

        .option-box:hover{
            transform:scale(1.05);
            box-shadow:0px 0px 25px rgba(0,255,255,0.5);
        }

        </style>
        """, unsafe_allow_html=True)


        # ---------------- MAIN CARD ----------------
        st.markdown("""
        <div >
            <div class="title">Voice Dashboard</div>
            <div class="subtitle">Control your email using voice commands</div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")


        # ---------------- OPTIONS ----------------
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="option-box">🎤 Compose Mail</div>', unsafe_allow_html=True)
            st.markdown('<div class="option-box">📥 Read Mail</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="option-box">🗑 Delete Mail</div>', unsafe_allow_html=True)
            st.markdown('<div class="option-box">🚪 Logout</div>', unsafe_allow_html=True)

        st.write("")
        st.write("")


        # ---------------- VOICE INTRO ----------------
        if not st.session_state.home_initialized:

            utils.speak("Welcome to your dashboard")

            utils.speak(
                "Available options are compose mail, read mail, delete mail and logout"
            )

            st.session_state.home_initialized = True
            st.session_state.waiting_for_command = True


        # ---------------- VOICE COMMAND ----------------
        if st.session_state.waiting_for_command:

            command = utils.listen()

            if not command:

                utils.speak("I did not hear anything. Please say again.")
                st.rerun()

            command = command.lower()


            # ---------------- COMPOSE ----------------
            if "compose" in command:

                utils.speak("Opening compose mail")

                st.session_state.page = "compose"
                st.session_state.home_initialized = False
                st.session_state.waiting_for_command = False

                st.rerun()


            # ---------------- READ ----------------
            elif "read" in command:

                utils.speak("Opening read mail")

                st.session_state.page = "read"
                st.session_state.home_initialized = False
                st.session_state.waiting_for_command = False

                st.rerun()


            # ---------------- DELETE ----------------
            elif "delete" in command:

                utils.speak("Opening delete mail")

                st.session_state.page = "delete"
                st.session_state.home_initialized = False
                st.session_state.waiting_for_command = False

                st.rerun()


            # ---------------- LOGOUT ----------------
            elif "logout" in command or "log out" in command:

                utils.speak("Logging out")

                st.session_state.clear()
                st.session_state.page = "start"

                st.rerun()


            # ---------------- UNKNOWN ----------------
            else:

                utils.speak(
                    "Option not recognized. Please say compose mail, read mail, delete mail or logout"
                )

                st.rerun()