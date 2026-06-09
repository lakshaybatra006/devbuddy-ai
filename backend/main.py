from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.middleware.sessions import SessionMiddleware
from services.llm_service import ask_llm
from services.export_service import generate_pdf, generate_project_zip
from models import ChatRequest
from services.auth_google import oauth
from motor.motor_asyncio import AsyncIOMotorClient
from db import users_collection
from models import UserRegister, UserLogin
from auth import hash_password, verify_password, create_token

app = FastAPI()

chat_memory = []

app.add_middleware(SessionMiddleware, secret_key="devbuddy_secret")

# Mongo
client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
db = client[os.getenv("DB_NAME")]
users_collection = db["users"]

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
# HOME
# =========================
@app.get("/")
def home():
    return {"message": "DevBuddy Backend Running 🚀"}

# =========================
# CHAT
# =========================
@app.post("/chat")
def chat(data: ChatRequest):
    try:
        answer = ask_llm(data.query, data.agent)

        # store chat automatically
        chat_memory.append({
            "role": "user",
            "text": data.query
        })

        chat_memory.append({
            "role": "bot",
            "text": answer
        })

        return {"response": answer}

    except Exception as e:
        return {"error": str(e)}
@app.get("/auth/google/login")
async def google_login(request: Request):

    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")

    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/google/callback")
async def google_callback(request: Request):

    token = await oauth.google.authorize_access_token(request)

    user_info = token.get("userinfo")

    if not user_info:
        return {"error": "Google login failed"}

    email = user_info["email"]

    user = await users_collection.find_one({"email": email})

    if not user:
        new_user = {
            "name": user_info["name"],
            "email": email,
            "picture": user_info["picture"]
        }
        await users_collection.insert_one(new_user)

    return RedirectResponse(url="https://devbuddy-ai.vercel.app/")  # frontend redirect
@app.post("/register")
async def register(user: UserRegister):

    existing = await users_collection.find_one({"email": user.email})

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    await users_collection.insert_one({
        "email": user.email,
        "password": hash_password(user.password)
    })

    return {"message": "User registered successfully"}

@app.post("/login")
async def login(user: UserLogin):

    db_user = await users_collection.find_one({"email": user.email})

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_token({"email": user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
# =========================
# STORE (optional)
# =========================
@app.post("/store")
def store(data: dict):
    chat_memory.append(data)
    return {"status": "ok"}

# =========================
# PDF DOWNLOAD
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