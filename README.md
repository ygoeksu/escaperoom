# 🎮 Escape Room Chat Game

An extensible, chat-based escape room game built with a Python backend and a TypeScript/React frontend. Players interact with the game through a chat interface, solving puzzles, exploring rooms, and escaping scenarios powered by a deterministic game engine.

## 🧠 Concept

This project simulates an escape room experience through a chat interface:

Players type commands like look, take key, use key on door
A backend game engine processes actions and updates state
A frontend chat UI renders the interaction like a conversational game

The system is designed to be:

extensible (add new escape rooms via content files)
testable (engine is fully deterministic)
deployable (Docker + CI/CD ready)
optionally AI-enhanced (for narration and hints)
## 🏗️ Architecture


Frontend (React + TypeScript)
        ↓
FastAPI Backend (Python)
        ↓
Game Engine (pure logic, no I/O)
        ↓
Content Layer (Rooms / Puzzles / Items)
        ↓
State Store (in-memory / optional Redis)

## 🧱 Tech Stack
Backend
Python 3.11+
FastAPI
Pydantic
Pytest
Frontend
React
TypeScript
Vite
DevOps
Docker
Docker Compose
GitHub Actions (CI/CD)
## 🎮 Features
Core Gameplay
Chat-based interaction system
Multiple escape rooms (data-driven)
Inventory system
Puzzle mechanics
Win/lose conditions
Architecture
Fully separated game engine
Content-driven room system (JSON-based)
Stateless API layer
Extensible design for new puzzles
DevOps
Dockerized backend and frontend
Automated testing via CI pipeline
Build validation on every push
## 📁 Project Structure
escape-room-game/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes
│   │   ├── engine/       # Game logic (core)
│   │   ├── content/       # Rooms, puzzles, items
│   │   ├── models/       # Pydantic schemas
│   │   └── main.py
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── api/
│   │   ├── types/
│   │   └── App.tsx
│   ├── index.html
│   └── package.json
│
├── infra/
│   ├── docker-compose.yml
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
└── README.md
## 🚀 Getting Started
1. Clone repository
git clone https://github.com/your-username/escape-room-game.git
cd escape-room-game
2. Run with Docker (recommended)
docker-compose up --build
Frontend: http://localhost:3000
Backend: http://localhost:8000
3. Run backend locally
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
4. Run frontend locally
cd frontend
npm install
npm run dev
## 🧪 Running Tests
Backend tests
cd backend
pytest
## 🧩 Game Design

The game is powered by a data-driven content system:

Example Room
{
  "id": "cell_01",
  "description": "A dark prison cell with a locked door.",
  "items": ["rusty_key"],
  "exits": {
    "north": "hallway_01"
  }
}
Example Puzzle
{
  "id": "door_lock",
  "type": "key_lock",
  "required_item": "rusty_key",
  "result": "door_unlocked"
}
⚙️ CI/CD Pipeline

On every push:

Install dependencies
Run backend tests (pytest)
Build frontend
(Optional) Build Docker images
## 🌩️ Deployment (Optional)

The project is designed to be deployable via:

Fly.io
Render
AWS (ECS / Fargate)
## 🤖 Future Improvements
AI-powered narration layer (LLM storyteller)
WebSocket-based real-time gameplay
Multiplayer escape rooms
Save/load game states
Leaderboards (escape time tracking)
## 🎯 Design Principles
Engine is deterministic
Content is data-driven
API is stateless
Frontend is presentation-only
## 📜 License

MIT (or your choice)

## 💡 Motivation

This project was built to explore:

system design for interactive games
clean separation of logic and interface
CI/CD pipelines in real-world fullstack apps
cloud deployment of containerized systems