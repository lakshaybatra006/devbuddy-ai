import os
import re
import zipfile
import json
from fpdf import FPDF


# =========================
# CLEAN TEXT (SAFE FOR PDF)
# =========================
def clean_text(text):
    if not text:
        return ""
    return re.sub(r"[^\x00-\x7F]+", "", str(text))


# =========================
# GENERATE PDF (FIXED)
# =========================
def generate_pdf(chat_memory: list):

    os.makedirs("temp", exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title
    pdf.cell(200, 10, txt="DevBuddy AI Report", ln=True, align="C")
    pdf.ln(10)

    # DEBUG fallback
    if chat_memory is None:
        chat_memory = []

    # EMPTY CHAT FIX
    if len(chat_memory) == 0:
        pdf.multi_cell(0, 8, txt="No chat history available.")
    else:
        for msg in chat_memory:

            role = clean_text(msg.get("role", "user"))
            text = clean_text(msg.get("text", msg.get("content", "")))

            pdf.multi_cell(
                0,
                8,
                txt=f"{role.upper()}: {text}"
            )
            pdf.ln(2)

    path = "temp/devbuddy.pdf"
    pdf.output(path)

    return path


# =========================
# GENERATE ZIP (OPTIONAL)
# =========================
def generate_project_zip(chat_memory: list):

    os.makedirs("temp", exist_ok=True)

    zip_path = "temp/devbuddy.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:

        zipf.writestr(
            "chat_history.json",
            json.dumps(chat_memory or [], indent=2)
        )

        zipf.writestr(
            "README.txt",
            "DevBuddy AI Export\n\nContains chat_history.json"
        )

    return zip_path