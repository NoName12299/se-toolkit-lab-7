"""Natural language intent router using LLM"""

import sys
from typing import List, Dict, Any
from services.llm_client import llm_client
from services.tools import TOOLS, execute_tool


SYSTEM_PROMPT = """You are an assistant for an LMS (Learning Management System). 
Users ask questions about labs, scores, students, and analytics.

You have access to these tools. ALWAYS use them to get real data:
- get_items: List all labs (call this first to see what labs exist)
- get_learners: Get enrolled students (returns count)
- get_pass_rates: Get per-task pass rates for a lab (shows percentages)
- get_scores: Get score distribution for a lab
- get_timeline: Get submissions timeline
- get_groups: Get group performance
- get_top_learners: Get top students
- get_completion_rate: Get completion percentage
- trigger_sync: Refresh data

IMPORTANT: 
1. ALWAYS use tools to fetch real data. NEVER guess or make up numbers.
2. For "show me scores for lab 4" -> call get_pass_rates with lab="lab-04"
3. For "how many students" -> call get_learners
4. For "which lab has the lowest pass rate" -> call get_items first, then get_pass_rates for each lab
5. Format answers with bullet points and percentages.
6. Include actual numbers from the API responses.

Example: When showing scores, format like:
• Task Name: 60.9% (X attempts)

Be helpful and conversational."""

def route_natural_language(user_message: str, debug: bool = False) -> str:
    """
    Route natural language query using LLM with tool calling
    
    Returns final response text
    """
    if debug:
        print(f"[debug] Routing: {user_message}", file=sys.stderr)
    
    # Initialize conversation
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]
    
    # Tool calling loop
    max_iterations = 5
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        
        if debug:
            print(f"[debug] Iteration {iteration}", file=sys.stderr)
        
        # Call LLM with current messages and tools
        try:
            response = llm_client.chat_completion(
                messages=messages,
                tools=TOOLS,
                tool_choice="auto"
            )
        except Exception as e:
            return f"Sorry, I'm having trouble connecting to the AI service. Error: {str(e)}"
        
        # Extract tool calls
        tool_calls = llm_client.extract_tool_calls(response)
        
        if not tool_calls:
            # No tool calls - return final response
            final_response = llm_client.get_response_text(response)
            if final_response:
                return final_response
            else:
                return "I'm not sure how to answer that. Try asking about labs, scores, or students."
        
        # Process each tool call
        for tool_call in tool_calls:
            tool_name = tool_call.get("function", {}).get("name", "")
            tool_args_str = tool_call.get("function", {}).get("arguments", "{}")
            
            # Parse arguments (might be JSON string)
            try:
                import json
                tool_args = json.loads(tool_args_str) if tool_args_str else {}
            except:
                tool_args = {}
            
            if debug:
                print(f"[debug] Tool called: {tool_name}({tool_args})", file=sys.stderr)
            
            # Execute tool
            tool_result = execute_tool(tool_name, tool_args)
            
            if debug:
                print(f"[debug] Tool result: {tool_result[:200]}...", file=sys.stderr)
            
            # Add tool result to conversation
            messages.append(response["choices"][0]["message"])
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.get("id", ""),
                "content": tool_result
            })
    
    return "I've tried to get the information but something went wrong. Please try again."


def is_slash_command(text: str) -> bool:
    """Check if text starts with a slash command"""
    return text.strip().startswith("/")


def handle_message(message: str, debug: bool = False) -> str:
    """
    Main entry point for message handling.
    If message is a slash command, it will be handled separately.
    Otherwise, use LLM routing.
    """
    if is_slash_command(message):
        # Slash commands handled elsewhere
        return None
    
    return route_natural_language(message, debug)
