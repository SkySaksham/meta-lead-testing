import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import PlainTextResponse

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
