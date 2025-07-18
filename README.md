# 🎭 mAsK Voicebot

A sophisticated AI companion powered by Deepgram's streaming text-to-speech and OpenAI's conversational AI.

## ✨ Features

- **👋 Interactive Intro**: Engaging animated welcome sequence with Lottie animations
- **🤖 Conversational AI**: Contextual responses with authentic mAsK personality
- **🔊 Streaming TTS**: Real-time text-to-speech using Deepgram's WebSocket API
- **💬 Smart Chat**: Context-aware conversations with memory
- **🎭 Authentic Personality**: MohammedAnas Shakil Kazi (mAsK) - A real persona, not an AI assistant
- **🎙️ Voice Interaction**: Record and receive voice responses with seamless audio processing
- **� Fallback System**: Robust error handling with automatic fallback to REST API

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file in the project directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
DEEPGRAM_API_KEY=your_deepgram_api_key_here
```

### 3. Run the App
```bash
streamlit run app.py
```

The main app now features Deepgram streaming TTS. For the ElevenLabs version (if you prefer it):
```bash
streamlit run app_elevenlabs.py
```

## 📁 Project Structure

```
Voicebot/
├── app.py             # Main application with streaming Deepgram TTS
├── app_elevenlabs.py  # Alternative version with ElevenLabs TTS
├── requirements.txt   # Dependencies
├── .env              # API keys (create this)
├── assets/           # Static assets
│   └── loading_animation.json  # Lottie animation
└── README.md         # This file
```

## 🤖 System Features

### Streaming TTS System
- **WebSocket Streaming**: Real-time text-to-speech using Deepgram's WebSocket API
- **Fallback Mechanism**: Automatic fallback to REST API if streaming fails
- **High Quality Audio**: Aura-2 model for natural voice synthesis
- **Efficient Processing**: Optimized for low-latency audio delivery

### Voice Features
- **Welcome Sequence**: Engaging introduction with Lottie animations
- **Voice Input**: Record voice messages for conversation using Whisper
- **Streaming Audio**: Real-time audio generation and playback
- **Interactive UI**: Dynamic elements with modern chat interface

### Conversation Features
- **Authentic Personality**: mAsK personality with genuine human-like responses
- **Context Memory**: Maintains conversation state across interactions
- **Dual Interface**: Both text and voice chat modes
- **Error Handling**: Robust error management with user-friendly messages

## 💬 Chat Features

- **Persistent History**: Conversations saved during session
- **Streamlit Chat UI**: Native chat interface
- **Real-time Responses**: Instant AI responses
- **Theme Integration**: Chat UI matches selected theme

## 🎭 About mAsK

MohammedAnas Shakil Kazi is an INFP personality who embodies:
- Deep introspection and empathy
- Authentic, vulnerable conversations  
- Creative and poetic expression
- Gentle humor with slight awkwardness
- Meaningful connections over small talk

## ⚙️ Configuration

### Environment Variables
Make sure your `.env` file contains:
```env
OPENAI_API_KEY=your_openai_api_key_here
DEEPGRAM_API_KEY=your_deepgram_api_key_here
```

### Audio Settings
- **Streaming TTS**: Enabled by default with WebSocket API
- **Fallback System**: Automatic REST API fallback on streaming failure
- **Audio Format**: Linear16 encoding, 24kHz sample rate
- **Voice Model**: Aura-2-Arcas-EN for natural voice synthesis
- **Auto-play**: Enabled for immediate audio response

### Chat Interface
- **Dual Modes**: Text chat and voice chat tabs
- **Session Persistence**: Chat history maintained during session
- **Real-time Updates**: Instant message display and audio generation
- **Error Handling**: User-friendly error messages and recovery

## 🔧 Technical Details

### Main Application (`app.py`)
- **Streaming TTS**: Deepgram WebSocket API for real-time audio generation
- **OpenAI Integration**: GPT-4 models for conversations with mAsK personality
- **Speech Recognition**: Whisper API for voice-to-text conversion
- **Fallback System**: Automatic REST API fallback if streaming fails
- **Session Management**: Persistent chat history and state management
- **Error Handling**: Comprehensive error handling with user feedback

### Alternative Version (`app_elevenlabs.py`)
- **ElevenLabs TTS**: High-quality voice synthesis with ElevenLabs API
- **Voice Cloning**: Custom voice models for personalized responses
- **Audio Processing**: Optimized audio generation and playback
- **Streamlit Interface**: Modern web-based chat interface

## 🛠️ Development

### Enhancing TTS System
- Implement additional Deepgram voice models
- Add voice speed and pitch controls
- Optimize WebSocket connection handling
- Implement audio caching for better performance

### Voice Integration
- Add real-time voice activity detection
- Implement voice interruption handling
- Enhance audio quality processing
- Add support for multiple languages

### Extending Features
- Add conversation export/import
- Implement user preferences storage
- Add more personality variations
- Enhance error recovery mechanisms

## 📋 Requirements

- Python 3.8+
- Streamlit 1.28+
- OpenAI API key
- Deepgram API key
- Internet connection
- Microphone access (for voice features)
- Modern web browser with audio support

## 🐛 Troubleshooting

### Common Issues

#### Streaming TTS Issues
- **WebSocket connection failed**: Check Deepgram API key and internet connection
- **No audio output**: Verify browser audio permissions and settings
- **Fallback to REST API**: Normal behavior when streaming fails, check console for details
- **Audio quality issues**: Ensure stable internet connection for streaming

#### Voice Features
- **No intro audio**: Verify assets/intro.mp3 file exists and is accessible
- **Recording issues**: Check microphone permissions in browser
- **Playback problems**: Verify browser audio settings and autoplay permissions
- **Animation not loading**: Check assets/loading_animation.json file

### API Issues  
- **OpenAI errors**: Verify API key in `.env` file and check usage limits
- **Deepgram errors**: Verify API key and check account balance
- **Rate limiting**: Wait a moment and try again, or upgrade API plan
- **Model not found**: Update to latest model versions in code

### Installation Issues
- **deepgram-sdk problems**: Try `pip install --upgrade deepgram-sdk`
- **Audio dependencies**: Install platform-specific audio libraries
- **Permission errors**: Run with administrator privileges
- **Module not found**: Ensure all requirements are installed with `pip install -r requirements.txt`

## 🤝 Contributing

Feel free to enhance mAsK with:
- Additional Deepgram voice models
- Real-time conversation features
- Advanced streaming optimizations
- Mobile app version
- Voice activity detection
- Multiple language support

## 📄 License

This project is open source. Feel free to use and modify for personal or educational purposes.

---

*"In a world of artificial intelligence, let's not forget to be authentically human." - mAsK* 🎭✨
