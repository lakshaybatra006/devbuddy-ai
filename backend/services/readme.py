def generate_readme(data: dict):
    return f"""
# {data.get('title', 'DevPilot Project')}

## Overview
{data.get('description', '')}

## Features
- Authentication
- API System
- Frontend UI
- Scalable Architecture

## Tech Stack
- React
- FastAPI
- PostgreSQL
- Docker

## Getting Started
```bash
cd backend
uvicorn main:app --reload