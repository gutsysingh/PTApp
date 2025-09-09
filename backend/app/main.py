# backend/app/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import time
import random
from typing import List, Dict

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Simple in-memory stores (single-user MVP)
orders: List[Dict] = []
trades: List[Dict] = []
order_id_seq = 1
trade_id_seq = 1

# Clients connected to websocket (for ticks)
clients: List[WebSocket] = []

def create_tick():
    """Return a mock tick dict."""
    # Make price random walk around 22000
    if not hasattr(create_tick, "price"):
        create_tick.price = 22000.0
    create_tick.price += random.uniform(-10, 10)
    return {
        "instrument": "NIFTY",
        "last_price": round(create_tick.price, 2),
        "bid": round(create_tick.price - 0.5, 2),
        "ask": round(create_tick.price + 0.5, 2),
        "ts": int(time.time())
    }

async def broadcast_tick(tick: Dict):
    dead = []
    for ws in clients:
        try:
            await ws.send_text(json.dumps(tick))
        except:
            dead.append(ws)
    for d in dead:
        if d in clients:
            clients.remove(d)

def try_fill_orders_with_tick(tick: Dict):
    """
    Simple matching:
    - For each OPEN MARKET order, fill fully at tick['last_price'].
    - Update order.filled_qty and order.status, create a trade record.
    """
    global trades, trade_id_seq
    filled_any = False
    last_price = tick.get("last_price")
    for order in orders:
        if order.get("status") == "OPEN" and order.get("order_type") == "MARKET":
            qty = int(order.get("qty", 0))
            if qty <= 0:
                continue
            # Fill fully at last_price
            trade = {
                "trade_id": trade_id_seq,
                "order_id": order["id"],
                "instrument": order.get("instrument"),
                "qty": qty,
                "price": last_price,
                "side": order.get("side"),
                "ts": int(time.time())
            }
            trade_id_seq += 1
            trades.append(trade)
            # Update order
            order["filled_qty"] = order.get("filled_qty", 0) + qty
            order["status"] = "FILLED"
            order["avg_fill_price"] = last_price
            filled_any = True
    return filled_any

# Background tick generator task
async def tick_generator_loop():
    while True:
        tick = create_tick()
        # try to match orders on this tick
        filled = try_fill_orders_with_tick(tick)
        # broadcast tick to websocket clients
        await broadcast_tick(tick)
        # small delay (1s)
        await asyncio.sleep(1)

@app.on_event("startup")
async def startup_event():
    # start background tick loop
    asyncio.create_task(tick_generator_loop())

# REST endpoints
@app.get("/api/account")
def get_account():
    # A simple derived account object (cash and P&L are static for now)
    return {"cash": 100000.0, "realized_pnl": 0.0, "unrealized_pnl": 0.0}

@app.post("/api/orders")
def place_order(order: Dict):
    """
    Create an order record. For MARKET orders, the background tick loop will
    attempt to fill it at the next tick.
    """
    global order_id_seq
    # basic validation
    required = ["instrument", "side", "qty", "order_type"]
    for r in required:
        if r not in order:
            return {"error": f"missing {r}"}
    order_record = {
        "id": order_id_seq,
        "instrument": order.get("instrument"),
        "side": order.get("side"),
        "qty": int(order.get("qty")),
        "filled_qty": 0,
        "price": order.get("price"),
        "order_type": order.get("order_type"),
        "status": "OPEN",
        "created_at": int(time.time())
    }
    order_id_seq += 1
    orders.append(order_record)
    return {"order_id": order_record["id"], "status": order_record["status"]}

@app.get("/api/orders")
def get_orders():
    return orders

@app.get("/api/trades")
def get_trades():
    return trades

# WebSocket endpoint for ticks
@app.websocket("/ws/quotes")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            # Keep connection alive; echo back any incoming message
            data = await websocket.receive_text()
            await websocket.send_text(f"echo: {data}")
    except WebSocketDisconnect:
        if websocket in clients:
            clients.remove(websocket)
