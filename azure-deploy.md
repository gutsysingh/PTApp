# Azure Deploy (Free-first) - Quick Guide

1) Create a Resource Group:
   az group create -n papertrade-rg -l westeurope

2) Create GitHub repo and push this project.

3) Create Azure Static Web App (Free):
   - In Azure Portal: Static Web Apps -> Create -> Link to your GitHub repo and branch
   - App location: /frontend
   - Api location: (leave blank if using separate Function/App Service)

4) Option A (Simple): Deploy backend separately as App Service (Free tier) using the Dockerfile or run as a container.
   Option B: Use Azure Functions (for serverless endpoints) under /api.

5) Provision Azure Database for PostgreSQL if needed (optional for initial testing).

Notes:
- Initially run in mock mode (no Angel One keys).
- For local dev you can simply run backend and open frontend in browser.
