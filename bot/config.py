from pydantic_settings import BaseSettings
from pydantic import Field
import os

class BotConfig(BaseSettings):
    """Configuration for the Telegram bot"""
    
    # Telegram settings
    bot_token: str = Field(default="", alias="BOT_TOKEN")
    
    # LMS backend settings
    lms_api_url: str = Field(default="http://localhost:42002", alias="LMS_API_URL")
    lms_api_key: str = Field(default="", alias="LMS_API_KEY")
    
    # LLM settings (for Task 3)
    llm_api_key: str = Field(default="", alias="LLM_API_KEY")
    llm_api_base_url: str = Field(default="http://localhost:42005/v1", alias="LLM_API_BASE_URL")
    llm_api_model: str = Field(default="coder-model", alias="LLM_API_MODEL")
    
    class Config:
        env_file = ".env.bot.secret"
        env_file_encoding = "utf-8"
        extra = "ignore"

# Create a singleton instance
config = BotConfig()
