# Changelog

All notable changes to Gwen Voice Assistant will be documented in this file.

## [2.0.0] - 2025-01-11

### 🔒 Security
- **BREAKING**: Removed hardcoded API keys from source code
- Added secure environment variable configuration
- Created comprehensive .gitignore to prevent secret leaks
- Implemented centralized configuration management

### ✨ New Features
- Added fallback TTS system (pyttsx3 when ElevenLabs fails)
- Implemented intelligent fuzzy matching for app detection
- Added comprehensive error handling and recovery
- Added proper resource management and cleanup
- Added time query functionality ("What time is it?")
- Added web search capability ("Search for...")
- Added system shutdown command with confirmation
- Added detailed logging with configurable levels

### 🐛 Bug Fixes
- Fixed memory leaks in audio stream handling
- Fixed file permission errors with proper retry logic
- Fixed registry access errors on Windows
- Fixed app cache corruption issues
- Fixed audio device detection problems

### 🚀 Performance Improvements
- Implemented app caching system (1-hour refresh cycle)
- Optimized Windows registry scanning
- Reduced startup time with lazy loading
- Improved wake word detection reliability

### 📝 Documentation
- Added comprehensive README with setup instructions
- Created detailed setup guide (SETUP_INSTRUCTIONS.md)
- Added troubleshooting section
- Created example configuration files
- Added inline code documentation

### 🔧 Technical Improvements
- Refactored monolithic code into class-based architecture
- Added type hints for better code maintainability
- Implemented proper exception handling hierarchy
- Added configuration validation
- Created automated setup script (run_assistant.bat)

### 📦 Dependencies
- Updated requirements.txt with all missing packages
- Added platform-specific dependencies
- Added development dependencies section
- Improved dependency version management

## [1.0.0] - Previous Version

### Initial Features
- Basic wake word detection with Picovoice
- ElevenLabs text-to-speech integration
- Windows app launching capability
- Basic voice command recognition
- Simple logging system

### Known Issues (Fixed in 2.0.0)
- Hardcoded API keys (security vulnerability)
- Missing dependencies in requirements.txt
- Poor error handling
- Memory leaks in audio processing
- Limited cross-platform support
- No fallback TTS system