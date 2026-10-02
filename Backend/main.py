from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/health")
async def health():
    return {"status":"UP"}


@app.post("/leads")
async def leads(request: Request):
    body = request.body()
    js = request.json()

    print(body)
    print(js)