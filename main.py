from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def get_health():
    return {"status": "get alive"}


@app.post("/health")
def post_health():
    return {"status": "post alive"}
