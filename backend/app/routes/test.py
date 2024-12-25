from flask import Blueprint, request, jsonify
from firebase_admin import firestore

# Ensure unique names for blueprints
bp = Blueprint("test_bp", __name__, url_prefix="/test")  # Rename to "test_bp"
user_bp = Blueprint("user_bp", __name__, url_prefix="/user")  # Rename to "user_bp"

@bp.route("/firebase", methods=["GET"])
def test_firebase():
    try:
        db = firestore.client()  # Initialize Firestore client inside the function
        test_doc = db.collection("test").document("testDoc").get()
        data = test_doc.to_dict() if test_doc.exists else {"message": "Test document not found"}
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@user_bp.route("/create", methods=["POST"])
def create_user():
    try:
        db = firestore.client()  # Initialize Firestore client inside the function
        data = request.json
        user_id = data.get("user_id")
        user_data = data.get("user_data")

        if not user_id or not user_data:
            return jsonify({"error": "user_id and user_data are required"}), 400

        doc_ref = db.collection("users").document(user_id)
        doc_ref.set(user_data)

        return jsonify({"status": "success", "message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500