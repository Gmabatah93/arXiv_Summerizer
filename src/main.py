from fastapi import FastAPI
from src.routers import ping, papers, ask

app = FastAPI()

app.include_router(ping.router)
app.include_router(papers.router)
app.include_router(ask.router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000, host="127.0.0.1")