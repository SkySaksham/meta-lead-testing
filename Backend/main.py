import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import PlainTextResponse,HTMLResponse

load_dotenv()

app = FastAPI()

VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN")

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
    body = await request.body()
    js = await request.json()

    print(body)
    print(js)


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