from fastapi import FastAPI, Request, Query, HTTPException

app = FastAPI()


@app.get("/")
async def health():
    return {"status": "UP"}


@app.get("/leads")
async def verify(
    challenge: str = Query(..., alias="hub.challenge")
):
    if challenge:
        print(challenge)
        return challenge

    raise HTTPException(
        status_code=400,
        detail="Missing challenge"
    )


@app.post("/leads")
async def leads(request: Request):
    body = await request.body()
    js = await request.json()

    print(body)
    print(js)
