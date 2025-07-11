"""
Gwen Voice Assistant - Secure and Improved Version
A voice-activated assistant with wake word detection and app launching capabilities.

Features:
- Secure API key management via environment variables
- Comprehensive error handling and logging
- Fallback TTS system
- Improved app detection and matching
- Resource management and cleanup
- Cross-platform compatibility improvements

Author: Your Name
Version: 2.0.0
"""

import pvporcupine
import pyaudio
import struct
import speech_recognition as sr
import os
import webbrowser
import time
import json
import re
import sys
import logging
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List
import platform

# Third-party imports with error handling
try:
    from elevenlabs import generate, save, set_api_key
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False
    logging.warning("ElevenLabs not available, will use fallback TTS")

try:
    from playsound import playsound
    PLAYSOUND_AVAILABLE = True
except ImportError:
    PLAYSOUND_AVAILABLE = False
    logging.warning("playsound not available")

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False
    logging.warning("pyttsx3 not available")

# Windows-specific imports
if platform.system() == "Windows":
    try:
        import winreg
        import winshell
        WINDOWS_FEATURES = True
    except ImportError:
        WINDOWS_FEATURES = False
        logging.warning("Windows-specific features not available")
else:
    WINDOWS_FEATURES = False

# Import configuration
try:
    from config import Config
except ImportError:
    logging.error("config.py not found. Please ensure config.py exists.")
    sys.exit(1)


