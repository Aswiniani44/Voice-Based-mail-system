# ==========================================================
# DATABASE.PY
# ==========================================================

import mysql.connector


def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@2004",
        database="voice_mail_system"
    )


# ---------------- SAVE USER ----------------

def save_user(name, email, password, face_encoding):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO users (name,email,password,face_encoding)
    VALUES (%s,%s,%s,%s)
    """

    cursor.execute(query, (name, email, password, face_encoding))

    conn.commit()

    cursor.close()
    conn.close()


# ---------------- FETCH USERS ----------------

def fetch_all_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id,name,email,password,face_encoding FROM users"
    )

    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return users


# ---------------- CHECK EMAIL ----------------

def email_exists(email):

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT email FROM users WHERE email=%s"

    cursor.execute(query, (email,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result is not None