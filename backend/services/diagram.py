from fpdf import FPDF

def create_architecture_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="DevPilot Architecture", ln=True)

    lines = [
        "User → Frontend (React)",
        "Frontend → FastAPI Backend",
        "Backend → AI Model (Ollama)",
        "Backend → Database",
        "Backend → Redis Cache"
    ]

    for l in lines:
        pdf.cell(200, 10, txt=l, ln=True)

    path = "temp/architecture.pdf"
    pdf.output(path)

    return path