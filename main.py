from fastapi import FastAPI
from routes import story_routes

app = FastAPI()

# Register the new story routes
app.include_router(story_routes.router, prefix="/story", tags=["Story"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Story Game!"}