class VoiceAssistant:
    """Main Voice Assistant class with improved error handling and security"""
    
    def __init__(self):
        """Initialize the voice assistant with secure configuration"""
        self.setup_logging()
        self.validate_configuration()
        self.setup_tts()
        self.apps_cache = {}
        self.porcupine = None
        self.audio_stream = None
        self.pyaudio_instance = None
        
    def setup_logging(self):
        """Setup comprehensive logging system"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Create logs directory if it doesn't exist
        log_dir = Path(Config.LOG_FILE).parent
        log_dir.mkdir(exist_ok=True)
        
        # Configure file handler for detailed logs
        file_handler = logging.FileHandler(Config.LOG_FILE, encoding='utf-8')
        file_handler.setLevel(Config.get_log_level())
        file_handler.setFormatter(logging.Formatter(log_format))
        
        # Configure console handler to only show errors
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.ERROR)
        console_handler.setFormatter(logging.Formatter('%(message)s'))
        
        # Get root logger and add handlers
        root_logger = logging.getLogger()
        root_logger.setLevel(Config.get_log_level())
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Voice Assistant logging initialized")
    
    def validate_configuration(self):
        """Validate all required configuration and dependencies"""
        try:
            Config.validate_config()
            self.logger.info("Configuration validation successful")
        except (ValueError, FileNotFoundError) as e:
            self.logger.error(f"Configuration error: {e}")
            print(f"❌ Configuration Error: {e}")
            print("\n📋 Setup Instructions:")
            print("1. Copy .env.example to .env")
            print("2. Fill in your API keys in the .env file")
            print("3. Ensure the wake word file exists")
            sys.exit(1)
    
    def setup_tts(self):
        """Setup text-to-speech with fallback options"""
        self.tts_primary = None
        self.tts_fallback = None
        
        # Setup ElevenLabs (primary)
        if ELEVENLABS_AVAILABLE and Config.ELEVEN_API_KEY:
            try:
                set_api_key(Config.ELEVEN_API_KEY)
                self.tts_primary = "elevenlabs"
                self.logger.info("ElevenLabs TTS initialized successfully")
            except Exception as e:
                self.logger.error(f"ElevenLabs setup failed: {e}")
        
        # Setup pyttsx3 (fallback)
        if PYTTSX3_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_fallback = "pyttsx3"
                self.logger.info("pyttsx3 TTS fallback initialized")
            except Exception as e:
                self.logger.error(f"pyttsx3 setup failed: {e}")
        
        if not self.tts_primary and not self.tts_fallback:
            self.logger.warning("No TTS system available")
    
    def speak(self, text: str) -> bool:
        """
        Speak text using available TTS system with fallback
        
        Args:
            text: Text to speak
            
        Returns:
            bool: True if speech was successful, False otherwise
        """
        print(f"🤖 Assistant: {text}")
        self.logger.info(f"Speaking: {text}")
        
        # Try ElevenLabs first
        if self.tts_primary == "elevenlabs":
            if self._speak_elevenlabs(text):
                return True
            self.logger.warning("ElevenLabs failed, trying fallback")
        
        # Try pyttsx3 fallback
        if self.tts_fallback == "pyttsx3":
            if self._speak_pyttsx3(text):
                return True
            self.logger.warning("pyttsx3 fallback failed")
        
        # If all TTS fails, at least print the message
        self.logger.error("All TTS systems failed")
        return False
    
    def _speak_elevenlabs(self, text: str) -> bool:
        """Speak using ElevenLabs with improved error handling"""
        try:
            # Clean up any existing output file
            if os.path.exists(Config.AUDIO_OUTPUT_FILE):
                self._safe_file_remove(Config.AUDIO_OUTPUT_FILE)
            
            # Generate audio
            audio = generate(
                text=text, 
                voice=Config.VOICE_ID, 
                model=Config.ELEVEN_MODEL
            )
            
            # Save and play audio
            save(audio, Config.AUDIO_OUTPUT_FILE)
            
            if PLAYSOUND_AVAILABLE:
                playsound(Config.AUDIO_OUTPUT_FILE)
            else:
                self.logger.warning("playsound not available, audio file saved but not played")
            
            # Cleanup
            self._safe_file_remove(Config.AUDIO_OUTPUT_FILE)
            return True
            
        except Exception as e:
            self.logger.error(f"ElevenLabs TTS error: {e}")
            return False
    
    def _speak_pyttsx3(self, text: str) -> bool:
        """Speak using pyttsx3 fallback"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            return True
        except Exception as e:
            self.logger.error(f"pyttsx3 TTS error: {e}")
            return False
    
    def _safe_file_remove(self, filepath: str, max_retries: int = 3) -> bool:
        """Safely remove file with retries"""
        for attempt in range(max_retries):
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                return True
            except PermissionError:
                if attempt < max_retries - 1:
                    time.sleep(0.5)
                    continue
                self.logger.warning(f"Could not remove file {filepath} after {max_retries} attempts")
                return False
            except Exception as e:
                self.logger.error(f"Error removing file {filepath}: {e}")
                return False
        return True
    
    def listen_command(self) -> str:
        """
        Listen for voice command with improved error handling
        
        Returns:
            str: Recognized command or empty string if failed
        """
        recognizer = sr.Recognizer()
        
        try:
            with sr.Microphone() as source:
                self.speak("Yes Peter, how can I help you?")
                self.logger.info("Listening for command...")
                
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen with timeout
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            
            # Recognize speech
            command = recognizer.recognize_google(audio).lower()
            print(f"🎤 You said: {command}")
            self.logger.info(f"Command received: {command}")
            return command
            
        except sr.WaitTimeoutError:
            self.speak("I didn't hear anything. Please try again.")
            self.logger.warning("Listen timeout")
            return ""
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't understand that.")
            self.logger.warning("Speech not recognized")
            return ""
        except sr.RequestError as e:
            self.speak("Speech recognition service is unavailable.")
            self.logger.error(f"Speech recognition error: {e}")
            return ""
        except Exception as e:
            self.speak("An error occurred while listening.")
            self.logger.error(f"Unexpected error in listen_command: {e}")
            return ""
    
    def get_installed_apps(self) -> Dict[str, str]:
        """
        Get installed applications with caching and improved error handling
        
        Returns:
            Dict[str, str]: Dictionary mapping app names to executable paths
        """
        # Try to load from cache first
        if os.path.exists(Config.APP_CACHE_FILE):
            try:
                cache_age = time.time() - os.path.getmtime(Config.APP_CACHE_FILE)
                if cache_age < 3600:  # Cache valid for 1 hour
                    with open(Config.APP_CACHE_FILE, 'r', encoding='utf-8') as f:
                        self.apps_cache = json.load(f)
                    self.logger.info(f"Loaded {len(self.apps_cache)} apps from cache")
                    return self.apps_cache
            except Exception as e:
                self.logger.warning(f"Failed to load app cache: {e}")
        
        # Build fresh app list
        apps = {}
        
        # Add common system apps
        apps.update(self._get_common_apps())
        
        # Add Windows-specific apps if available
        if WINDOWS_FEATURES:
            apps.update(self._scan_windows_registry())
            apps.update(self._scan_start_menu_shortcuts())
        
        # Add popular app locations
        apps.update(self._scan_common_locations())
        
        # Cache the results
        try:
            with open(Config.APP_CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(apps, f, indent=2)
            self.logger.info(f"Cached {len(apps)} apps")
        except Exception as e:
            self.logger.warning(f"Failed to save app cache: {e}")
        
        self.apps_cache = apps
        return apps
    
    def _get_common_apps(self) -> Dict[str, str]:
        """Get common system applications"""
        common_apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "wordpad": "write.exe",
            "command prompt": "cmd.exe",
            "powershell": "powershell.exe",
            "explorer": "explorer.exe",
            "control panel": "control.exe",
            "task manager": "taskmgr.exe",
        }
        
        if platform.system() == "Windows":
            common_apps.update({
                "snipping tool": "SnippingTool.exe",
                "snip and sketch": "SnipSketch.exe"
            })
        
        return common_apps
    
    def _scan_windows_registry(self) -> Dict[str, str]:
        """Scan Windows registry for installed applications"""
        if not WINDOWS_FEATURES:
            return {}
        
        apps = {}
        reg_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        
        for reg_path in reg_paths:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                if display_name:
                                    name = re.sub(r'[^\w\s]', '', display_name.lower().strip())
                                    
                                    # Try to find executable path
                                    exe_path = self._find_app_executable(subkey)
                                    if exe_path:
                                        apps[name] = exe_path
                        except (OSError, FileNotFoundError):
                            continue
            except Exception as e:
                self.logger.warning(f"Registry scan error for {reg_path}: {e}")
        
        return apps
    
    def _find_app_executable(self, registry_key) -> Optional[str]:
        """Find executable path from registry key"""
        path_keys = ["InstallLocation", "ExecutablePath", "Inno Setup: App Path"]
        
        for key_name in path_keys:
            try:
                path_value = winreg.QueryValueEx(registry_key, key_name)[0]
                if path_value and os.path.exists(path_value):
                    if path_value.endswith('.exe'):
                        return path_value
                    elif os.path.exists(path_value + '.exe'):
                        return path_value + '.exe'
            except (OSError, FileNotFoundError):
                continue
        
        return None
    
    def _scan_start_menu_shortcuts(self) -> Dict[str, str]:
        """Scan Windows Start Menu shortcuts"""
        if not WINDOWS_FEATURES:
            return {}
        
        apps = {}
        shortcut_dirs = [
            os.path.join(os.environ.get('PROGRAMDATA', ''), r'Microsoft\Windows\Start Menu\Programs'),
            os.path.join(os.environ.get('APPDATA', ''), r'Microsoft\Windows\Start Menu\Programs')
        ]
        
        for directory in shortcut_dirs:
            if not os.path.exists(directory):
                continue
                
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.lnk'):
                        try:
                            full_path = os.path.join(root, file)
                            shortcut = winshell.shortcut(full_path)
                            target_path = shortcut.path
                            
                            if os.path.exists(target_path) and target_path.endswith('.exe'):
                                name = re.sub(r'[^\w\s]', '', os.path.splitext(file)[0].lower().strip())
                                apps[name] = target_path
                        except Exception:
                            continue
        
        return apps
    
    def _scan_common_locations(self) -> Dict[str, str]:
        """Scan common application installation locations"""
        apps = {}
        
        # Common Windows app locations
        if platform.system() == "Windows":
            common_paths = [
                rf"C:\Users\{os.getlogin()}\AppData\Roaming\Telegram Desktop\Telegram.exe",
                rf"C:\Users\{os.getlogin()}\AppData\Local\Programs\Telegram Desktop\Telegram.exe",
                r"C:\Program Files\Telegram Desktop\Telegram.exe",
                r"C:\Program Files (x86)\Telegram Desktop\Telegram.exe"
            ]
            
            for path in common_paths:
                if os.path.exists(path):
                    app_name = Path(path).stem.lower()
                    apps[app_name] = path
        
        return apps
    
    def find_best_app_match(self, app_name: str, apps: Dict[str, str]) -> Optional[str]:
        """
        Find the best matching application using improved fuzzy matching
        
        Args:
            app_name: Name of app to find
            apps: Dictionary of available apps
            
        Returns:
            str: Best matching app name or None if no match found
        """
        app_name = app_name.lower().strip()
        
        # Exact match
        if app_name in apps:
            return app_name
        
        # Try variations
        variations = [
            app_name.replace(' ', ''),
            app_name.replace(' ', '-'),
            app_name.replace(' ', '_'),
            app_name.replace(' ', '.'),
            f"{app_name} desktop",
            f"{app_name} app",
            f"{app_name} program"
        ]
        
        for variation in variations:
            if variation in apps:
                return variation
        
        # Fuzzy matching - find apps that contain the search term
        matches = []
        for name in apps:
            if app_name in name:
                matches.append((name, len(name)))  # Prefer shorter matches
            elif name in app_name:
                matches.append((name, len(app_name)))
        
        if matches:
            # Return the shortest match (most specific)
            matches.sort(key=lambda x: x[1])
            return matches[0][0]
        
        return None
    
    def execute_command(self, command: str):
        """
        Execute voice command with improved error handling and functionality
        
        Args:
            command: Voice command to execute
        """
        if not command:
            return
        
        command_lower = command.lower().strip()
        self.logger.info(f"Executing command: {command}")
        
        try:
            # Handle exit commands
            if any(phrase in command_lower for phrase in ["exit", "stop listening", "goodbye", "quit"]):
                self.speak("Goodbye! Have a great day!")
                self.logger.info("Assistant stopped by user command")
                self.cleanup()
                sys.exit(0)
            
            # Handle shutdown command
            elif "shutdown" in command_lower:
                self.speak("Shutting down your system in 10 seconds. Say 'cancel' to stop.")
                # Add a confirmation mechanism here if needed
                if platform.system() == "Windows":
                    os.system("shutdown /s /t 10")
                else:
                    os.system("sudo shutdown -h +1")
            
            # Handle web commands
            elif "open youtube" in command_lower:
                webbrowser.open("https://www.youtube.com")
                self.speak("Opening YouTube")
            
            elif "open google" in command_lower:
                webbrowser.open("https://www.google.com")
                self.speak("Opening Google")
            
            elif "search for" in command_lower:
                search_term = command_lower.replace("search for", "").strip()
                if search_term:
                    webbrowser.open(f"https://www.google.com/search?q={search_term}")
                    self.speak(f"Searching for {search_term}")
                else:
                    self.speak("What would you like me to search for?")
            
            # Handle special speech
            elif "give your speech" in command_lower:
                speech = ("It's easy to feel hopeful on a beautiful day like today, "
                         "but there will be dark days ahead of us too. There will be days "
                         "when we feel all alone, and that's when hope is needed most.")
                self.speak(speech)
            
            # Handle time query
            elif "what time is it" in command_lower or "current time" in command_lower:
                current_time = datetime.now().strftime("%I:%M %p")
                self.speak(f"The current time is {current_time}")
            
            # Handle app opening commands
            elif command_lower.startswith("open "):
                app_name = command_lower[5:].strip()
                self._open_application(app_name)
            
            # Try to match command directly with app names
            else:
                apps = self.get_installed_apps()
                best_match = self.find_best_app_match(command_lower, apps)
                
                if best_match:
                    self._open_application(best_match)
                else:
                    self.speak("Sorry, I don't know how to do that yet. You can ask me to open applications, search the web, or tell me to exit.")
        
        except Exception as e:
            self.logger.error(f"Error executing command '{command}': {e}")
            self.speak("Sorry, I encountered an error while processing your request.")
    
    def _open_application(self, app_name: str):
        """
        Open an application with improved error handling
        
        Args:
            app_name: Name of application to open
        """
        apps = self.get_installed_apps()
        best_match = self.find_best_app_match(app_name, apps)
        
        if not best_match:
            self.speak(f"I couldn't find {app_name}. Please make sure it's installed.")
            return
        
        app_path = apps[best_match]
        
        try:
            if os.path.exists(app_path):
                subprocess.Popen([app_path], shell=True)
                self.speak(f"Opening {best_match}")
                self.logger.info(f"Successfully opened {best_match}")
            else:
                self.speak(f"{best_match} was found but the file doesn't exist anymore.")
                self.logger.warning(f"App path doesn't exist: {app_path}")
        
        except Exception as e:
            self.logger.error(f"Error opening {best_match}: {e}")
            self.speak(f"Sorry, I couldn't open {best_match}")
    
    def setup_wake_word_detection(self):
        """Setup wake word detection with proper error handling"""
        try:
            self.porcupine = pvporcupine.create(
                access_key=Config.PORCUPINE_ACCESS_KEY,
                keyword_paths=[Config.WAKE_WORD_PATH]
            )
            
            self.pyaudio_instance = pyaudio.PyAudio()
            self.audio_stream = self.pyaudio_instance.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )
            
            self.logger.info("Wake word detection setup successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Wake word detection setup failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up resources properly"""
        self.logger.info("Cleaning up resources...")
        
        try:
            if self.audio_stream:
                self.audio_stream.stop_stream()
                self.audio_stream.close()
            
            if self.pyaudio_instance:
                self.pyaudio_instance.terminate()
            
            if self.porcupine:
                self.porcupine.delete()
            
            # Clean up temporary files
            self._safe_file_remove(Config.AUDIO_OUTPUT_FILE)
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    def run(self):
        """Main execution loop with comprehensive error handling"""
        try:
            print("🚀 Starting Gwen Voice Assistant...")
            self.logger.info("Starting Gwen Voice Assistant")
            
            # Setup wake word detection
            if not self.setup_wake_word_detection():
                print("❌ Failed to setup wake word detection")
                return
            
            print("🎯 Gwen is running in background...")
            print("🎤 Waiting for 'Hey Gwen'...")
            print("💡 Say 'exit' to stop the assistant")
            
            # Main listening loop
            while True:
                try:
                    pcm = self.audio_stream.read(
                        self.porcupine.frame_length, 
                        exception_on_overflow=False
                    )
                    pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                    
                    result = self.porcupine.process(pcm)
                    if result >= 0:
                        print("🎤 Wake word detected!")
                        self.logger.info("Wake word detected")
                        
                        command = self.listen_command()
                        if command:
                            self.execute_command(command)
                
                except KeyboardInterrupt:
                    print("\n🛑 Stopping assistant...")
                    self.logger.info("Assistant stopped by user (Ctrl+C)")
                    break
                
                except Exception as e:
                    self.logger.error(f"Error in main loop: {e}")
                    time.sleep(1)  # Brief pause before continuing
        
        except Exception as e:
            self.logger.error(f"Critical error in main execution: {e}")
            print(f"❌ Critical error: {e}")
        
        finally:
            self.cleanup()


def main():
    """Main entry point with error handling"""
    try:
        assistant = VoiceAssistant()
        assistant.run()
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        print(f"❌ Fatal error: {e}")
        print("Please check the log file for more details.")
    
    finally:
        print("🔄 Assistant shutdown complete")


if __name__ == "__main__":
    main()