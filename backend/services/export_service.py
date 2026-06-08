import os
import json
import zipfile
import re
from fpdf import FPDF


def clean_text(text):
    return re.sub(
        r"[^\x00-\x7F]+",
        "",
        str(text)
    )


def generate_pdf(chat_memory):

    os.makedirs("temp", exist_ok=True)

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font(
        "Arial",
        size=12
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    pdf.cell(
        200,
        10,
        txt="DevBuddy AI Report",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    if not chat_memory:

        pdf.multi_cell(
            0,
            8,
            txt="No chat history available."
        )

    else:

        for msg in chat_memory:

            role = clean_text(
                msg.get("role", "")
            )

            text = clean_text(
                msg.get("text", "")
            )

            pdf.multi_cell(
                0,
                8,
                txt=f"{role.upper()}: {text}"
            )

            pdf.ln(3)

    path = "temp/devbuddy.pdf"

    pdf.output(path)

    return path


def generate_project_zip(chat_memory):

    os.makedirs("temp", exist_ok=True)

    zip_path = "temp/devbuddy.zip"

    with zipfile.ZipFile(
        zip_path,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zipf:

        zipf.writestr(
            "chat_history.json",
            json.dumps(
                chat_memory,
                indent=2
            )
        )

        readme_content = """
DevBuddy AI Export

Generated Chat History Export

Contains:
- chat_history.json
"""

        zipf.writestr(
            "README.txt",
            readme_content
        )

    return zip_path