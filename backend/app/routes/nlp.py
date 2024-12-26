import os
from flask import Blueprint, request, jsonify
from app.services.nlp_processor import NLPProcessor  # Assuming you have this

bp = Blueprint("nlp", __name__, url_prefix="/nlp")
nlp_processor = NLPProcessor(api_key=os.getenv("OPENAI_API_KEY"))

@bp.route("/process", methods=["POST"])
def process_text():
    try:
        data = request.get_json()  # Use get_json for JSON data
        if not data or "text" not in data:
            return jsonify({"error": "Text is required"}), 400

        text = data["text"]
        key_points = nlp_processor.extract_key_points(text) # Use your NLP logic.

        return jsonify({"key_points": key_points}), 200 # Return 200 OK
    except Exception as e:
        print(f"NLP Processing Error: {e}") # Log the error for debugging
        return jsonify({"error": str(e)}), 500