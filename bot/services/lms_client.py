"""LMS Backend API Client - Synchronous version for --test mode"""

import httpx
import re
import sys
from typing import List, Dict, Any, Optional, Tuple
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
        print(f"[API CALL] GET {self.base_url}/items/", file=sys.stderr)
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/items/",
                    headers=self._get_headers()
                )
                response.raise_for_status()
                result = response.json()
                print(f"[API RESPONSE] items: {len(result)}", file=sys.stderr)
                return result
        except Exception as e:
            print(f"[API ERROR] {str(e)}", file=sys.stderr)
            raise Exception(f"Failed to fetch items: {str(e)}")
    
    def get_learners(self) -> List[Dict[str, Any]]:
        """Get enrolled students"""
        print(f"[API CALL] GET {self.base_url}/learners/", file=sys.stderr)
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/learners/",
                    headers=self._get_headers()
                )
                response.raise_for_status()
                result = response.json()
                print(f"[API RESPONSE] learners: {len(result)}", file=sys.stderr)
                return result
        except Exception as e:
            print(f"[API ERROR] {str(e)}", file=sys.stderr)
            raise Exception(f"Failed to fetch learners: {str(e)}")
    
    def get_pass_rates(self, lab: str) -> Dict[str, Any]:
        """Get pass rates for a specific lab"""
        print(f"[API CALL] GET {self.base_url}/analytics/pass-rates?lab={lab}", file=sys.stderr)
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/analytics/pass-rates",
                    params={"lab": lab},
                    headers=self._get_headers()
                )
                response.raise_for_status()
                data = response.json()
                print(f"[API RESPONSE] pass rates: {len(data)} tasks", file=sys.stderr)
                
                # Convert list of tasks to dict
                result = {}
                for task_data in data:
                    task_name = task_data.get("task", "")
                    avg_score = task_data.get("avg_score", 0)
                    attempts = task_data.get("attempts", 0)
                    result[task_name] = avg_score
                
                return result
        except Exception as e:
            print(f"[API ERROR] {str(e)}", file=sys.stderr)
            raise Exception(f"Failed to fetch pass rates: {str(e)}")
    
    def get_scores(self, lab: str) -> Dict[str, Any]:
        """Get score distribution for a lab"""
        print(f"[API CALL] GET {self.base_url}/analytics/scores?lab={lab}", file=sys.stderr)
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/analytics/scores",
                    params={"lab": lab},
                    headers=self._get_headers()
                )
                response.raise_for_status()
                result = response.json()
                print(f"[API RESPONSE] scores received", file=sys.stderr)
                return result
        except Exception as e:
            print(f"[API ERROR] {str(e)}", file=sys.stderr)
            raise Exception(f"Failed to fetch scores: {str(e)}")
    
    def get_timeline(self, lab: str) -> Dict[str, Any]:
        """Get submissions timeline for a lab"""
        print(f"[API CALL] GET {self.base_url}/analytics/timeline?lab={lab}", file=sys.stderr)
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/analytics/timeline",
                    params={"lab": lab},
                    headers=self._get_headers()
                )
                response.raise_for_status()
                result = response.json()
                print(f"[API RESPONSE] timeline received", file=sys.stderr)
                return result
        except Exception as e:
            print(f"[API ERROR] {str(e)}", file=sys.stderr)
            raise Exception(f"Failed to fetch timeline: {str(e)}")
    
    def get_groups(self, lab: str) -> Dict[str, Any]:
        """Get group performance for a lab"""
        print(f"[API CALL] GET {self.base_url}/analytics/groups?lab={lab}", file=sys.stderr)
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/analytics/groups",
                    params={"lab": lab},
                    headers=self._get_headers()
                )
                response.raise_for_status()
                result = response.json()
                print(f"[API RESPONSE] groups received", file=sys.stderr)
                return result
        except Exception as e:
            print(f"[API ERROR] {str(e)}", file=sys.stderr)
            raise Exception(f"Failed to fetch groups: {str(e)}")
    
    def get_top_learners(self, lab: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top N learners for a lab"""
        print(f"[API CALL] GET {self.base_url}/analytics/top-learners?lab={lab}&limit={limit}", file=sys.stderr)
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/analytics/top-learners",
                    params={"lab": lab, "limit": limit},
                    headers=self._get_headers()
                )
                response.raise_for_status()
                result = response.json()
                print(f"[API RESPONSE] top learners: {len(result)}", file=sys.stderr)
                return result
        except Exception as e:
            print(f"[API ERROR] {str(e)}", file=sys.stderr)
            raise Exception(f"Failed to fetch top learners: {str(e)}")
    
    def get_completion_rate(self, lab: str) -> Dict[str, Any]:
        """Get completion rate for a lab"""
        print(f"[API CALL] GET {self.base_url}/analytics/completion-rate?lab={lab}", file=sys.stderr)
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/analytics/completion-rate",
                    params={"lab": lab},
                    headers=self._get_headers()
                )
                response.raise_for_status()
                result = response.json()
                print(f"[API RESPONSE] completion rate: {result}", file=sys.stderr)
                return result
        except Exception as e:
            print(f"[API ERROR] {str(e)}", file=sys.stderr)
            raise Exception(f"Failed to fetch completion rate: {str(e)}")
    
    def trigger_sync(self) -> Dict[str, Any]:
        """Trigger ETL sync"""
        print(f"[API CALL] POST {self.base_url}/pipeline/sync", file=sys.stderr)
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.base_url}/pipeline/sync",
                    headers=self._get_headers(),
                    json={}
                )
                response.raise_for_status()
                result = response.json()
                print(f"[API RESPONSE] sync: {result}", file=sys.stderr)
                return result
        except Exception as e:
            print(f"[API ERROR] {str(e)}", file=sys.stderr)
            raise Exception(f"Failed to trigger sync: {str(e)}")
    
    def get_labs(self) -> List[str]:
        """Get list of lab names (short form: lab-01, lab-02, etc.)"""
        try:
            items = self.get_items()
            labs = []
            for item in items:
                if item.get("type") == "lab":
                    if "title" in item:
                        title = item.get("title", "")
                        # Extract lab number from title
                        match = re.search(r'Lab (\d+)', title)
                        if match:
                            lab_num = match.group(1)
                            labs.append(f"lab-{lab_num}")
            return sorted(labs)
        except Exception as e:
            print(f"Error fetching labs: {e}", file=sys.stderr)
            return []
    
    def get_labs_with_titles(self) -> List[Tuple[str, str]]:
        """Get list of labs with both short name and full title"""
        try:
            items = self.get_items()
            labs = []
            for item in items:
                if item.get("type") == "lab":
                    if "title" in item:
                        title = item.get("title", "")
                        # Extract lab number from title
                        match = re.search(r'Lab (\d+)', title)
                        if match:
                            lab_num = match.group(1)
                            short_name = f"lab-{lab_num}"
                            # Clean up title (replace HTML entities)
                            clean_title = title.replace("–", "-").replace("—", "-")
                            labs.append((short_name, clean_title))
            return sorted(labs, key=lambda x: x[0])  # Sort by short_name
        except Exception as e:
            print(f"Error fetching labs: {e}", file=sys.stderr)
            return []
    
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
