from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
import os
from dotenv import load_dotenv
import openai
from bs4 import BeautifulSoup
import re
from datetime import datetime
import logging
import sys
import requests
import PyPDF2
import io
import traceback

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(
    title="Multi-Format AI Processing System",
    description="API for processing PDF files, text content, and JSON data",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the frontend static files
app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.warning("OPENAI_API_KEY not found in environment variables")
    client = None
else:
    client = openai.OpenAI(api_key=api_key)

class ProcessingResponse(BaseModel):
    classification: Dict[str, Any]
    processed_data: Dict[str, Any]
    action: Dict[str, Any]

class TextInput(BaseModel):
    text: str

class JsonInput(BaseModel):
    json_data: str

async def classify_input(text: str) -> Dict[str, Any]:
    """Classify the input using basic rules."""
    try:
        # Basic classification based on content analysis
        text_lower = text.lower()
        
        # Determine format
        format_type = "unknown"
        if "pdf" in text_lower or "adobe" in text_lower:
            format_type = "pdf"
        elif "json" in text_lower or "{" in text_lower:
            format_type = "json"
        elif "@" in text_lower and ("mail" in text_lower or "email" in text_lower):
            format_type = "email"
            
        # Determine intent
        intent = "unknown"
        if any(word in text_lower for word in ["invoice", "bill", "payment"]):
            intent = "billing"
        elif any(word in text_lower for word in ["policy", "terms", "agreement"]):
            intent = "policy"
        elif any(word in text_lower for word in ["report", "analysis", "data"]):
            intent = "report"
            
        # Calculate confidence based on content length and keyword matches
        confidence = min(0.95, 0.3 + (len(text) / 10000))
        
        # Determine risk level
        risk_level = "low"
        if any(word in text_lower for word in ["confidential", "secret", "private"]):
            risk_level = "high"
        elif any(word in text_lower for word in ["important", "urgent", "critical"]):
            risk_level = "medium"
            
        return {
            "format": format_type,
            "intent": intent,
            "confidence": round(confidence, 2),
            "risk_level": risk_level,
            "requires_escalation": risk_level == "high"
        }
    except Exception as e:
        logger.error(f"Classification error: {str(e)}")
        return {
            "format": "unknown",
            "intent": "unknown",
            "confidence": 0.0,
            "risk_level": "low",
            "requires_escalation": False
        }

async def process_email(text: str) -> Dict[str, Any]:
    """Process email content."""
    try:
        soup = BeautifulSoup(text, 'html.parser')
        plain_text = soup.get_text()

        # Extract basic metadata
        metadata = {
            "sender": re.search(r"From: (.*)", plain_text),
            "subject": re.search(r"Subject: (.*)", plain_text),
            "date": re.search(r"([A-Za-z]+ \d{1,2}, \d{4})", plain_text)
        }

        # Clean up metadata
        for key, value in metadata.items():
            if value:
                # For date, the group(1) is the matched date string itself
                if key == "date":
                    metadata[key] = value.group(1).strip()
                else:
                    metadata[key] = value.group(1).strip()
            else:
                metadata[key] = ""

        # Remove header lines from the content (From:, To:, Subject:)
        plain_text_cleaned = plain_text
        plain_text_cleaned = re.sub(r"^From: .*\n?", "", plain_text_cleaned, flags=re.MULTILINE)
        plain_text_cleaned = re.sub(r"^To: .*\n?", "", plain_text_cleaned, flags=re.MULTILINE)
        plain_text_cleaned = re.sub(r"^Subject: .*\n?", "", plain_text_cleaned, flags=re.MULTILINE)

        return {
            "metadata": metadata,
            "content": plain_text_cleaned,
            "type": "email"
        }
    except Exception as e:
        logger.error(f"Email processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Email processing error: {str(e)}")

async def process_json(json_data: str) -> Dict[str, Any]:
    """Process JSON data."""
    try:
        data = json.loads(json_data)
        return {
            "data": data,
            "type": "json"
        }
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")

async def process_pdf(content: bytes) -> Dict[str, Any]:
    """Process PDF content."""
    try:
        # Create a BytesIO object from the content
        pdf_file = io.BytesIO(content)
        
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        # Get PDF metadata
        metadata = pdf_reader.metadata
        
        return {
            "content": text,
            "metadata": {
                "title": metadata.get("/Title", ""),
                "author": metadata.get("/Author", ""),
                "pages": len(pdf_reader.pages),
                "creation_date": metadata.get("/CreationDate", "")
            },
            "type": "pdf"
        }
    except Exception as e:
        logger.error(f"PDF processing error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"PDF processing error: {str(e)}")

@app.post("/process", response_model=ProcessingResponse)
async def process_input(
    file: Optional[UploadFile] = File(None, description="Upload a PDF file"),
    text: Optional[str] = Form(None, description="Input text content"),
    json_data: Optional[str] = Form(None, description="Input JSON data as string")
):
    """
    Process various input formats (PDF, text, or JSON).
    
    This endpoint accepts three types of inputs:
    1. PDF File Upload: Use the file upload button to select a PDF file
    2. Text Content: Enter text in the text field
    3. JSON Data: Enter JSON string in the json_data field
    
    Only one type of input should be provided at a time.
    
    Returns processed data with classification and action details.
    """
    try:
        logger.info(f"Processing request - file: {bool(file)}, text: {bool(text)}, json_data: {bool(json_data)}")
        
        # Process input based on type
        if file:
            if not file.filename:
                raise HTTPException(status_code=400, detail="No file name provided")
                
            if not file.filename.lower().endswith('.pdf'):
                raise HTTPException(status_code=400, detail="Only PDF files are allowed")
                
            if file.content_type != "application/pdf":
                raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed")
                
            content = await file.read()
            if not content:
                raise HTTPException(status_code=400, detail="Empty file provided")
                
            processed_data = await process_pdf(content)
        elif json_data:
            processed_data = await process_json(json_data)
        elif text:
            processed_data = await process_email(text)
        else:
            raise HTTPException(status_code=400, detail="No input provided")

        # Classify the input
        classification = await classify_input(str(processed_data))

        # Determine action based on classification
        action = {
            "type": "process",
            "priority": "normal",
            "details": classification
        }

        return ProcessingResponse(
            classification=classification,
            processed_data=processed_data,
            action=action
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Process error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process/text", response_model=ProcessingResponse)
async def process_text(
    text_input: TextInput = Body(
        ...,
        description="Input text content",
        example={"text": "Enter your text here"}
    )
):
    """
    Process text content.
    
    This endpoint accepts text input and processes it.
    Returns processed data with classification and action details.
    """
    try:
        processed_data = await process_email(text_input.text)
        classification = await classify_input(str(processed_data))
        action = {
            "type": "process",
            "priority": "normal",
            "details": classification
        }
        return ProcessingResponse(
            classification=classification,
            processed_data=processed_data,
            action=action
        )
    except Exception as e:
        logger.error(f"Text processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process/json", response_model=ProcessingResponse)
async def process_json_endpoint(
    json_input: JsonInput = Body(
        ...,
        description="Input JSON data as string",
        example={"json_data": "{\"key\": \"value\"}"}
    )
):
    """
    Process JSON data.
    
    This endpoint accepts JSON string input and processes it.
    Returns processed data with classification and action details.
    """
    try:
        processed_data = await process_json(json_input.json_data)
        classification = await classify_input(str(processed_data))
        action = {
            "type": "process",
            "priority": "normal",
            "details": classification
        }
        return ProcessingResponse(
            classification=classification,
            processed_data=processed_data,
            action=action
        )
    except Exception as e:
        logger.error(f"JSON processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process/pdf", response_model=ProcessingResponse)
async def process_pdf_endpoint(
    file: UploadFile = File(
        ...,
        description="Upload a PDF file",
        example="example.pdf"
    )
):
    """
    Process PDF file.
    
    This endpoint accepts PDF file upload and processes it.
    Returns processed data with classification and action details.
    """
    try:
        logger.info(f"Received PDF file: {file.filename}")
        
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file name provided")
            
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
            
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed")
            
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Empty file provided")
            
        logger.info(f"Processing PDF file: {file.filename}")
        processed_data = await process_pdf(content)
        
        logger.info("Classifying processed data")
        classification = await classify_input(str(processed_data))
        
        action = {
            "type": "process",
            "priority": "normal",
            "details": classification
        }
        
        logger.info("Successfully processed PDF file")
        return ProcessingResponse(
            classification=classification,
            processed_data=processed_data,
            action=action
        )
    except HTTPException as he:
        logger.error(f"HTTP Exception: {str(he)}")
        raise he
    except Exception as e:
        logger.error(f"PDF processing error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        logger.info("Health check endpoint called")
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the frontend application."""
    return FileResponse("frontend/build/index.html")

@app.get("/{path:path}", response_class=HTMLResponse)
async def catch_all(path: str):
    """Catch all routes to serve the frontend application."""
    return FileResponse("frontend/build/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server:app",  # Use the import string format
        host="127.0.0.1",
        port=8000,  # Changed to 8000 to match the frontend expectation
        reload=True,
        workers=1
    ) 