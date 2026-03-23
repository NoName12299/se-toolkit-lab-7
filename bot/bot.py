#!/usr/bin/env python3
"""
Telegram bot entry point with --test mode for offline verification
"""

import sys
import argparse
import asyncio
from telegram.ext import Application, CommandHandler
from handlers.commands import (
    handle_start, handle_help, handle_health,
    handle_labs, handle_scores, handle_unknown
)
from config import config


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Telegram Bot")
    parser.add_argument(
        "--test",
        metavar="COMMAND",
        help="Test mode: run command and print response to stdout"
    )
    return parser.parse_args()


def process_command_test_mode(command: str) -> str:
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
    else:
        return handle_unknown(command)


def main():
    """Main entry point"""
    args = parse_args()
    
    # Test mode
    if args.test:
        response = process_command_test_mode(args.test)
        print(response)
        sys.exit(0)
    
    # Normal mode - run Telegram bot
    print("Starting Telegram bot...")
    
    # Check if token is configured
    if not config.bot_token:
        print("ERROR: BOT_TOKEN not set in .env.bot.secret")
        print("Please create .env.bot.secret with BOT_TOKEN=<your-token>")
        sys.exit(1)
    
    # Create application
    application = Application.builder().token(config.bot_token).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text(handle_start())))
    application.add_handler(CommandHandler("help", lambda u, c: u.message.reply_text(handle_help())))
    application.add_handler(CommandHandler("health", lambda u, c: u.message.reply_text(handle_health())))
    application.add_handler(CommandHandler("labs", lambda u, c: u.message.reply_text(handle_labs())))
    application.add_handler(CommandHandler("scores", lambda u, c: u.message.reply_text(
        handle_scores(" ".join(c.args) if c.args else None)
    )))
    
    # Start the bot
    print("Bot is running. Press Ctrl+C to stop.")
    application.run_polling()


if __name__ == "__main__":
    main()
