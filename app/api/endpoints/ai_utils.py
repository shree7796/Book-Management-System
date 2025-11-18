from fastapi import APIRouter, Depends, Body
from typing import Dict, Any

from app.ai_models.llm_client import llm_client
from app.api.dependencies import current_user # Requires authentication

router = APIRouter()

@router.post("/generate-summary", summary="Generate a summary for arbitrary content (Auth Required)")
async def generate_summary_for_content(
    title: str = Body(..., embed=True, description="Title of the content."),
    content: str = Body(..., embed=True, description="The full text content to summarize."),
    user = Depends(current_user) # Requires any authenticated user
) -> Dict[str, str]:
    """
    Generates a summary for a given book content using the Llama3 model.
    """
    summary = await llm_client.generate_book_summary(content, title)
    return {"summary": summary}