# 🤖 Gwen Voice Assistant

A secure, feature-rich voice assistant with wake word detection and intelligent app launching capabilities.

## ✨ Features

- 🎤 **Wake Word Detection**: Responds to "Hey Gwen"
- 🔊 **Advanced Text-to-Speech**: ElevenLabs integration with pyttsx3 fallback
- 🚀 **Smart App Launching**: Intelligent fuzzy matching for installed applications
- 🔒 **Secure Configuration**: Environment-based API key management
- 📝 **Comprehensive Logging**: Detailed logging with configurable levels
- 🛡️ **Error Handling**: Robust error handling and recovery
- 🔄 **Resource Management**: Proper cleanup and resource management
- 🌐 **Web Integration**: Open websites and perform web searches

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Windows 10/11 (for full functionality)
- Microphone access
- Internet connection

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd gwen-voice-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment variables**
   ```bash
   # Copy the example environment file
   copy .env.example .env
   
   # Edit .env file with your API keys (see Configuration section)
   ```

4. **Download wake word file**
   - Get your wake word file (.ppn) from [Picovoice Console](https://console.picovoice.ai/)
   - Place it in the project directory
   - Update the `WAKE_WORD_PATH` in your `.env` file

5. **Run the assistant**
   ```bash
   python main.pyw
   ```

## ⚙️ Configuration

### Required API Keys

1. **Picovoice Access Key**
   - Sign up at [Picovoice Console](https://console.picovoice.ai/)
   - Create a new access key
   - Download or create a wake word file (.ppn)

2. **ElevenLabs API Key** (Optional but recommended)
   - Sign up at [ElevenLabs](https://elevenlabs.io/)
   - Get your API key from the profile section
   - Choose a voice ID from your available voices

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Required
PORCUPINE_ACCESS_KEY=your_porcupine_access_key_here
WAKE_WORD_PATH=hey-Gwen_en_windows_v3_0_0.ppn

# Optional (for premium TTS)
ELEVEN_API_KEY=your_elevenlabs_api_key_here
VOICE_ID=your_voice_id_here

# Optional (with defaults)
LOG_LEVEL=INFO
LOG_FILE=gwen.log
APP_CACHE_FILE=app_cache.json
ELEVEN_MODEL=eleven_monolingual_v1
```

## 🎯 Usage

### Voice Commands

Once running, say **"Hey Gwen"** followed by your command:

#### Application Control
- "Open [app name]" - Opens any installed application
- "Open notepad" - Opens Windows Notepad
- "Open calculator" - Opens Calculator
- "Open chrome" - Opens Google Chrome

#### Web Commands
- "Open YouTube" - Opens YouTube in default browser
- "Open Google" - Opens Google in default browser
- "Search for [query]" - Performs Google search

#### System Commands
- "What time is it?" - Tells current time
- "Shutdown" - Initiates system shutdown (with confirmation)
- "Exit" / "Stop listening" / "Goodbye" - Stops the assistant

#### Special Commands
- "Give your speech" - Plays a motivational speech

### Text-to-Speech Options

The assistant uses a fallback system for speech:

1. **Primary**: ElevenLabs (high-quality, requires API key)
2. **Fallback**: pyttsx3 (built-in, works offline)

## 🔧 Troubleshooting

### Common Issues

#### "Configuration Error: Missing required environment variables"
- Ensure your `.env` file exists and contains all required variables
- Check that your API keys are valid and properly formatted

#### "Wake word file not found"
- Verify the wake word file (.ppn) exists in the specified path
- Check the `WAKE_WORD_PATH` in your `.env` file

#### "No audio input device found"
- Ensure your microphone is connected and working
- Check Windows audio settings and permissions

#### "ElevenLabs failed" or TTS issues
- Verify your ElevenLabs API key is valid
- Check your internet connection
- The assistant will fall back to pyttsx3 automatically

#### App not opening
- The app cache refreshes every hour automatically
- Try using the exact app name as it appears in Windows
- Check if the application is actually installed

### Installation Issues

#### PyAudio installation fails
```bash
# Windows: Install Microsoft C++ Build Tools
# Or install pre-compiled wheel:
pip install pipwin
pipwin install pyaudio
```

#### Permission errors
- Run command prompt as Administrator
- Ensure antivirus isn't blocking the application

## 🛡️ Security Features

- ✅ **No hardcoded API keys** - All secrets in environment variables
- ✅ **GitHub-safe** - `.gitignore` prevents accidental key commits
- ✅ **Secure configuration** - Centralized config management
- ✅ **Input validation** - Sanitized voice command processing
- ✅ **Error isolation** - Failures don't expose sensitive data

## 📁 Project Structure

```
gwen-voice-assistant/
├── main.pyw              # Main application file
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
├── README.md            # This file
├── gwen.log             # Log file (created at runtime)
├── app_cache.json       # App cache (created at runtime)
└── hey-Gwen_*.ppn       # Wake word file (you provide)
```

## 🔄 Updates and Maintenance

### Updating App Cache
The app cache automatically refreshes every hour. To force refresh:
- Delete `app_cache.json`
- Restart the assistant

### Updating Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Log Management
Logs are stored in `gwen.log`. You can:
- Change log level in `.env` file (`DEBUG`, `INFO`, `WARNING`, `ERROR`)
- Archive old logs by renaming the file
- Clear logs by deleting the file

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the log file (`gwen.log`) for error details
3. Ensure all dependencies are properly installed
4. Verify your API keys are valid and properly configured

## 🔮 Future Enhancements

- [ ] Cross-platform support (macOS, Linux)
- [ ] Plugin system for custom commands
- [ ] GUI configuration interface
- [ ] Smart home integration
- [ ] Calendar and reminder features
- [ ] Multi-language support

---

**Made with ❤️ for voice interaction enthusiasts**