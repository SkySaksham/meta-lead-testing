import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Query, HTTPException, WebSocket
from fastapi.responses import PlainTextResponse,HTMLResponse
import requests
from lead_utils import get_lead_details

load_dotenv()

app = FastAPI()

VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN")
META_GRAPH_URL = "https://graph.facebook.com/v26.0"
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")



WEBSOCKET_SECRET = os.getenv("WEBSOCKET_SECRET")
active_connection: WebSocket | None = None



@app.get("/")
async def health():
    return {"status": "UP"}


@app.get("/leads")
async def verify(
    mode: str = Query(None, alias="hub.mode"),
    verify_token: str = Query(None, alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge"),
):
    print("MODE:", mode)
    print("VERIFY TOKEN:", verify_token)
    print("CHALLENGE:", challenge)

    if mode == "subscribe" and verify_token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)

    raise HTTPException(
        status_code=403,
        detail="Verification failed"
    )

@app.post("/leads")
async def leads(request: Request):
    global active_connection

    js = await request.json()

    leadgen_id = (
        js["entry"][0]["changes"][0]["value"]["leadgen_id"]
    )

    print("Leadgen ID:", leadgen_id)

    lead = get_lead_details(leadgen_id)

    if lead is None:
        raise HTTPException(
            status_code=502,
            detail="Failed to fetch lead from Meta"
        )

    print("LEAD DATA:")
    print(lead)

    if active_connection is not None:
        try:
            await active_connection.send_json(lead)
            print("Lead sent through WebSocket")
        except Exception as e:
            print("Failed to send lead:", e)
            active_connection = None

    return {"status": "ok"}


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str,
):
    global active_connection

    if token != WEBSOCKET_SECRET:
        await websocket.close(code=1008)
        return

    if active_connection is not None:
        await websocket.close(code=1008)
        return

    await websocket.accept()
    active_connection = websocket

    print("WebSocket connected")

    try:
        while True:
            await websocket.receive_text()
    finally:
        active_connection = None
        print("WebSocket disconnected")
@app.get("/privacy", response_class=HTMLResponse)
async def privacy_policy():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Privacy Policy</title>
        <meta charset="UTF-8">
    </head>
    <body>
        <h1>Privacy Policy</h1>

        <p>This application is a proof-of-concept for receiving Meta Lead Ad
        submissions.</p>

        <h2>Information We Receive</h2>
        <p>When a lead is submitted through a Meta Instant Form, this application
        may receive the information provided in that form.</p>

        <h2>How We Use Information</h2>
        <p>The information is used solely for testing and demonstrating the
        application's lead receiving and display functionality.</p>

        <h2>Data Storage</h2>
        <p>Lead data may be temporarily processed by the application for the
        purposes of this proof-of-concept.</p>

        <h2>Third Parties</h2>
        <p>Lead information originates from Meta platforms and is processed
        through this application.</p>

        <h2>Contact</h2>
        <p>For privacy-related questions or data deletion requests, please
        contact the application owner.</p>
    </body>
    </html>
    """