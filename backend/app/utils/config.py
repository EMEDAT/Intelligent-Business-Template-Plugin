import os
import json
import base64
import firebase_admin
from firebase_admin import credentials, firestore

def configure_app(app):
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")
    app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", "./uploads")
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB


def initialize_firebase():
    # Load Firebase credentials
    firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS")
    if not firebase_credentials_path:
        raise Exception("FIREBASE_CREDENTIALS environment variable is not set")

    # Load Firebase Realtime Database URL
    firebase_database_url = os.getenv("FIREBASE_DATABASE_URL")
    if not firebase_database_url:
        raise Exception("FIREBASE_DATABASE_URL environment variable is not set")

    # Initialize Firebase Admin SDK
    cred = credentials.Certificate(firebase_credentials_path)
    firebase_admin.initialize_app(cred, {
        "databaseURL": firebase_database_url
    })
    print("Firebase Realtime Database initialized successfully")