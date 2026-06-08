# Escape Room — Frontend

React + TypeScript + Vite frontend for the escape room chat game.

## Prerequisites

- Node.js 18+
- The backend running on `http://localhost:8000` (see `../backend/`)

## Getting Started

```bash
# Install dependencies
npm install

# Start the dev server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

The dev server proxies `/start` and `/command` requests to the backend automatically, so no extra configuration is needed.

## Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start the development server with hot reload |
| `npm run build` | Type-check and build for production (`dist/`) |
| `npm run preview` | Preview the production build locally |

## Project Structure

```
src/
├── api/
│   └── gameApi.ts          # startGame / sendCommand API calls
├── components/
│   ├── ChatWindow.tsx       # Scrolling message log
│   ├── CommandInput.tsx     # Text input and Send button
│   ├── CommandReference.tsx # Sidebar listing all available commands
│   └── GameStatus.tsx       # Header bar showing room / turns / inventory
├── types/
│   └── game.ts             # Shared TypeScript types
├── App.tsx                 # Root component and game state
├── index.css               # Global styles
└── main.tsx                # Entry point
```

## Running with Docker

From the repository root:

```bash
docker-compose up --build
```

This starts both the backend and frontend together.
