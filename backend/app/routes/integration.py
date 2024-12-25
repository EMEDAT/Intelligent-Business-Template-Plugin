import os
from flask import Blueprint, request, jsonify
from app.services.messaging import SlackIntegration, WhatsAppIntegration, TeamsIntegration
from app.services.nlp_processor import NLPProcessor
from firebase_admin import firestore

bp = Blueprint("integration", __name__, url_prefix="/integration")

# Initialize messaging services
slack_service = SlackIntegration()
whatsapp_service = WhatsAppIntegration()
teams_service = TeamsIntegration()
nlp_processor = NLPProcessor(api_key=os.getenv("OPENAI_API_KEY"))

@bp.route("/slack", methods=["POST"])
def slack_event():
    data = request.json
    if not data or not data.get("channel_id"):
        return jsonify({"error": "Channel ID is required"}), 400

    conversation = slack_service.fetch_conversation(data.get("channel_id"))
    if not conversation:
        return jsonify({"error": f"Failed to fetch Slack conversation: {slack_service.last_error}"}), 500

    key_points = nlp_processor.extract_key_points(conversation)
    return jsonify({"key_points": key_points})

@bp.route("/whatsapp", methods=["POST"])
def whatsapp_event():
    data = request.json
    if not data or not data.get("thread_id"):
        return jsonify({"error": "Thread ID is required"}), 400

    conversation = whatsapp_service.fetch_conversation(data.get("thread_id"))
    if not conversation:
        return jsonify({"error": "Failed to fetch WhatsApp conversation"}), 500

    key_points = nlp_processor.extract_key_points(conversation)
    return jsonify({"key_points": key_points})

@bp.route("/teams", methods=["POST"])
def teams_event():
    data = request.json
    if not data or not data.get("team_id"):
        return jsonify({"error": "Team ID is required"}), 400

    conversation = teams_service.fetch_conversation(data.get("team_id"))
    if not conversation:
        return jsonify({"error": "Failed to fetch Teams conversation"}), 500

    key_points = nlp_processor.extract_key_points(conversation)
    return jsonify({"key_points": key_points})

@bp.route("/upload", methods=["POST"])
def upload_transcript():
    data = request.json
    transcript = data.get("transcript", "")
    if not transcript:
        return jsonify({"error": "Transcript is required"}), 400

    key_points = nlp_processor.extract_key_points(transcript)
    return jsonify({"key_points": key_points})

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
