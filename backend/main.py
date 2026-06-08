import os
import json
import zipfile
import re
from fpdf import FPDF


def clean_text(text):
    if not text:
        return ""
    return re.sub(r"[^\x00-\x7F]+", "", str(text))


# =========================
# PDF GENERATION
# =========================
def generate_pdf(chat_memory):

    os.makedirs("temp", exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.cell(200, 10, txt="DevBuddy AI Report", ln=True, align="C")
    pdf.ln(10)

    if not chat_memory:
        pdf.multi_cell(0, 8, "No chat history available.")
    else:
        for msg in chat_memory:

            role = clean_text(msg.get("role", "user"))
            text = clean_text(msg.get("text") or msg.get("content", ""))

            pdf.multi_cell(0, 8, f"{role.upper()}: {text}")
            pdf.ln(2)

    path = "temp/devbuddy.pdf"
    pdf.output(path)

    return path


# =========================
# ZIP GENERATION
# =========================
def generate_project_zip(chat_memory):

    os.makedirs("temp", exist_ok=True)

    zip_path = "temp/devbuddy.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:

        zipf.writestr(
            "chat_history.json",
            json.dumps(chat_memory or [], indent=2)
        )

        zipf.writestr(
            "README.txt",
            "DevBuddy AI Export\nContains chat history JSON"
        )

    return zip_path