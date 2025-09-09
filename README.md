# PaperTrade MVP (Minimal Starter)

This is a minimal starter repository for the PaperTrade MVP.
It contains a small FastAPI backend that serves:
- REST endpoints: /api/account, /api/orders
- WebSocket: /ws/quotes (streams mock ticks)

And a tiny frontend: frontend/index.html which connects to the websocket and posts orders.

## Quick Local Run (Windows / Linux)

1. Backend
   - Install Python 3.10+ and pip.
   - Open terminal, go to backend folder:
     ```
     cd backend
     pip install -r requirements.txt
     uvicorn app.main:app --reload --port 8000
     ```
2. Frontend
   - Open frontend/index.html in your browser (or serve it with a static server).
   - If you open the HTML from file://, websocket may fail; it's better to open http://localhost:8000/frontend/index.html
   - To serve frontend from backend, you can place the file under a static path or use `python -m http.server 8080` in frontend folder and open http://localhost:8080

## Next steps
- Push this repo to GitHub.
- Follow azure-deploy.md to create Azure Static Web App and/or Function App.
