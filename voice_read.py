# ==========================================================
# voice_read.py - FINAL (ALL FEATURES COMPLETE)
# ==========================================================

import streamlit as st
import imaplib
import email
import re
import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from utils import speak, listen, smart_convert, apply_neon_ui


# ==========================================================
# 🔢 NUMBER EXTRACTOR
# ==========================================================

def extract_number(text):

    if not text:
        return None

    text = text.lower()

    number_map = {
        "one": 1, "1": 1, "first": 1,
        "two": 2, "2": 2, "second": 2, "too": 2, "to": 2,
        "three": 3, "3": 3, "third": 3,
        "four": 4, "4": 4, "fourth": 4, "for": 4,
        "five": 5, "5": 5, "fifth": 5
    }

    words = text.split()

    for word in words:
        if word in number_map:
            return number_map[word]

    # EXTRA: handle phrases like "mail number 2"
    for key in number_map:
        if key in text:
            return number_map[key]

    return None

# ==========================================================
# 📥 MAIN FUNCTION
# ==========================================================

def show_read_mail():

    apply_neon_ui()

    user_email = st.session_state.get("user_email")
    user_password = st.session_state.get("user_password")

    if not user_email or not user_password:
        st.session_state.page = "login"
        st.rerun()

    st.markdown("## 📥 Voice Inbox")

    try:

        speak("Opening your inbox")

        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(user_email, user_password)
        mail.select("inbox")

        result, data = mail.search(None, "ALL")
        all_mails = data[0].split()

        result, data = mail.search(None, "UNSEEN")
        unread_mails = data[0].split()

        speak("Inbox opened successfully")

        while True:

            speak("Say mail count, unread mail, read latest mail, read mail number or exit")

            command = listen()

            if not command:
                speak("Please say again")
                continue

            command = command.lower()

            if "count" in command:
                speak(f"You have {len(all_mails)} emails")

            elif "unread" in command:
                speak(f"You have {len(unread_mails)} unread emails")

            elif "latest" in command:
                read_selected_mail(mail, all_mails[-1])

            elif "mail" in command or "number" in command:

                latest_five = all_mails[-5:]
                mail_map = {}
                index = 1

                for num in reversed(latest_five):

                    result, data = mail.fetch(num, "(RFC822)")
                    msg = email.message_from_bytes(data[0][1])

                    sender = msg["from"]
                    subject = msg["subject"]

                    speak(f"Mail {index} from {sender}")
                    speak(f"Subject {subject}")

                    mail_map[str(index)] = num
                    index += 1

                speak("Say the mail number")

                retry = 0
                selected = None

                while retry < 5:

                    select = listen()

                    if not select:
                        speak("Please say again")
                        retry += 1
                        continue

                    num = extract_number(select)

                    if num and str(num) in mail_map:
                        selected = mail_map[str(num)]
                        break
                    else:
                        speak("Invalid number. Please say again")
                        retry += 1

                if selected:
                    read_selected_mail(mail, selected)

            elif "exit" in command:
                speak("Closing inbox")
                break

            else:
                speak("Command not recognized")

        mail.logout()

    except Exception as e:
        st.error(str(e))
        speak("Error accessing inbox")

    go_home()


# ==========================================================
# 📧 READ MAIL
# ==========================================================

