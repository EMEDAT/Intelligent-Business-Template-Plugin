import os
import io
from notion_client import Client
from dotenv import load_dotenv
from flask import Blueprint, send_file, make_response, request, jsonify
from app.services import template_service
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

bp = Blueprint("template_generator", __name__, url_prefix="/templates")

# Google Docs Functionality

def save_to_google_docs(template_content, document_title):
    credentials_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_CREDENTIALS")
    if not credentials_path or not os.path.exists(credentials_path):
        raise FileNotFoundError(f"Google credentials file not found: {credentials_path}")

    try:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/documents"]
        )
        docs_service = build('docs', 'v1', credentials=credentials)

        # Create a new Google Doc
        document = docs_service.documents().create(body={"title": document_title}).execute()
        document_id = document.get("documentId")

        # Write content to the Google Doc
        requests = [{"insertText": {"location": {"index": 1}, "text": template_content}}]
        docs_service.documents().batchUpdate(documentId=document_id, body={"requests": requests}).execute()

        return f"https://docs.google.com/document/d/{document_id}"
    except Exception as e:
        print(f"Error saving to Google Docs: {e}")
        return None

# Notion Functionality

def save_to_notion(template_content, page_title):
    notion_token = os.getenv("YOUR_NOTION_INTEGRATION_TOKEN")
    database_id = os.getenv("YOUR_DATABASE_ID")

    if not notion_token:
        raise ValueError("YOUR_NOTION_INTEGRATION_TOKEN environment variable is not set.")
    if not database_id:
        raise ValueError("YOUR_DATABASE_ID environment variable is not set.")

    notion = Client(auth=notion_token)

    try:
        database = notion.databases.retrieve(database_id)
        # Find the title property
        title_property_name = None
        for name, details in database["properties"].items():
            if details["type"] == "title":
                title_property_name = name
                break
        if not title_property_name:
            raise ValueError("No title property found in the database.")

        # Construct the properties dictionary dynamically
        properties = {
            title_property_name: {"title": [{"text": {"content": page_title}}]}
        }

        # Example: Setting "Status" to "In Progress" (Adapt as needed)
        if "Status" in database["properties"]:
            properties["Status"] = {"select": {"name": "In Progress"}}
        # Example: Setting "Due Date" (Adapt as needed)
        if "Due Date" in database["properties"]:
            properties["Due Date"] = {"date": {"start": "2024-12-31"}}  # ISO 8601 format

        new_page = notion.pages.create(
            parent={"database_id": database_id},
            properties=properties,
            children=[
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": template_content}}]
                    }
                }
            ]
        )

        url = new_page.get("url")
        return url
    except Exception as e:
        print(f"Error saving to Notion: {e}")
        return None

@bp.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        if not data or "template_type" not in data or "key_points" not in data:
            return jsonify({"error": "template_type and key_points are required"}), 400
        template_type = data["template_type"]
        key_points = data["key_points"]
        format_type = data.get("format", "word")  # Default to "word"

        template_data = template_service.create_template(template_type, key_points)
        content = template_data.get("content", "")

        file_bytes = None
        mimetype = None
        filename = None

        if format_type == "word":
            mimetype = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            filename = f"{template_type}.docx"
            file_bytes = template_service.export_as_word(content)
        elif format_type == "pdf":
            mimetype = "application/pdf"
            filename = f"{template_type}.pdf"
            file_bytes = template_service.export_as_pdf(content)
        elif format_type == "pptx":
            mimetype = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
            filename = f"{template_type}.pptx"
            file_bytes = template_service.export_as_pptx(content)
        else:
            return jsonify({"error": f"Unsupported format: {format_type}"}), 400

        if file_bytes is None:
            return jsonify({"error": "File generation failed"}), 500

        response = make_response(send_file(
            io.BytesIO(file_bytes),
            mimetype=mimetype,
            as_attachment=True,
            download_name=filename,
        ))

        return response
    except Exception as e:
        print(f"Template Generation Error: {e}")
        return jsonify({"error": str(e)}), 500

@bp.route("/store", methods=["POST"])
def store_template():
    try:
        data = request.get_json()
        template_type = data.get("template_type")
        key_points = data.get("key_points")
        format_type = data.get("format")

        if not template_type or not key_points or not format_type:
            return jsonify({"error": "template_type, key_points, and format are required"}), 400

        content = template_service.create_template(template_type, key_points)["content"]

        file_bytes = None
        mimetype = None
        filename = None

        if format_type == "word":
            mimetype = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            filename = f"{template_type}.docx"
            file_bytes = template_service.export_as_word(content)
        elif format_type == "pdf":
            mimetype = "application/pdf"
            filename = f"{template_type}.pdf"
            file_bytes = template_service.export_as_pdf(content)
        elif format_type == "pptx":
            mimetype = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
            filename = f"{template_type}.pptx"
            file_bytes = template_service.export_as_pptx(content)
        else:
            return jsonify({"error": f"Unsupported format: {format_type}"}), 400

        if file_bytes is None:
            return jsonify({"error": "File generation failed"}), 500

        response = make_response(send_file(
            io.BytesIO(file_bytes),
            mimetype=mimetype,
            as_attachment=True,
            download_name=filename,
        ))

        return response
    except Exception as e:
        print(f"Template Generation Error: {e}")
        return jsonify({"error": str(e)}), 500

@bp.route('/save_to_google_docs', methods=['POST'])
def save_to_google_docs_route():
    """Saves the generated template to Google Docs."""
    try:
        data = request.get_json()
        template_type = data.get("template_type")
        key_points = data.get("key_points")

        if not template_type or not key_points:
            return jsonify({"error": "template_type and key_points are required"}), 400

        template_data = template_service.create_template(template_type, key_points)
        content = template_data.get("content", "")

        doc_url = save_to_google_docs(content, f"{template_type} Template")
        return jsonify({"url": doc_url}), 200
    except Exception as e:
        print(f"Google Docs Error: {e}")
        return jsonify({"error": str(e)}), 500
