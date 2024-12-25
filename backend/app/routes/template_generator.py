import os
from notion_client import Client
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from app.services.template_service import create_template, export_as_word, export_as_pdf, export_as_pptx
from google.oauth2 import service_account
from googleapiclient.discovery import build
from firebase_admin import firestore

load_dotenv()

bp = Blueprint("template_generator", __name__, url_prefix="/templates")

# Google Docs Functionality
def save_to_google_docs(template_content, document_title):
    credentials_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_CREDENTIALS")
    if not credentials_path or not os.path.exists(credentials_path):
        raise FileNotFoundError(f"Google credentials file not found: {credentials_path}")

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

        # Example: Setting "Status" to "In Progress"
        if "Status" in database["properties"]:
            properties["Status"] = {"select": {"name": "In Progress"}}

        # Example: Setting "Due Date"
        if "Due Date" in database["properties"]:
            properties["Due Date"] = {"date": {"start": "2024-12-31"}}  # YYYY-MM-DD format

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
            ],
        )

        url = new_page.get("url")
        return url
    except Exception as e:
        return str(e)

@bp.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        template_type = data.get("template_type", "business_plan")
        key_points = data.get("key_points", [])

        if not key_points:
            return jsonify({"error": "Key points are required"}), 400

        # Generate the template
        content = create_template(template_type, key_points)
        return jsonify({"template": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/save_to_google_docs", methods=["POST"])
def google_docs_endpoint():
    try:
        data = request.json
        content = data.get("content", "")
        title = data.get("title", "Generated Template")

        if not content:
            return jsonify({"error": "Content is required"}), 400

        doc_link = save_to_google_docs(content, title)
        return jsonify({"message": "Template saved to Google Docs", "link": doc_link})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/save_to_notion", methods=["POST"])
def notion_endpoint():
    try:
        data = request.json
        content = data.get("content", "")
        title = data.get("title", "Generated Template")

        if not content:
            return jsonify({"error": "Content is required"}), 400

        notion_link = save_to_notion(content, title)
        return jsonify({"message": "Template saved to Notion", "link": notion_link})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/store", methods=["POST"])
def store_template():
    try:
        data = request.json
        template_type = data.get("template_type")
        key_points = data.get("key_points")
        format_type = data.get("format")  # New: Get the desired format

        if not template_type or not key_points or not format_type:
            return jsonify({"error": "template_type, key_points, and format are required"}), 400

        # Generate the template content
        content = create_template(template_type, key_points)["content"]

        # Export to the desired format
        if format_type == "word":
            file_path = export_as_word(content, f"{template_type}.docx")
        elif format_type == "pdf":
            file_path = export_as_pdf(content, f"{template_type}.pdf")
        elif format_type == "pptx":
            file_path = export_as_pptx(content, f"{template_type}.pptx")
        else:
            return jsonify({"error": f"Unsupported format: {format_type}"}), 400

        return jsonify({"message": f"Template exported to: {file_path}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500