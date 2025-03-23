from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Dict, List, Optional
from app.services.ai_processor import AIProcessor
from app.models.request_models import GenerateRequest, StreamGenerateRequest
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.get("/")
async def get_available_providers(request: Request) -> Dict[str, str]:
    """Get all available LLM providers
    
    Returns:
        Dictionary of provider names to model names
    """
    ai_processor: AIProcessor = request.app.state.ai_processor
    return ai_processor.get_available_providers()


@router.post("/generate")
async def generate_response(request: Request, generate_request: GenerateRequest):
    """Generate a response using a specific LLM provider
    
    Args:
        generate_request: The request containing system prompt, user prompt, and optional provider name
        
    Returns:
        The generated response
    """
    ai_processor: AIProcessor = request.app.state.ai_processor
    
    try:
        response = await ai_processor.generate_response(
            generate_request.system_prompt,
            generate_request.user_prompt,
            generate_request.role_id,
            generate_request.provider_name
        )
        
        return {"response": response}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")


@router.post("/generate/stream")
async def generate_response_stream(request: Request, stream_request: StreamGenerateRequest):
    """Generate a streaming response using a specific LLM provider
    
    Args:
        stream_request: The request containing system prompt, user prompt, and optional provider name
        
    Returns:
        A streaming response with the generated content
    """
    ai_processor: AIProcessor = request.app.state.ai_processor
    
    async def generate_stream():
        try:
            async for chunk in ai_processor.generate_response_stream(
                stream_request.system_prompt,
                stream_request.user_prompt,
                stream_request.role_id,
                stream_request.provider_name
            ):
                yield f"data: {chunk}\n\n"
        except ValueError as e:
            yield f"data: Error: {str(e)}\n\n"
        except Exception as e:
            yield f"data: Error generating response: {str(e)}\n\n"
    
    return StreamingResponse(generate_stream(), media_type="text/event-stream")
