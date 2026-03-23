"""Command handlers for the Telegram bot"""

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
        "You can also ask questions like:\n"
        "• 'Show me lab scores'\n"
        "• 'What's the health status?'\n"
        "• 'Which labs are available?'"
    )

def handle_health() -> str:
    """Handle /health command"""
    # Placeholder - will be implemented in Task 2
    return "Backend is operational (placeholder - real implementation in Task 2)"

def handle_labs() -> str:
    """Handle /labs command"""
    # Placeholder - will be implemented in Task 2
    return "Available labs: lab-01, lab-02, lab-03, lab-04, lab-05, lab-06 (placeholder)"

def handle_scores(lab_name: str = None) -> str:
    """Handle /scores command"""
    if not lab_name:
        return "Please specify a lab name. Example: /scores lab-04"
    
    # Placeholder - will be implemented in Task 2
    return f"Scores for {lab_name}: Not implemented yet (Task 2)"

def handle_unknown(command: str) -> str:
    """Handle unknown commands"""
    return f"Unknown command: {command}\nType /help to see available commands."
