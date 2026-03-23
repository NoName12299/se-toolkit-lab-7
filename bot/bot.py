#!/usr/bin/env python3
"""
Telegram bot entry point with --test mode for offline verification
"""

import sys
import argparse
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers.commands import (
    handle_start, handle_help, handle_health,
    handle_labs, handle_scores, handle_unknown
)
from handlers.natural_language import handle_message
from config import config


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Telegram Bot")
    parser.add_argument(
        "--test",
        metavar="COMMAND",
        help="Test mode: run command and print response to stdout"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print debug info to stderr"
    )
    return parser.parse_args()


def process_command_test_mode(command: str, debug: bool = False) -> str:
    """
    Process a command in test mode (no Telegram connection)
    Returns the response text
    """
    command = command.strip()
    
    # Parse command and arguments
    parts = command.split(maxsplit=1)
    cmd = parts[0].lower() if parts else ""
    args = parts[1] if len(parts) > 1 else ""
    
    # Route to appropriate handler
    if cmd == "/start":
        return handle_start()
    elif cmd == "/help":
        return handle_help()
    elif cmd == "/health":
        return handle_health()
    elif cmd == "/labs":
        return handle_labs()
    elif cmd == "/scores":
        return handle_scores(args if args else None)
    elif cmd.startswith("/"):
        return handle_unknown(command)
    else:
        # Natural language query
        response = handle_message(command, debug=debug)
        return response if response else handle_unknown(command)


async def message_handler(update, context):
    """Handle regular text messages (not commands)"""
    user_message = update.message.text
    response = handle_message(user_message, debug=False)
    
    if response:
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("I'm not sure how to help. Try /help for commands.")


def main():
    """Main entry point"""
    args = parse_args()
    
    # Test mode
    if args.test:
        response = process_command_test_mode(args.test, debug=args.debug)
        print(response)
        sys.exit(0)
    
    # Normal mode - run Telegram bot
    print("Starting Telegram bot...")
    
    # Check if token is configured
    if not config.bot_token:
        print("❌ ERROR: BOT_TOKEN not set in .env.bot.secret")
        print("Please create .env.bot.secret with BOT_TOKEN=<your-token>")
        sys.exit(1)
    
    # Create application
    application = Application.builder().token(config.bot_token).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text(handle_start())))
    application.add_handler(CommandHandler("help", lambda u, c: u.message.reply_text(handle_help())))
    application.add_handler(CommandHandler("health", lambda u, c: u.message.reply_text(handle_health())))
    application.add_handler(CommandHandler("labs", lambda u, c: u.message.reply_text(handle_labs())))
    application.add_handler(CommandHandler("scores", lambda u, c: u.message.reply_text(handle_scores(" ".join(c.args) if c.args else None))))
    
    # Add message handler for natural language
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    # Start the bot
    print("✅ Bot is running. Press Ctrl+C to stop.")
    print("   Now you can ask questions like:")
    print("   - 'what labs are available?'")
    print("   - 'show me scores for lab 4'")
    print("   - 'which lab has the lowest pass rate?'")
    application.run_polling()


if __name__ == "__main__":
    main()
