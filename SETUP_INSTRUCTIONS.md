# 🚀 Gwen Voice Assistant - Setup Instructions

## Step-by-Step Setup Guide

### 1. Prerequisites Check ✅

Before starting, ensure you have:
- [ ] Python 3.7+ installed
- [ ] Windows 10/11 (for full functionality)
- [ ] Working microphone
- [ ] Internet connection
- [ ] Git installed (optional)

### 2. Download and Setup 📥

#### Option A: Clone from GitHub
```bash
git clone <your-repo-url>
cd gwen-voice-assistant
```

#### Option B: Download ZIP
1. Download the project ZIP file
2. Extract to your desired location
3. Open command prompt in the project folder

### 3. Install Python Dependencies 📦

```bash
# Install all required packages
pip install -r requirements.txt
```

**If you encounter issues:**

#### PyAudio Installation Problems (Windows)
```bash
# Method 1: Use pipwin
pip install pipwin
pipwin install pyaudio

# Method 2: Install Visual Studio Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

#### Other Package Issues
```bash
# Update pip first
python -m pip install --upgrade pip

# Install packages one by one if batch install fails
pip install pvporcupine
pip install pyaudio
pip install SpeechRecognition
pip install elevenlabs
pip install playsound
pip install pyttsx3
pip install python-dotenv
pip install requests
```

### 4. Get Your API Keys 🔑

#### A. Picovoice (Required)
1. Go to [Picovoice Console](https://console.picovoice.ai/)
2. Sign up for a free account
3. Create a new Access Key
4. Download or create a wake word file:
   - Go to "Wake Word" section
   - Create a wake word "Hey Gwen" or use existing
   - Download the `.ppn` file
   - Save it in your project folder

#### B. ElevenLabs (Optional but Recommended)
1. Go to [ElevenLabs](https://elevenlabs.io/)
2. Sign up for an account (free tier available)
3. Go to Profile → API Keys
4. Generate a new API key
5. Go to VoiceLab to find your Voice ID
   - Click on any voice
   - Copy the Voice ID from the URL or settings

### 5. Configure Environment Variables 🔧

1. **Copy the example file:**
   ```bash
   copy .env.example .env
   ```

2. **Edit the .env file** with your actual values:
   ```env
   # Required - Replace with your actual keys
   PORCUPINE_ACCESS_KEY=px_your_actual_key_here
   ELEVEN_API_KEY=sk_your_actual_key_here
   
   # Required - Update with your file name
   WAKE_WORD_PATH=hey-Gwen_en_windows_v3_0_0.ppn
   
   # Optional - Replace with your preferred voice
   VOICE_ID=your_voice_id_here
   
   # Optional - Keep defaults or customize
   LOG_LEVEL=INFO
   LOG_FILE=gwen.log
   APP_CACHE_FILE=app_cache.json
   ELEVEN_MODEL=eleven_monolingual_v1
   ```

### 6. Test Your Setup 🧪

1. **Test basic functionality:**
   ```bash
   python -c "import pvporcupine, pyaudio, speech_recognition; print('Core packages OK')"
   ```

2. **Test configuration:**
   ```bash
   python -c "from config import Config; Config.validate_config(); print('Configuration OK')"
   ```

3. **Test audio devices:**
   ```bash
   python -c "import pyaudio; p=pyaudio.PyAudio(); print(f'Audio devices: {p.get_device_count()}'); p.terminate()"
   ```

### 7. First Run 🎯

1. **Start the assistant:**
   ```bash
   python main.pyw
   ```

2. **You should see:**
   ```
   🚀 Starting Gwen Voice Assistant...
   🎯 Gwen is running in background...
   🎤 Waiting for 'Hey Gwen'...
   💡 Say 'exit' to stop the assistant
   ```

3. **Test wake word:**
   - Say "Hey Gwen" clearly
   - Wait for response: "Yes Peter, how can I help you?"
   - Try a command: "Open calculator"

### 8. Troubleshooting Common Issues 🔧

#### Issue: "Configuration Error: Missing required environment variables"
**Solution:**
- Check that `.env` file exists in project root
- Verify all required variables are set
- Ensure no extra spaces around the `=` sign

#### Issue: "Wake word file not found"
**Solution:**
- Verify the `.ppn` file is in the project folder
- Check the filename matches `WAKE_WORD_PATH` in `.env`
- Ensure the file isn't corrupted (re-download if needed)

#### Issue: "No audio input device found"
**Solution:**
- Check microphone is connected and working
- Test microphone in Windows Sound settings
- Run as Administrator if permission issues

#### Issue: "ElevenLabs failed"
**Solution:**
- Verify API key is correct (starts with `sk_`)
- Check internet connection
- Verify you have ElevenLabs credits
- Assistant will fall back to pyttsx3 automatically

#### Issue: Apps not opening
**Solution:**
- Try exact app names: "notepad", "calculator", "chrome"
- Wait for app cache to build (first run takes longer)
- Check if apps are actually installed

### 9. Advanced Configuration ⚙️

#### Custom Wake Word
1. Go to Picovoice Console
2. Create custom wake word
3. Download new `.ppn` file
4. Update `WAKE_WORD_PATH` in `.env`

#### Voice Customization
1. Go to ElevenLabs VoiceLab
2. Clone or create custom voice
3. Copy the Voice ID
4. Update `VOICE_ID` in `.env`

#### Logging Configuration
```env
# Debug level for troubleshooting
LOG_LEVEL=DEBUG

# Custom log file location
LOG_FILE=logs/gwen_debug.log
```

### 10. Security Checklist 🛡️

- [ ] `.env` file is not committed to Git
- [ ] API keys are not shared publicly
- [ ] `.gitignore` includes `.env` and `*.log`
- [ ] Regular API key rotation (recommended)

### 11. Performance Optimization 🚀

#### For Better Performance:
- Close unnecessary applications
- Use SSD storage for faster app scanning
- Ensure stable internet for ElevenLabs
- Use quality microphone for better recognition

#### For Lower Resource Usage:
- Set `LOG_LEVEL=WARNING` in `.env`
- Use pyttsx3 only (comment out ElevenLabs)
- Reduce app cache refresh frequency

### 12. Getting Help 🆘

If you're still having issues:

1. **Check the logs:**
   ```bash
   type gwen.log
   ```

2. **Test individual components:**
   ```bash
   # Test speech recognition
   python -c "import speech_recognition as sr; r=sr.Recognizer(); print('Speech recognition OK')"
   
   # Test TTS
   python -c "import pyttsx3; e=pyttsx3.init(); e.say('test'); e.runAndWait(); print('TTS OK')"
   ```

3. **Common solutions:**
   - Restart as Administrator
   - Disable antivirus temporarily
   - Update Windows audio drivers
   - Reinstall Python packages

### 13. Success Indicators ✅

You'll know everything is working when:
- [ ] Assistant starts without errors
- [ ] Wake word detection responds
- [ ] Voice commands are recognized
- [ ] Apps open successfully
- [ ] TTS speaks responses clearly
- [ ] No error messages in console

---

**🎉 Congratulations! Your Gwen Voice Assistant is ready to use!**

Say "Hey Gwen" followed by:
- "Open [app name]"
- "What time is it?"
- "Search for [something]"
- "Exit" to stop

Enjoy your new voice assistant! 🤖