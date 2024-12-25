from flask import Blueprint, request, jsonify
from firebase_admin import firestore

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")

@settings_bp.route("/update", methods=["POST"])
def update_settings():
    try:
        db = firestore.client()  # Initialize Firestore client inside the function
        data = request.json
        setting_id = data.get("setting_id")
        settings_data = data.get("settings_data")

        if not setting_id or not settings_data:
            return jsonify({"error": "setting_id and settings_data are required"}), 400

        doc_ref = db.collection("settings").document(setting_id)
        doc_ref.update(settings_data)

        return jsonify({"status": "success", "message": "Settings updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@settings_bp.route("/delete/<collection>/<doc_id>", methods=["DELETE"])
def delete_document(collection, doc_id):
    try:
        db = firestore.client()  # Initialize Firestore client inside the function
        db.collection(collection).document(doc_id).delete()
        return jsonify({"status": "success", "message": "Document deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500