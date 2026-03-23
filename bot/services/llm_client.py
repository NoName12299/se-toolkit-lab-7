"""LLM Client for Qwen Code API"""

import httpx
import json
from typing import List, Dict, Any, Optional
from config import config


class LLMClient:
    """Client for Qwen Code API with tool calling support"""
    
    def __init__(self):
        self.base_url = config.llm_api_base_url
        self.api_key = config.llm_api_key
        self.model = config.llm_api_model
        self.timeout = 30.0
        
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat_completion(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[str] = "auto"
    ) -> Dict[str, Any]:
        """
        Send chat completion request with optional tool support
        
        Returns the full API response
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = tool_choice
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self._get_headers(),
                    json=payload
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise Exception(f"LLM API error: {str(e)}")
    
    def extract_tool_calls(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract tool calls from LLM response
        Returns list of tool calls, each with name and arguments
        """
        message = response.get("choices", [{}])[0].get("message", {})
        return message.get("tool_calls", [])
    
    def get_response_text(self, response: Dict[str, Any]) -> str:
        """Extract text response from LLM"""
        return response.get("choices", [{}])[0].get("message", {}).get("content", "")


# Создаем глобальный экземпляр
llm_client = LLMClient()
