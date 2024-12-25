import os
from docx import Document
from pptx import Presentation
import pdfkit

# Base directory for exported files
EXPORT_DIR = "./exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

def create_template(template_type, key_points):
    if template_type == "business_plan":
        return generate_business_plan(key_points)
    elif template_type == "pitch_deck":
        return generate_pitch_deck(key_points)
    elif template_type == "marketing_strategy":
        return generate_marketing_strategy(key_points)
    return {"error": "Unknown template type"}

# Generate a business plan based on extracted key points
def generate_business_plan(key_points):
    key_points_text = '\n'.join(key_points)
    content = f"Business Plan:\n{key_points_text}"
    return {
        "template_type": "business_plan",
        "content": content
    }

# Generate a pitch deck based on extracted key points
def generate_pitch_deck(key_points):
    key_points_text = '\n'.join(key_points)
    content = f"Pitch Deck:\n{key_points_text}"
    return {
        "template_type": "pitch_deck",
        "content": content
    }

# Generate a marketing strategy based on extracted key points
def generate_marketing_strategy(key_points):
    key_points_text = '\n'.join(key_points)
    content = f"Marketing Strategy:\n{key_points_text}"
    return {
        "template_type": "marketing_strategy",
        "content": content
    }

# Export templates
def export_as_word(template_content, file_name):
    file_path = os.path.join(EXPORT_DIR, f"{file_name}.docx")
    doc = Document()
    doc.add_heading("Template", level=1)
    doc.add_paragraph(template_content)
    doc.save(file_path)
    return file_path

def export_as_pdf(template_content, file_name):
    file_path = os.path.join(EXPORT_DIR, f"{file_name}.pdf")
    html_content = f"<h1>Template</h1><p>{template_content}</p>"
    pdfkit.from_string(html_content, file_path)
    return file_path

def export_as_pptx(template_content, file_name):
    file_path = os.path.join(EXPORT_DIR, f"{file_name}.pptx")
    presentation = Presentation()
    slide = presentation.slides.add_slide(presentation.slide_layouts[5])
    text_box = slide.shapes.add_textbox(left=0, top=0, width=presentation.slide_width, height=2000000)
    text_frame = text_box.text_frame
    text_frame.text = template_content
    presentation.save(file_path)
    return file_path