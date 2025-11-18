import httpx
from app.core.config import settings
from typing import Optional, Dict, Any

# Define the model to use from configuration
MODEL = settings.LLM_MODEL_NAME
BASE_URL = settings.LLM_BASE_URL

class LLMClient:
    """
    Asynchronous client for interacting with the local Llama3 model via the Ollama API.
    """
    def __init__(self):
        # Ollama's API endpoint for generating completions
        self.generate_url = f"{BASE_URL}/api/generate"
        self.http_client = httpx.AsyncClient(timeout=60.0) # Set a generous timeout

    async def _generate_text(self, prompt: str) -> Optional[str]:
        """Internal function to call the Ollama generate API."""
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "stream": False # Don't stream, wait for the full response
        }
        
        try:
            # POST request to the Ollama server
            response = await self.http_client.post(self.generate_url, json=payload)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            
            # Ollama response structure: {"model": "...", "response": "..."}
            data = response.json()
            return data.get("response", "").strip()

        except httpx.RequestError as e:
            # Handle connection errors (e.g., Ollama server is down)
            print(f"LLM Connection Error: {e}")
            return f"Error: Failed to connect to LLM server. ({e})"
        except Exception as e:
            print(f"LLM Generation Error: {e}")
            return f"Error: LLM generation failed. ({e})"

    async def generate_book_summary(self, content: str, title: str) -> Optional[str]:
        """Generate a summary for a new book entry based on its content."""
        prompt = (
            f"You are a professional book summarizer. Summarize the following book content "
            f"for the book titled '{title}' in approximately 150 words. Content: {content}"
        )
        return await self._generate_text(prompt)

    async def generate_review_summary(self, reviews_text: str) -> Optional[str]:
        """Generate an aggregated summary of all reviews for a book."""
        prompt = (
            f"You are a critical review analyst. Based on the following user reviews, "
            f"provide a concise, neutral summary of the overall sentiment and common themes. "
            f"Reviews: {reviews_text}"
        )
        return await self._generate_text(prompt)

# Instantiate the client once
llm_client = LLMClient()