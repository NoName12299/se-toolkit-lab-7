"""Tool definitions for LLM function calling"""

import json
from typing import Dict, Any, List
from services.lms_client import lms_client


# Tool schemas for LLM
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_items",
            "description": "Get all items (labs and tasks). Returns list of labs with their titles.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_learners",
            "description": "Get enrolled students. Returns total count and list of students.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pass_rates",
            "description": "Get per-task pass rates for a specific lab. Returns task names and percentages.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g., 'lab-01', 'lab-02', 'lab-03', 'lab-04', 'lab-05', 'lab-06'"
                    }
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_scores",
            "description": "Get score distribution (4 buckets: 0-50, 50-70, 70-90, 90-100) for a lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g., 'lab-01'"
                    }
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_timeline",
            "description": "Get submissions timeline (per day) for a lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g., 'lab-01'"
                    }
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_groups",
            "description": "Get per-group performance for a lab. Returns group names and their average scores.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g., 'lab-01'"
                    }
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_learners",
            "description": "Get top N learners by score for a lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g., 'lab-01'"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of top learners to return (default 5)"
                    }
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_completion_rate",
            "description": "Get completion rate percentage for a lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g., 'lab-01'"
                    }
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "trigger_sync",
            "description": "Trigger ETL sync to refresh data from autochecker. Use when data seems stale.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


# Tool executors - map tool names to actual functions
def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
    """
    Execute a tool and return formatted result
    """
    try:
        if tool_name == "get_items":
            items = lms_client.get_items()
            labs = [item for item in items if item.get("type") == "lab"]
            result = f"Found {len(items)} items total, {len(labs)} labs.\n\n"
            for lab in labs:
                title = lab.get("title", "Unknown")
                # Extract lab number from title
                import re
                match = re.search(r'Lab (\d+)', title)
                lab_num = match.group(1) if match else "??"
                result += f"- lab-{lab_num}: {title}\n"
            return result
            
        elif tool_name == "get_learners":
            learners = lms_client.get_learners()
            return f"Total enrolled students: {len(learners)}\n\nFirst few: {', '.join([l.get('name', 'Unknown') for l in learners[:5]])}"
            
        elif tool_name == "get_pass_rates":
            lab = arguments.get("lab")
            if not lab:
                return "Error: lab parameter required"
            rates = lms_client.get_pass_rates(lab)
            if not rates:
                return f"No pass rate data available for {lab}"
            result = f"Pass rates for {lab.upper()}:\n\n"
            for task, rate in rates.items():
                result += f"• {task}: {rate:.1f}%\n"
            return result
            
        elif tool_name == "get_scores":
            lab = arguments.get("lab")
            if not lab:
                return "Error: lab parameter required"
            scores = lms_client.get_scores(lab)
            return f"Score distribution for {lab.upper()}:\n{json.dumps(scores, indent=2)}"
            
        elif tool_name == "get_timeline":
            lab = arguments.get("lab")
            timeline = lms_client.get_timeline(lab)
            return f"Submissions timeline for {lab.upper()}:\n{json.dumps(timeline, indent=2)}"
            
        elif tool_name == "get_groups":
            lab = arguments.get("lab")
            groups = lms_client.get_groups(lab)
            return f"Group performance for {lab.upper()}:\n{json.dumps(groups, indent=2)}"
            
        elif tool_name == "get_top_learners":
            lab = arguments.get("lab")
            limit = arguments.get("limit", 5)
            learners = lms_client.get_top_learners(lab, limit)
            result = f"Top {limit} learners for {lab.upper()}:\n\n"
            for i, learner in enumerate(learners[:limit], 1):
                name = learner.get("name", "Unknown")
                score = learner.get("score", 0)
                result += f"{i}. {name}: {score:.1f}%\n"
            return result
            
        elif tool_name == "get_completion_rate":
            lab = arguments.get("lab")
            rate = lms_client.get_completion_rate(lab)
            return f"Completion rate for {lab.upper()}: {rate.get('completion_rate', 0):.1f}%"
            
        elif tool_name == "trigger_sync":
            result = lms_client.trigger_sync()
            return f"ETL sync triggered successfully. Loaded: {result}"
            
        else:
            return f"Unknown tool: {tool_name}"
            
    except Exception as e:
        return f"Error executing {tool_name}: {str(e)}"
