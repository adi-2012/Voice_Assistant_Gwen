import pvporcupine
import pyaudio
import struct
import speech_recognition as sr
import os
import webbrowser
import time
from elevenlabs import generate, save, set_api_key
from playsound import playsound
import winreg
import json
import re
from pathlib import Path
import subprocess
import winshell
import sys
import logging
from datetime import datetime

# === Logging Setup ===
log_file = os.path.join(os.path.dirname(__file__), "gwen.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

# === Settings ===
ACCESS_KEY = "ntm0THZoVQmzci08LzntLp4rfDzwR1qPi5cD/WAmrtD2bXZlSyq5Qw=="
WAKE_WORD_PATH = "hey-Gwen_en_windows_v3_0_0.ppn"

ELEVEN_API_KEY = "sk_654f711d85fae6dab6593f9cb1f0d5bed1639be12639ad6c"
VOICE_ID = "Vara1IkEw7vh5Hr5dT3C"

set_api_key(ELEVEN_API_KEY)

def speak(text):
    print("Assistant:", text)
    logging.info(f"Speaking: {text}")
    output_file = "output.mp3"
    try:
        if os.path.exists(output_file):
            try:
                os.remove(output_file)
            except PermissionError:
                time.sleep(0.5)
                os.remove(output_file)

        audio = generate(text=text, voice=VOICE_ID, model="eleven_monolingual_v1")
        save(audio, output_file)
        playsound(output_file)
        os.remove(output_file)
    except Exception as e:
        logging.error(f"ElevenLabs failed: {e}")
        print("⚠ ElevenLabs failed:", e)

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("yes peter, how can i help you?")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        logging.info(f"Command received: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't get that.")
        return ""
    except sr.RequestError:
        speak("Speech recognition service is down.")
        return ""

APP_CACHE_FILE = "app_cache.json"

def scan_start_menu_shortcuts():
    shortcut_dirs = [
        os.path.join(os.environ['PROGRAMDATA'], r'Microsoft\Windows\Start Menu\Programs'),
        os.path.join(os.environ['APPDATA'], r'Microsoft\Windows\Start Menu\Programs')
    ]
    found_apps = {}
    for directory in shortcut_dirs:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.lnk'):
                    full_path = os.path.join(root, file)
                    try:
                        shortcut = winshell.shortcut(full_path)
                        target_path = shortcut.path
                        name = os.path.splitext(file)[0].lower().strip()
                        name = re.sub(r'[^\w\s]', '', name)
                        if os.path.exists(target_path) and target_path.endswith('.exe'):
                            found_apps[name] = target_path
                    except Exception:
                        continue
    return found_apps

def get_installed_apps():
    apps = {}
    if os.path.exists(APP_CACHE_FILE):
        try:
            with open(APP_CACHE_FILE, 'r') as f:
                apps = json.load(f)
            print(f"Loaded {len(apps)} apps from cache")
        except Exception as e:
            print(f"⚠ Failed to load app cache: {e}")

    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    for reg_path in reg_paths:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
            for i in range(winreg.QueryInfoKey(key)[0]):
                subkey_name = winreg.EnumKey(key, i)
                subkey = winreg.OpenKey(key, subkey_name)
                try:
                    display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    if display_name:
                        name = re.sub(r'[^\w\s]', '', display_name.lower().strip())
                        exe_path = None
                        for k in ["InstallLocation", "ExecutablePath", "Inno Setup: App Path"]:
                            try:
                                val = winreg.QueryValueEx(subkey, k)[0]
                                if val and os.path.exists(val):
                                    exe_path = val
                                    break
                                elif val and os.path.exists(val + ".exe"):
                                    exe_path = val + ".exe"
                                    break
                            except: continue
                        if exe_path:
                            apps[name] = exe_path
                except: pass
                finally:
                    subkey.Close()
        except: pass
        finally:
            try: key.Close()
            except: pass

    apps.update(scan_start_menu_shortcuts())

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
        "snipping tool": "SnippingTool.exe",
        "snip and sketch": "SnipSketch.exe"
    }
    apps.update(common_apps)

    if "telegram" not in apps:
        paths = [
            rf"C:\Users\{os.getlogin()}\AppData\Roaming\Telegram Desktop\Telegram.exe",
            rf"C:\Users\{os.getlogin()}\AppData\Local\Programs\Telegram Desktop\Telegram.exe",
            r"C:\Program Files\Telegram Desktop\Telegram.exe",
            r"C:\Program Files (x86)\Telegram Desktop\Telegram.exe"
        ]
        for p in paths:
            if os.path.exists(p):
                apps["telegram"] = p
                break

    with open(APP_CACHE_FILE, 'w') as f:
        json.dump(apps, f)
        print(f"Cached {len(apps)} apps")

    return apps

