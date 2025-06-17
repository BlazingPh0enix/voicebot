# 🎭 mAsK Voicebot

A soulful AI companion with customizable dark themes and audio visualization.

## ✨ Features

- **🎨 Customizable Dark Themes**: Choose from 5 beautiful color schemes
- **🔊 Audio Visualizer**: Real-time circular waveform visualization
- **💬 Dual Interface**: Text chat and voice chat modes
- **🎭 Personality**: MohammedAnas Shakil Kazi (mAsK) - An INFP companion
- **🌙 Dark Mode**: Elegant dark interface with neon accents

## 🎨 Available Themes

1. **Cyber Green** - Matrix-inspired green glow
2. **Electric Blue** - Cool blue cyberpunk vibes  
3. **Purple Haze** - Mystical purple energy
4. **Sunset Orange** - Warm orange ambient
5. **Ice Blue** - Cool cyan aesthetics

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file in the project directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
HOUNDIFY_CLIENT_ID=your_houndify_id_here (optional)
HOUNDIFY_CLIENT_KEY=your_houndify_key_here (optional)
```

### 3. Run the App
```bash
python run_voicebot.py
```

Or directly with Streamlit:
```bash
streamlit run app_frontend.py
```

## 📁 Project Structure

```
Voicebot/
├── app_frontend.py      # Main UI with themes and visualizer
├── backend.py           # AI logic and speech processing
├── run_voicebot.py      # Launcher script
├── requirements.txt     # Dependencies
├── .env                # API keys (create this)
├── temp_audio/         # Temporary audio files
└── README.md           # This file
```

## 🎤 Voice Features

- **Speech-to-Text**: Powered by Houndify (with fallback)
- **Text-to-Speech**: Google Text-to-Speech (gTTS)
- **Audio Visualizer**: Real-time waveform during listening/thinking

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

### Theme Customization
Themes can be selected from the sidebar. Each theme includes:
- Primary color (main accents)
- Secondary color (buttons, borders)
- Accent color (highlights, text)
- Background (dark gradients)
- Surface (container backgrounds)

### Audio Settings
- Toggle text-to-speech on/off
- Adjust visualizer sensitivity
- Audio files auto-cleanup after 30 minutes

## 🔧 Technical Details

### Backend (`backend.py`)
- **VoicebotBackend Class**: Handles all AI and audio processing
- **OpenAI Integration**: GPT models for conversations
- **Speech Recognition**: Houndify with fallbacks
- **Text-to-Speech**: gTTS with temporary file management
- **Error Handling**: Graceful fallbacks for all operations

### Frontend (`app_frontend.py`)
- **Streamlit UI**: Modern web interface
- **Plotly Visualizer**: Real-time audio waveform
- **CSS Theming**: Dynamic theme application
- **Session Management**: Persistent chat and settings
- **Responsive Design**: Works on desktop and mobile

## 🛠️ Development

### Adding New Themes
1. Add theme config to `THEMES` dict in `app_frontend.py`
2. Define primary, secondary, accent, background, surface colors
3. Theme automatically applies to all UI elements

### Customizing Visualizer
- Modify `create_audio_visualizer()` function
- Adjust waveform generation in `np.random.normal()`
- Change circle radius, animation, or add new effects

### Extending Backend
- Add new AI models in `generate_response()`
- Implement additional speech services
- Add voice cloning or custom TTS

## 📋 Requirements

- Python 3.8+
- Streamlit 1.28+
- OpenAI API key
- Microphone access (for voice features)
- Internet connection

## 🐛 Troubleshooting

### Audio Issues
- **No microphone detected**: Check system audio permissions
- **Poor speech recognition**: Try using text chat instead
- **No audio playback**: Check browser audio settings

### API Issues  
- **OpenAI errors**: Verify API key in `.env` file
- **Rate limiting**: Wait a moment and try again
- **Model not found**: Update to latest OpenAI models

### Installation Issues
- **PyAudio problems**: Try `conda install pyaudio` or pre-compiled wheels
- **Permission errors**: Run with administrator privileges
- **Module not found**: Ensure all requirements are installed

## 🤝 Contributing

Feel free to enhance mAsK with:
- New themes and visual effects
- Additional AI personalities  
- Voice cloning integration
- Mobile app version
- Advanced audio processing

## 📄 License

This project is open source. Feel free to use and modify for personal or educational purposes.

---

*"In a world of artificial intelligence, let's not forget to be authentically human." - mAsK* 🎭✨