def read_selected_mail(mail, mail_id):

    result, data = mail.fetch(mail_id, "(RFC822)")
    msg = email.message_from_bytes(data[0][1])

    sender = msg["from"]
    subject = msg["subject"]

    speak(f"Email from {sender}")
    speak(f"Subject is {subject}")

    body = ""
    attachments = []

    if msg.is_multipart():
        for part in msg.walk():

            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in disposition:
                body = part.get_payload(decode=True).decode(errors="ignore")

            if "attachment" in disposition:
                attachments.append(part)

    else:
        body = msg.get_payload(decode=True).decode(errors="ignore")

    body = re.sub(r"\s+", " ", body)

    # ---------- READ BODY ----------
    if body:

        chunks = [body[i:i+300] for i in range(0, len(body), 300)]

        for i, chunk in enumerate(chunks):

            speak(chunk)

            if i != len(chunks) - 1:

                speak("Say continue or stop")

                cmd = listen()

                if not cmd:
                    speak("Please say again")
                    continue

                if "stop" in cmd:
                    break

    else:
        speak("No message body")

    # ==========================================================
    # 📎 ATTACHMENTS
    # ==========================================================

    if attachments:

        speak(f"This email has {len(attachments)} attachments")

        for i, part in enumerate(attachments):
            speak(f"Attachment {i+1}: {part.get_filename()}")

        speak("Say download all or say attachment number")

        retry = 0

        while retry < 5:

            cmd = listen()

            if not cmd:
                speak("Please say again")
                retry += 1
                continue

            cmd = cmd.lower()

            if "all" in cmd:
                download_attachments(msg)
                break

            num = extract_number(cmd)

            if num and 1 <= num <= len(attachments):
                download_single_attachment(msg, num-1)
                break

            else:
                speak("Invalid choice")
                retry += 1

    else:
        speak("No attachments found")

    # ==========================================================
    # DELETE / FORWARD
    # ==========================================================

    speak("Say delete, forward or back")

    cmd = listen()

    if not cmd:
        speak("Please say again")
        return

    cmd = cmd.lower()

    # ---------- DELETE ----------
    if "delete" in cmd:

        speak("Are you sure? Say confirm or no")

        confirm = listen()

        if confirm and ("confirm" in confirm or "yes" in confirm):

            mail.copy(mail_id, "[Gmail]/Trash")
            mail.store(mail_id, "-X-GM-LABELS", "\\Inbox")

            speak("Email moved to trash")

        else:
            speak("Delete cancelled")

    # ---------- FORWARD ----------
    elif "forward" in cmd:

        speak("Say the email address")

        retry = 0

        while retry < 3:

            to_voice = listen()

            if not to_voice:
                speak("Please say again")
                retry += 1
                continue

            to_email = smart_convert(to_voice)

            if not re.match(r"[^@]+@[^@]+\.[^@]+", to_email):
                speak("Invalid email address")
                retry += 1
                continue

            speak(f"You said {to_email}. Say confirm or no")

            confirm = listen()

            if confirm and ("confirm" in confirm or "yes" in confirm):

                sender_email = st.session_state.get("user_email")
                sender_password = st.session_state.get("user_password")

                msg_fwd = MIMEMultipart()
                msg_fwd["From"] = sender_email
                msg_fwd["To"] = to_email
                msg_fwd["Subject"] = "Fwd: " + (subject or "")

                msg_fwd.attach(MIMEText(body, "plain"))

                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, to_email, msg_fwd.as_string())

                speak("Email forwarded successfully")
                break

            else:
                speak("Please say again")
                retry += 1

    else:
        speak("Returning to inbox")


# ==========================================================
# 📂 DOWNLOAD
# ==========================================================

def download_attachments(msg):

    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    folder = os.path.join(desktop, "voice_mail_downloads")
    os.makedirs(folder, exist_ok=True)

    count = 0

    for part in msg.walk():
        if "attachment" in str(part.get("Content-Disposition")):
            filename = part.get_filename()
            if filename:
                path = os.path.join(folder, filename)
                with open(path, "wb") as f:
                    f.write(part.get_payload(decode=True))
                count += 1

    speak(f"{count} files downloaded")
    speak(f"Saved in {folder}")


def download_single_attachment(msg, index):

    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    folder = os.path.join(desktop, "voice_mail_downloads")
    os.makedirs(folder, exist_ok=True)

    attachments = []

    for part in msg.walk():
        if "attachment" in str(part.get("Content-Disposition")):
            attachments.append(part)

    if index < len(attachments):

        part = attachments[index]
        filename = part.get_filename()
        path = os.path.join(folder, filename)

        with open(path, "wb") as f:
            f.write(part.get_payload(decode=True))

        speak(f"{filename} downloaded")
        speak(f"Saved in {folder}")


# ==========================================================
# 🔙 RETURN HOME
# ==========================================================

def go_home():

    speak("Returning to dashboard")

    st.session_state.page = "home"
    st.rerun()