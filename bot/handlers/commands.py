"""Command handlers for the Telegram bot - Synchronous version"""

from typing import Optional
from services.lms_client import lms_client


def handle_start() -> str:
    """Handle /start command"""
    return (
        "🤖 Welcome to the LMS Bot!\n\n"
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
        "📋 Available commands:\n\n"
        "/start - Welcome message\n"
        "/help - Show this help\n"
        "/health - Check backend status\n"
        "/labs - List all labs\n"
        "/scores <lab> - Show scores for a lab\n\n"
        "Examples:\n"
        "• /scores lab-01\n"
        "• /scores lab-02\n"
        "• /scores lab-03\n"
        "• /scores lab-04\n"
        "• /scores lab-05\n"
        "• /scores lab-06\n\n"
        "You can also ask questions like:\n"
        "• 'Show me lab scores'\n"
        "• 'What's the health status?'\n"
        "• 'Which labs are available?'"
    )


def handle_health() -> str:
    """Get backend health status"""
    try:
        result = lms_client.check_health()
        if result["healthy"]:
            return f"✅ Backend is healthy. {result['item_count']} items available."
        else:
            error_msg = result["error"]
            if "Connection refused" in error_msg or "connect" in error_msg.lower():
                return f"❌ Backend error: connection refused ({lms_client.base_url}). Check that services are running."
            elif "401" in error_msg or "Unauthorized" in error_msg:
                return "❌ Backend error: authentication failed. Check your LMS_API_KEY."
            elif "404" in error_msg:
                return "❌ Backend error: endpoint not found. Check API URL."
            else:
                return f"❌ Backend error: {error_msg}"
    except Exception as e:
        return f"❌ Backend error: {str(e)}"


def handle_labs() -> str:
    """List all available labs"""
    try:
        labs = lms_client.get_labs()
        
        if not labs:
            return "📚 No labs found in the system. Please run ETL sync first."
        
        result = "📚 **Available Labs**\n\n"
        for lab in labs:
            lab_num = lab.replace("lab-", "").upper()
            result += f"• `{lab}` (Lab {lab_num})\n"
        
        return result
    except Exception as e:
        error_msg = str(e)
        if "Connection refused" in error_msg:
            return f"❌ Cannot connect to backend ({lms_client.base_url}). Please check if services are running."
        elif "401" in error_msg:
            return "❌ Authentication failed. Check your LMS_API_KEY in .env.bot.secret"
        else:
            return f"❌ Failed to fetch labs: {error_msg}"


def handle_scores(lab_name: Optional[str] = None) -> str:
    """Get scores for a specific lab"""
    if not lab_name:
        return "❌ Please specify a lab name.\nExample: /scores lab-04\n\nAvailable labs: lab-01, lab-02, lab-03, lab-04, lab-05, lab-06"
    
    # Clean up lab name
    if lab_name.startswith("/scores"):
        parts = lab_name.split()
        lab_name = parts[1] if len(parts) > 1 else None
        if not lab_name:
            return "❌ Please specify a lab name.\nExample: /scores lab-04"
    
    try:
        # Verify lab exists
        labs = lms_client.get_labs()
        if lab_name not in labs:
            available = ", ".join(labs[:5])
            if len(labs) > 5:
                available += "..."
            return f"❌ Lab '{lab_name}' not found.\nAvailable labs: {available}"
        
        # Get pass rates
        pass_rates = lms_client.get_pass_rates(lab_name)
        
        if not pass_rates:
            return f"📊 No pass rate data available for {lab_name.upper()}."
        
        # Format the response
        result = f"📊 **Pass Rates for {lab_name.upper()}**\n\n"
        
        for task_name, avg_score in pass_rates.items():
            # Format with one decimal place
            result += f"• **{task_name}**: {avg_score:.1f}%\n"
        
        return result
        
    except Exception as e:
        error_msg = str(e)
        if "Connection refused" in error_msg:
            return f"❌ Cannot connect to backend ({lms_client.base_url}). Please check if services are running."
        elif "401" in error_msg:
            return "❌ Authentication failed. Check your LMS_API_KEY in .env.bot.secret"
        elif "404" in error_msg:
            return f"❌ Lab '{lab_name}' not found or no data available."
        else:
            return f"❌ Failed to fetch scores: {error_msg}"


def handle_unknown(command: str) -> str:
    """Handle unknown commands"""
    return f"❌ Unknown command: {command}\nType /help to see available commands."
