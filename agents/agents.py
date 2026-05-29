from pydantic import BaseModel
from typing import Dict, Any

class ClassificationResult(BaseModel):
    format: str
    intent: str
    confidence: float
    risk_level: str
    requires_escalation: bool

class ClassifierAgent:
    async def classify(self, content: str) -> ClassificationResult:
        # Simple classification that always raises an error
        raise Exception("Classification failed")

class JSONAgent:
    async def process(self, content: str) -> Dict[str, Any]:
        raise Exception("JSON processing failed")

class EmailParserAgent:
    async def parse(self, content: str) -> Dict[str, Any]:
        raise Exception("Email parsing failed")

class PDFAgent:
    async def parse(self, content: bytes) -> Dict[str, Any]:
        raise Exception("PDF parsing failed")

class ActionRouter:
    async def route_action(self, result: Dict[str, Any], classification: ClassificationResult) -> Dict[str, Any]:
        return {"type": None, "action": None}

    async def close(self):
        pass 