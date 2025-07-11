"""
Configuration management for Gwen Voice Assistant
Handles secure loading of API keys and settings from environment variables
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for secure settings management"""
    
    # === API Keys (loaded from environment variables) ===
    PORCUPINE_ACCESS_KEY = os.getenv('PORCUPINE_ACCESS_KEY')
    ELEVEN_API_KEY = os.getenv('ELEVEN_API_KEY')
    VOICE_ID = os.getenv('VOICE_ID', 'Vara1IkEw7vh5Hr5dT3C')  # Default voice ID
    
    # === File Paths ===
    WAKE_WORD_PATH = os.getenv('WAKE_WORD_PATH', 'hey-Gwen_en_windows_v3_0_0.ppn')
    LOG_FILE = os.getenv('LOG_FILE', 'gwen.log')
    APP_CACHE_FILE = os.getenv('APP_CACHE_FILE', 'app_cache.json')
    
    # === Audio Settings ===
    AUDIO_OUTPUT_FILE = 'output.mp3'
    ELEVEN_MODEL = os.getenv('ELEVEN_MODEL', 'eleven_monolingual_v1')
    
    # === Logging Settings ===
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # === Validation ===
    @classmethod
    def validate_config(cls):
        """Validate that all required configuration is present"""
        missing_vars = []
        
        if not cls.PORCUPINE_ACCESS_KEY:
            missing_vars.append('PORCUPINE_ACCESS_KEY')
        if not cls.ELEVEN_API_KEY:
            missing_vars.append('ELEVEN_API_KEY')
            
        if missing_vars:
            error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
            error_msg += "\nPlease check your .env file and ensure all required variables are set."
            raise ValueError(error_msg)
        
        # Check if wake word file exists
        if not os.path.exists(cls.WAKE_WORD_PATH):
            raise FileNotFoundError(f"Wake word file not found: {cls.WAKE_WORD_PATH}")
        
        return True
    
    @classmethod
    def get_log_level(cls):
        """Get logging level from config"""
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        return level_map.get(cls.LOG_LEVEL.upper(), logging.INFO)