#!/usr/bin/env python3
"""
Telegram bot entry point with --test mode for offline verification
"""

import sys
import argparse
import asyncio
from telegram.ext import Application, CommandHandler
from handlers.commands import (
    handle_start, handle_help, handle_health, handle_health_async,
    handle_labs, handle_labs_async, handle_scores, handle_scores_async,
    handle_unknown
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
        # For test mode, we need to run async function
        return asyncio.run(handle_health_async())
    elif cmd == "/labs":
        return asyncio.run(handle_labs_async())
    elif cmd == "/scores":
        return asyncio.run(handle_scores_async(args if args else None))
    else:
        return handle_unknown(command)


async def health_callback(update, context):
    """Telegram handler for /health"""
    response = await handle_health_async()
    await update.message.reply_text(response)


async def labs_callback(update, context):
    """Telegram handler for /labs"""
    response = await handle_labs_async()
    await update.message.reply_text(response)


async def scores_callback(update, context):
    """Telegram handler for /scores"""
    lab_name = " ".join(context.args) if context.args else None
    response = await handle_scores_async(lab_name)
    await update.message.reply_text(response)


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
        print("❌ ERROR: BOT_TOKEN not set in .env.bot.secret")
        print("Please create .env.bot.secret with BOT_TOKEN=<your-token>")
        sys.exit(1)
    
    # Create application
    application = Application.builder().token(config.bot_token).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text(handle_start())))
    application.add_handler(CommandHandler("help", lambda u, c: u.message.reply_text(handle_help())))
    application.add_handler(CommandHandler("health", health_callback))
    application.add_handler(CommandHandler("labs", labs_callback))
    application.add_handler(CommandHandler("scores", scores_callback))
    
    # Start the bot
    print("✅ Bot is running. Press Ctrl+C to stop.")
    application.run_polling()


if __name__ == "__main__":
    main()
