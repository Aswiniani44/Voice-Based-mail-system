# ==========================================================
# FACE_UTILS.PY - Face Capture (Correct Version)
# ==========================================================

import cv2
import face_recognition
import pickle
import time


def capture_face():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return None

    time.sleep(2)  # camera warmup

    ret, frame = cap.read()

    if not ret:
        cap.release()
        return None

    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces
    face_locations = face_recognition.face_locations(rgb_frame)

    if len(face_locations) == 0:
        cap.release()
        return None

    # Generate encoding
    encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]

    cap.release()

    # Convert encoding to binary
    face_binary = pickle.dumps(encoding)

    return face_binary