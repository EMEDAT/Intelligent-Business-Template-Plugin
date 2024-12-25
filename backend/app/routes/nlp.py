import os
from flask import Blueprint, request, jsonify
from app.services.nlp_processor import NLPProcessor

bp = Blueprint("nlp", __name__, url_prefix="/nlp")
nlp_processor = NLPProcessor(api_key=os.getenv("OPENAI_API_KEY"))

@bp.route("/process", methods=["POST"])
def process_text():
    try:
        data = request.json
        text = data.get("text", "")
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        # Use NLPProcessor to extract key points
        key_points = nlp_processor.extract_key_points(text)
        
        return jsonify({"key_points": key_points})
    except Exception as e:
        return jsonify({"error": str(e)}), 500