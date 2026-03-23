"""LMS Backend API Client"""

import httpx
from typing import List, Dict, Any, Optional
from config import config


class LMSClient:
    """Client for LMS backend API"""
    
    def __init__(self):
        self.base_url = config.lms_api_url
        self.api_key = config.lms_api_key
        self.timeout = 10.0
        
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def get_items(self) -> List[Dict[str, Any]]:
        """Get all items (labs and tasks)"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/items/",
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
    
    async def get_learners(self) -> List[Dict[str, Any]]:
        """Get enrolled students"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/learners/",
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
    
    async def get_pass_rates(self, lab: str) -> Dict[str, Any]:
        """Get pass rates for a specific lab"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/analytics/pass-rates",
                params={"lab": lab},
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
    
    async def get_scores(self, lab: str) -> Dict[str, Any]:
        """Get score distribution for a lab"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/analytics/scores",
                params={"lab": lab},
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
    
    async def check_health(self) -> Dict[str, Any]:
        """Check if backend is healthy by fetching items"""
        try:
            items = await self.get_items()
            return {
                "healthy": True,
                "item_count": len(items),
                "error": None
            }
        except Exception as e:
            return {
                "healthy": False,
                "item_count": 0,
                "error": str(e)
            }
    
    async def get_labs(self) -> List[str]:
        """Get list of lab names from items"""
        items = await self.get_items()
        labs = []
        for item in items:
            if item.get("type") == "lab" and "lab-" in item.get("name", ""):
                labs.append(item.get("name"))
        return sorted(labs)
