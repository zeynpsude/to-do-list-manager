from fastapi import FastAPI

app = FastAPI(
    title="To-Do List Manager API",
    description="Bulut Mimarilerinde Test Mühendisliği Dönem Projesi",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "To-Do List API is running!"}