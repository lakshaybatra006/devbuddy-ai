from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from services.llm_service import ask_llm
from services.export_service import generate_pdf, generate_project_zip
from models import ChatRequest

app = FastAPI()

# =========================
# CHAT MEMORY (TEMP STORAGE)
# =========================
chat_memory = []


# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def home():
    return {"message": "DevBuddy Backend Running 🚀"}


# =========================
# CHAT API
# =========================
@app.post("/chat")
def chat(data: ChatRequest):
    try:
        answer = ask_llm(data.query, data.agent)

        # store chat
        chat_memory.append({
            "role": "user",
            "text": data.query
        })

        chat_memory.append({
            "role": "assistant",
            "text": answer
        })

        return {"response": answer}

    except Exception as e:
        return {"error": str(e)}


# =========================
# STORE CHAT (OPTIONAL)
# =========================
@app.post("/store")
def store(data: dict):
    chat_memory.append(data)
    return {"status": "ok"}


# =========================
# PDF DOWNLOAD
# IMPORTANT: MUST BE GET
# =========================
@app.get("/download/pdf")
def download_pdf():
    path = generate_pdf(chat_memory)

    return FileResponse(
        path,
        media_type="application/pdf",
        filename="devbuddy.pdf"
    )


# =========================
# ZIP DOWNLOAD
# =========================
@app.get("/download/zip")
def download_zip():
    path = generate_project_zip(chat_memory)

    return FileResponse(
        path,
        media_type="application/zip",
        filename="devbuddy.zip"
    )