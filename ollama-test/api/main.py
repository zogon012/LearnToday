from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx
import os
import json
from typing import Optional
import asyncio

app = FastAPI(title="Local LLM Chatbot", version="1.0.0")

# Ollama URL from environment variable
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

class ChatMessage(BaseModel):
    message: str
    model: Optional[str] = "smollm2:1.7b"

class ChatResponse(BaseModel):
    response: str
    model: str

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "OK", "message": "Local LLM Chatbot API is running"}

@app.get("/models")
async def list_models():
    """List available models in Ollama"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OLLAMA_URL}/api/tags")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch models: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat(chat_message: ChatMessage):
    """Send message to LLM and get response"""
    try:
        payload = {
            "model": chat_message.model,
            "prompt": chat_message.message,
            "stream": False,
            "options": {
                "num_predict": 50,
                "temperature": 0.3,
                "top_p": 0.5,
                "num_ctx": 512
            }
        }
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/generate", 
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            
            return ChatResponse(
                response=result.get("response", "No response generated"),
                model=chat_message.model
            )
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="LLM response timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Check if Ollama service is accessible"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OLLAMA_URL}/api/version")
            if response.status_code == 200:
                return {"status": "healthy", "ollama": "connected"}
            else:
                return {"status": "degraded", "ollama": "unreachable"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.post("/chat/stream")
async def chat_stream(chat_message: ChatMessage):
    """Send message to LLM and get streaming response"""
    async def generate():
        try:
            payload = {
                "model": chat_message.model,
                "prompt": chat_message.message,
                "stream": True,
                "options": {
                    "num_predict": 50,
                    "temperature": 0.3,
                    "top_p": 0.5,
                    "num_ctx": 512
                }
            }
            
            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream(
                    "POST", 
                    f"{OLLAMA_URL}/api/generate", 
                    json=payload
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                data = json.loads(line)
                                if "response" in data:
                                    yield f"data: {json.dumps({'content': data['response']})}\n\n"
                                if data.get("done"):
                                    yield f"data: {json.dumps({'done': True})}\n\n"
                                    break
                            except json.JSONDecodeError:
                                continue
                                
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/plain")