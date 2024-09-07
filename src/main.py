# src/main.py

from fastapi import FastAPI
from src.routers import prediction

app = FastAPI()

# Include routes
app.include_router(prediction.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Government Hackathon API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
