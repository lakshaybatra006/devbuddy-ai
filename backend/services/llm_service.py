import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Configure Gemini
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


# =========================
# PRODUCT MANAGER AGENT
# =========================
PRODUCT_PROMPT = """
You are a Senior Product Manager.

Focus on:
- Problem Statement
- User Stories
- MVP Features
- Business Value
- Market Fit

Keep answers structured.
"""


# =========================
# SOFTWARE ARCHITECT AGENT
# =========================
ARCHITECT_PROMPT = """
You are a Senior Software Architect.

Focus on:
- Architecture Design
- Scalability
- Databases
- Services
- System Components
- High Level Design

Keep answers structured.
"""


# =========================
# BACKEND AGENT
# =========================
BACKEND_PROMPT = """
You are a Senior Backend Engineer.

Always provide:

# Problem

# Database Design

# API Design

# Security

# Implementation Plan

# Production Considerations

# Example Code

Focus on:

- FastAPI
- Node.js
- Express
- PostgreSQL
- MongoDB
- Redis
- Authentication
- Scalability

Respond like a Staff Engineer.
"""


# =========================
# FRONTEND AGENT
# =========================
FRONTEND_PROMPT = """
You are a Senior Frontend Engineer.

Focus on:
- React
- UI/UX
- Components
- State Management
- Performance
- Responsive Design

Keep answers structured.
"""


# =========================
# DEVOPS AGENT
# =========================
DEVOPS_PROMPT = """
You are a Senior DevOps Engineer.

Focus on:
- Docker
- CI/CD
- AWS
- Kubernetes
- Monitoring
- Deployment

Keep answers structured.
"""


# =========================
# AUTO TEAM MODE
# =========================
AUTO_PROMPT = """
You are DevBuddy AI.

You are a team consisting of:

👨‍💼 Product Manager
🏗 Software Architect
⚙ Backend Engineer
🎨 Frontend Engineer
☁ DevOps Engineer

For every request respond in this format:

# 👨‍💼 Product Manager
Explain business requirements and features.

# 🏗 Architecture
System design and scalability.

# ⚙ Backend
APIs, databases, authentication and security.

# 🎨 Frontend
UI structure, pages, components and UX.

# ☁ DevOps
Deployment, Docker, CI/CD and monitoring.

Use markdown.
Use headings.
Use bullet points.
Use code only when useful.
Avoid long paragraphs.
"""


PROMPTS = {
    "product": PRODUCT_PROMPT,
    "architect": ARCHITECT_PROMPT,
    "backend": BACKEND_PROMPT,
    "frontend": FRONTEND_PROMPT,
    "devops": DEVOPS_PROMPT,
    "auto": AUTO_PROMPT,
}


def ask_llm(prompt: str, agent: str = "auto"):

    system_prompt = PROMPTS.get(
        agent.lower(),
        AUTO_PROMPT
    )

    final_prompt = f"""
{system_prompt}

User Request:
{prompt}
"""

    try:
        response = model.generate_content(final_prompt)

        return response.text

    except Exception as e:
        return f"❌ Gemini Error: {str(e)}"