def find_best_match(app_name, apps):
    app_name = app_name.lower()
    if app_name in apps:
        return app_name
    variations = [
        app_name.replace(' ', ''),
        app_name.replace(' ', '-'),
        app_name.replace(' ', '_'),
        app_name.replace(' ', '.'),
        app_name + ' desktop', app_name + ' app', app_name + ' program'
    ]
    for v in variations:
        if v in apps:
            return v
    for name in apps:
        if app_name in name or name in app_name:
            return name
    return None

def execute_command(command):
    
    apps = get_installed_apps()
    app_name = None
    command_lower = command.lower()

    if command_lower in apps:
        app_name = command_lower
    else:
        for name in apps:
            if name in command_lower or command_lower in name:
                app_name = name
                break

    if app_name:
        app_path = apps[app_name]
        if app_path:
            try:
                subprocess.Popen([app_path])
                speak(f"Opening {app_name}")
                return
            except Exception as e:
                print(f"Error opening {app_name}: {e}")
                speak(f"Sorry, I couldn't open {app_name}")
        else:
            speak(f"I couldn't find the path for {app_name}")
        return

    if "give your speech" in command:
        speak("It's easy to feel hopeful on a beautiful day like today, but there will be dark days ahead...")
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")      
    elif "shutdown" in command:
        speak("Shutting down your system.")
        os.system("shutdown /s /t 1")
    elif "exit" in command or "stop listening" in command:
        speak("Goodbye!")
        logging.info("Assistant stopped by user command")
        sys.exit(0)
    elif command.startswith("open "):
        app_name = command[5:].strip()
        best_match = find_best_match(app_name, apps)
        if best_match:
            app_path = apps[best_match]
            if os.path.exists(app_path):
                subprocess.Popen([app_path])
                speak(f"Opening {best_match}")
            else:
                speak(f"{best_match} not found on disk.")
        else:
            speak(f"I couldn't find {app_name}")
    else:
        speak("Sorry, I can't do that yet.")

def main():
    """Main function with error handling"""
    try:
        # Check if wake word file exists
        if not os.path.exists(WAKE_WORD_PATH):
            logging.error(f"Wake word file not found: {WAKE_WORD_PATH}")
            print(f"❌ Wake word file not found: {WAKE_WORD_PATH}")
            return

        # === Wake Word Detection Setup ===
        porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,
            keyword_paths=[WAKE_WORD_PATH]
        )
        pa = pyaudio.PyAudio()
        stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("🕵   Gwen is running in background...")
        print("🎙   Waiting for 'hey Gwen'...")
        logging.info("Gwen assistant started successfully")

        # === Main Loop ===
        try:
            while True:
                pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                result = porcupine.process(pcm)
                if result >= 0:
                    print("🎙   Wake word detected!")
                    logging.info("Wake word detected")
                    command = listen_command()
                    if command:
                        execute_command(command)

        except KeyboardInterrupt:
            print("🛑 Stopping assistant...")
            logging.info("Assistant stopped by user (Ctrl+C)")

        finally:
            stream.stop_stream()
            stream.close()
            pa.terminate()
            porcupine.delete()

    except Exception as e:
        logging.error(f"Critical error in main: {e}")
        print(f"❌ Critical error: {e}")
        time.sleep(5)  # Wait before potential restart

if __name__ == "__main__":
    main()