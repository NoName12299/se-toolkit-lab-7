"""Command handlers for the Telegram bot"""

from typing import Optional
import asyncio
from services.lms_client import LMSClient


lms_client = LMSClient()


def handle_start() -> str:
    """Handle /start command"""
    return (
        "Welcome to the LMS Bot!\n\n"
        "I can help you with:\n"
        "• Check system health: /health\n"
        "• List available labs: /labs\n"
        "• Get lab scores: /scores <lab-name>\n"
        "• Ask questions in plain language\n\n"
        "Type /help to see all commands."
    )


def handle_help() -> str:
    """Handle /help command"""
    return (
        "Available commands:\n\n"
        "/start - Welcome message\n"
        "/help - Show this help\n"
        "/health - Check backend status\n"
        "/labs - List all labs\n"
        "/scores <lab> - Show scores for a lab\n\n"
        "Examples:\n"
        "• /scores lab-04\n"
        "• /scores lab-01\n\n"
        "You can also ask questions like:\n"
        "• 'Show me lab scores'\n"
        "• 'What's the health status?'\n"
        "• 'Which labs are available?'"
    )


async def handle_health_async() -> str:
    """Get backend health status"""
    try:
        result = await lms_client.check_health()
        if result["healthy"]:
            return f"Backend is healthy. {result['item_count']} items available."
        else:
            # Friendly error with actual error message
            error_msg = result["error"]
            if "Connection refused" in error_msg or "connect" in error_msg.lower():
                return f"Backend error: connection refused ({lms_client.base_url}). Check that services are running."
            elif "401" in error_msg or "Unauthorized" in error_msg:
                return "Backend error: authentication failed. Check your LMS_API_KEY."
            elif "404" in error_msg:
                return "Backend error: endpoint not found. Check API URL."
            else:
                return f"Backend error: {error_msg}"
    except Exception as e:
        return f"Backend error: {str(e)}"


def handle_health() -> str:
    """Synchronous wrapper for health check"""
    return asyncio.run(handle_health_async())


async def handle_labs_async() -> str:
    """List all available labs"""
    try:
        labs = await lms_client.get_labs()
        
        if not labs:
            return "No labs found in the system. Please run ETL sync first."
        
        result = "Available labs:\n\n"
        for lab in labs:
            # Format lab name nicely
            lab_num = lab.replace("lab-", "").upper()
            result += f"• {lab.upper()} — Lab {lab_num}\n"
        
        return result
    except Exception as e:
        error_msg = str(e)
        if "Connection refused" in error_msg:
            return f"Cannot connect to backend ({lms_client.base_url}). Please check if services are running."
        elif "401" in error_msg:
            return "Authentication failed. Check your LMS_API_KEY in .env.bot.secret"
        else:
            return f"Failed to fetch labs: {error_msg}"


def handle_labs() -> str:
    """Synchronous wrapper for labs"""
    return asyncio.run(handle_labs_async())


async def handle_scores_async(lab_name: Optional[str] = None) -> str:
    """Get scores for a specific lab"""
    if not lab_name:
        return "Please specify a lab name. Example: /scores lab-04"
    
    # Normalize lab name (remove /scores prefix if present)
    if lab_name.startswith("/scores"):
        parts = lab_name.split()
        lab_name = parts[1] if len(parts) > 1 else None
        if not lab_name:
            return "Please specify a lab name. Example: /scores lab-04"
    
    try:
        # First verify lab exists
        labs = await lms_client.get_labs()
        if lab_name not in labs:
            available = ", ".join(labs[:5])
            return f"Lab '{lab_name}' not found. Available labs: {available}"
        
        # Get pass rates
        pass_rates = await lms_client.get_pass_rates(lab_name)
        
        if not pass_rates:
            return f"No data available for {lab_name}."
        
        # Format the response
        result = f"Pass rates for {lab_name.upper()}:\n\n"
        
        # pass_rates is a dict like {"task_name": percentage}
        for task_name, percentage in pass_rates.items():
            if isinstance(percentage, (int, float)):
                result += f"• {task_name}: {percentage:.1f}%\n"
            else:
                result += f"• {task_name}: {percentage}\n"
        
        return result
        
    except Exception as e:
        error_msg = str(e)
        if "Connection refused" in error_msg:
            return f"Cannot connect to backend ({lms_client.base_url}). Please check if services are running."
        elif "401" in error_msg:
            return "Authentication failed. Check your LMS_API_KEY in .env.bot.secret"
        elif "404" in error_msg:
            return f"Lab '{lab_name}' not found or no data available."
        else:
            return f"Failed to fetch scores: {error_msg}"


def handle_scores(lab_name: Optional[str] = None) -> str:
    """Synchronous wrapper for scores"""
    return asyncio.run(handle_scores_async(lab_name))


def handle_unknown(command: str) -> str:
    """Handle unknown commands"""
    return f"Unknown command: {command}\nType /help to see available commands."
