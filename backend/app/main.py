from fastapi import FastAPI

app = FastAPI(title="Human Firewall API")

@app.get("/")
def root():
    return {"message": "Human Firewall backend is running"}

@app.get("/health")
def health():
    return {"status": "ok"}