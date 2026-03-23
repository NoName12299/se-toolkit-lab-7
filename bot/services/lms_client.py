"""LMS Backend API Client - Synchronous version for --test mode"""

import httpx
from typing import List, Dict, Any, Optional
from config import config


class LMSClient:
    """Synchronous client for LMS backend API"""
    
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
    
    def get_items(self) -> List[Dict[str, Any]]:
        """Get all items (labs and tasks)"""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/items/",
                    headers=self._get_headers()
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise Exception(f"Failed to fetch items: {str(e)}")
    
    def get_labs(self) -> List[str]:
        """Get list of lab names from items"""
        try:
            items = self.get_items()
            labs = []
            for item in items:
                if item.get("type") == "lab":
                    # Get name from title or id
                    if "title" in item:
                        # Extract lab name from title, e.g., "Lab 01 – Products" -> "lab-01"
                        title = item.get("title", "")
                        if "Lab" in title:
                            # Extract number
                            import re
                            match = re.search(r'Lab (\d+)', title)
                            if match:
                                lab_num = match.group(1)
                                labs.append(f"lab-{lab_num}")
            return sorted(labs)
        except Exception as e:
            print(f"Error fetching labs: {e}")
            return []
    
    def get_pass_rates(self, lab: str) -> Dict[str, Any]:
        """Get pass rates for a specific lab"""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/analytics/pass-rates",
                    params={"lab": lab},
                    headers=self._get_headers()
                )
                response.raise_for_status()
                data = response.json()
                
                # Convert list of tasks to dict
                result = {}
                for task_data in data:
                    task_name = task_data.get("task", "")
                    avg_score = task_data.get("avg_score", 0)
                    attempts = task_data.get("attempts", 0)
                    result[task_name] = avg_score
                
                return result
        except Exception as e:
            raise Exception(f"Failed to fetch pass rates: {str(e)}")
    
    def check_health(self) -> Dict[str, Any]:
        """Check if backend is healthy by fetching items"""
        try:
            items = self.get_items()
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


# Создаем глобальный экземпляр
lms_client = LMSClient()
