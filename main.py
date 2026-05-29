from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from agents import (
    ClassifierAgent,
    JSONAgent,
    EmailParserAgent,
    PDFAgent,
    ActionRouter,
)

app = FastAPI(title="Multi-Format Intake Agent System")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
classifier = ClassifierAgent()
json_agent = JSONAgent()
email_agent = EmailParserAgent()
pdf_agent = PDFAgent()
action_router = ActionRouter()

class ProcessingRequest(BaseModel):
    content: str
    content_type: Optional[str] = None

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Server is running"}

@app.post("/process")
async def process_input(request: ProcessingRequest):
    """Process input data and route to appropriate agent."""
    try:
        await classifier.classify(request.content)
        return {"status": "error", "message": "This should not be reached"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    await action_router.close()

# At the end of the file, add:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
