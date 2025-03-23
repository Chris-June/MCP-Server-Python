from fastapi import APIRouter, Depends, Request, HTTPException, Response, File, UploadFile, Form
from typing import List, Optional, AsyncGenerator, Dict, Any
from fastapi.responses import StreamingResponse
import base64
from app.models.multimodal import MultiModalContent, MultiModalProcessRequest, MultiModalProcessResponse
from app.services.multimodal_processor import MultiModalProcessor
from app.services.role_service import RoleService

router = APIRouter(prefix="/multimodal")

async def get_multimodal_processor(request: Request) -> MultiModalProcessor:
    """Dependency for getting the multi-modal processor"""
    return request.app.state.multimodal_processor

async def get_role_service(request: Request) -> RoleService:
    """Dependency for getting the role service"""
    return request.app.state.role_service

@router.post("/process", response_model=MultiModalProcessResponse, summary="Process multi-modal content using a specific role")
async def process_multimodal_content(
    request: MultiModalProcessRequest,
    multimodal_processor: MultiModalProcessor = Depends(get_multimodal_processor),
    role_service: RoleService = Depends(get_role_service)
):
    """Process multi-modal content using a specific role"""
    # Get the role to use its system prompt
    role = await role_service.get_role(request.role_id)
    
    # Prepare the system prompt with any custom instructions
    system_prompt = role.system_prompt
    if request.custom_instructions:
        system_prompt += f"\n\nAdditional Instructions: {request.custom_instructions}"
    
    # Process the multi-modal content
    response_text = await multimodal_processor.process_multimodal_content(
        system_prompt,
        request.content
    )
    
    # Prepare information about processed media
    processed_media = []
    if request.content.media:
        for i, media in enumerate(request.content.media):
            processed_media.append({
                "index": i,
                "type": media.type,
                "processed": True,
                "alt_text": media.alt_text
            })
    
    return MultiModalProcessResponse(
        role_id=request.role_id,
        response=response_text,
        processed_media=processed_media
    )

async def generate_multimodal_stream_response(
    role_id: str,
    content: MultiModalContent,
    custom_instructions: Optional[str],
    multimodal_processor: MultiModalProcessor,
    role_service: RoleService
) -> AsyncGenerator[str, None]:
    """Generate a streaming response for multi-modal content"""
    # Get the role to use its system prompt
    role = await role_service.get_role(role_id)
    
    # Prepare the system prompt with any custom instructions
    system_prompt = role.system_prompt
    if custom_instructions:
        system_prompt += f"\n\nAdditional Instructions: {custom_instructions}"
    
    # Process the multi-modal content with streaming
    async for chunk in multimodal_processor.process_multimodal_content_stream(system_prompt, content):
        yield f"data: {chunk}\n\n"
    yield "data: [DONE]\n\n"

@router.post("/process/stream", summary="Process multi-modal content using a specific role with streaming response")
async def process_multimodal_content_stream(
    request: MultiModalProcessRequest,
    multimodal_processor: MultiModalProcessor = Depends(get_multimodal_processor),
    role_service: RoleService = Depends(get_role_service)
):
    """Process multi-modal content using a specific role with streaming response"""
    return StreamingResponse(
        generate_multimodal_stream_response(
            request.role_id,
            request.content,
            request.custom_instructions,
            multimodal_processor,
            role_service
        ),
        media_type="text/event-stream"
    )

@router.post("/upload", summary="Upload a file for multi-modal processing")
async def upload_file(
    file: UploadFile = File(...),
    description: str = Form(None)
):
    """Upload a file for multi-modal processing"""
    try:
        # Read the file content
        file_content = await file.read()
        
        # Encode the file content as base64
        base64_content = base64.b64encode(file_content).decode("utf-8")
        
        # Determine the file type
        content_type = file.content_type or "application/octet-stream"
        
        return {
            "filename": file.filename,
            "content_type": content_type,
            "size": len(file_content),
            "base64_data": base64_content,
            "description": description
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@router.post("/analyze/image", summary="Analyze an image with a specific prompt")
async def analyze_image(
    image_url: str = Form(...),
    prompt: str = Form(...),
    multimodal_processor: MultiModalProcessor = Depends(get_multimodal_processor)
):
    """Analyze an image with a specific prompt"""
    try:
        result = await multimodal_processor.analyze_image(image_url, prompt)
        return {"analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing image: {str(e)}")
