import os
import re
import json
from pypdf import PdfReader
from docx import Document
from flask import Blueprint, request, jsonify
from app.services.messaging import SlackIntegration, WhatsAppIntegration, TeamsIntegration
from app.services.nlp_processor import NLPProcessor
from firebase_admin import firestore

# Configuration for wkhtmltopdf (optional, depending on your setup)
wkhtmltopdf_path = '/usr/local/bin/wkhtmltopdf'  # Replace with the actual path if needed

bp = Blueprint("integration", __name__, url_prefix="/integration")

# Initialize messaging services
slack_service = SlackIntegration()
whatsapp_service = WhatsAppIntegration()
teams_service = TeamsIntegration()
nlp_processor = NLPProcessor(api_key=os.getenv("OPENAI_API_KEY"))


def clean_and_extract_key_points(conversation):
    cleaned_conversation = re.sub(r'\s+', ' ', conversation).strip()
    key_points = nlp_processor.extract_key_points(cleaned_conversation)

    if isinstance(key_points, dict) and "error" in key_points:
        return key_points # Return the error dictionary

    cleaned_key_points = []
    if isinstance(key_points, str):
        for point in key_points.split('\n'):
            cleaned_point = re.sub(r'\s+', ' ', point.strip())
            if cleaned_point:
                cleaned_point = re.sub(r"^\d+\.\s*", "", cleaned_point).strip()
                cleaned_key_points.append(cleaned_point)
    elif isinstance(key_points, list):
        cleaned_key_points = [re.sub(r'\s+', ' ', str(point).strip()) for point in key_points]
    else:
        cleaned_key_points = []
    return cleaned_key_points

@bp.route("/slack", methods=["POST"])
def slack_event():
    data = request.json
    if not data or not data.get("channel_id"):
        return jsonify({"error": "Channel ID is required"}), 400

    conversation = slack_service.fetch_conversation(data.get("channel_id"))
    if not conversation:
        return jsonify({"error": f"Failed to fetch Slack conversation: {slack_service.last_error}"}), 500

    cleaned_key_points = clean_and_extract_key_points(conversation)
    if isinstance(cleaned_key_points, dict) and "error" in cleaned_key_points:
        return jsonify(cleaned_key_points), 500

    return jsonify({"key_points": cleaned_key_points})

@bp.route("/whatsapp", methods=["POST"])
def whatsapp_event():
    data = request.json
    if not data or not data.get("thread_id"):
        return jsonify({"error": "Thread ID is required"}), 400

    conversation = whatsapp_service.fetch_conversation(data.get("thread_id"))
    if not conversation:
        return jsonify({"error": "Failed to fetch WhatsApp conversation"}), 500

    cleaned_key_points = clean_and_extract_key_points(conversation)
    if isinstance(cleaned_key_points, dict) and "error" in cleaned_key_points:
        return jsonify(cleaned_key_points), 500
    return jsonify({"key_points": cleaned_key_points})

@bp.route("/teams", methods=["POST"])
def teams_event():
    data = request.json
    if not data or not data.get("team_id"):
        return jsonify({"error": "Team ID is required"}), 400

    conversation = teams_service.fetch_conversation(data.get("team_id"))
    if not conversation:
        return jsonify({"error": "Failed to fetch Teams conversation"}), 500

    cleaned_key_points = clean_and_extract_key_points(conversation)
    if isinstance(cleaned_key_points, dict) and "error" in cleaned_key_points:
        return jsonify(cleaned_key_points), 500

    return jsonify({"key_points": cleaned_key_points})

@bp.route("/upload", methods=["POST"])
def upload_transcript():
    try:
        transcript = ""

        if "file" in request.files:
            file = request.files["file"]
            filename = file.filename.lower()

            if filename.endswith(".pdf"):
                reader = PdfReader(file)
                transcript = " ".join([page.extract_text() for page in reader.pages])
            elif filename.endswith(".docx"):
                doc = Document(file)
                transcript = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            else:
                transcript = file.read().decode("utf-8")

        elif request.json:
            transcript = request.json.get("transcript", "")

        if not transcript:
            return jsonify({"error": "Transcript is required"}), 400

        cleaned_key_points = clean_and_extract_key_points(transcript)
        if isinstance(cleaned_key_points, dict) and "error" in cleaned_key_points:
            return jsonify(cleaned_key_points), 500

        return jsonify({"key_points": cleaned_key_points}), 200

    except UnicodeDecodeError:
        return jsonify({"error": "Unsupported file encoding or format"}), 400
    except Exception as e:
        print(f"Error processing transcript: {e}")
        return jsonify({"error": str(e)}), 500


@bp.route("/read/<collection>/<doc_id>", methods=["GET"])
def read_document(collection, doc_id):
    try:
        db = firestore.client()
        doc_ref = db.collection(collection).document(doc_id)
        doc = doc_ref.get()
        if doc.exists:
            return jsonify(doc.to_dict()), 200
        else:
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500