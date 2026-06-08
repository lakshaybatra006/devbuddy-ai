from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from services.export_service import (
    generate_pdf,
    generate_project_zip
)

from services.llm_service import ask_llm
from models import ChatRequest

app = FastAPI()

chat_memory = []


# ==========================
# CORS
# ==========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================
# HOME
# ==========================
@app.get("/")
def home():
    return {
        "message": "DevBuddy Backend Running 🚀"
    }


# ==========================
# CHAT
# ==========================
@app.post("/chat")
def chat(data: ChatRequest):
    try:
        answer = ask_llm(
            data.query,
            data.agent
        )

        return {
            "response": answer
        }

    except Exception as e:
        return {
            "error": str(e)
        }


    


# ==========================
# STORE CHAT
# ==========================
@app.post("/store")
def store(data: dict):

    chat_memory.append(data)

    return {
        "status": "ok"
    }


# ==========================
# PDF EXPORT
# ==========================
@app.get("/download/pdf")
def download_pdf():

    path = generate_pdf(chat_memory)

    return FileResponse(
        path,
        media_type="application/pdf",
        filename="devbuddy.pdf"
    )


# ==========================
# ZIP EXPORT
# ==========================
@app.get("/download/zip")
def download_zip():

    path = generate_project_zip(chat_memory)

    return FileResponse(
        path,
        media_type="application/zip",
        filename="devbuddy.zip"
    )