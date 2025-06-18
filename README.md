# 🎭 mAsK Voicebot

A sophisticated AI companion powered by RAG (Retrieval-Augmented Generation) and ElevenLabs voice synthesis.

## ✨ Features

- **👋 Interactive Intro**: Engaging voice introduction with animated welcome sequence
- **🤖 RAG System**: Contextual responses based on personal knowledge base
- **�️ ElevenLabs Voice**: High-quality text-to-speech for natural conversations
- **💬 Smart Chat**: Context-aware conversations with memory
- **🎭 Authentic Personality**: MohammedAnas Shakil Kazi (mAsK) - A real persona
- **🔊 Voice Interaction**: Record and receive voice responses
- **� Knowledge Base**: Integrated with personal resume and experiences

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file in the project directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

### 3. Run the App
```bash
streamlit run app.py
```

For voice interaction features:
```bash
streamlit run app_elevenlabs.py
```

## 📁 Project Structure

```
Voicebot/
├── app.py             # Main chat application with RAG
├── app_elevenlabs.py  # Voice-enabled version with ElevenLabs
├── rag_system.py      # RAG system implementation
├── my_resume.txt      # Knowledge base content
├── requirements.txt   # Dependencies
├── .env              # API keys (create this)
├── faiss_index/      # Vector store for RAG system
│   ├── index.faiss   # FAISS vector database
│   └── index.pkl     # Pickle file for embeddings
└── README.md         # This file
```

## 🤖 System Features

### RAG System
- **Vector Store**: FAISS-based efficient similarity search
- **Knowledge Base**: Personal resume and experience integration
- **Context Awareness**: Retrieves relevant information for responses
- **Memory**: Maintains conversation context

### Voice Features
- **Welcome Sequence**: Engaging introduction with animations
- **Voice Input**: Record voice messages for conversation
- **ElevenLabs TTS**: High-quality voice synthesis
- **Interactive UI**: Dynamic elements during voice playback

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
- **Text-to-Speech**: ElevenLabs API integration for natural voice output
- **Welcome Sequence**: Interactive introduction with animations
- **Error Handling**: Graceful fallbacks for all operations

### Frontend (`app_frontend.py`)
- **Streamlit UI**: Modern web interface
- **Plotly Visualizer**: Real-time audio waveform
- **CSS Theming**: Dynamic theme application
- **Session Management**: Persistent chat and settings
- **Responsive Design**: Works on desktop and mobile

## 🛠️ Development

### Enhancing RAG System
- Add new documents to knowledge base
- Customize embedding models
- Implement additional retrieval strategies
- Optimize vector store performance

### Voice Integration
- Configure ElevenLabs voice settings
- Implement additional voice models
- Enhance voice recording quality
- Add real-time transcription

### Extending Features
- Add new conversation capabilities
- Implement additional API integrations
- Enhance memory management
- Improve context handling

## 📋 Requirements

- Python 3.8+
- Streamlit 1.28+
- OpenAI API key
- ElevenLabs API key
- FAISS for vector storage
- Internet connection
- Microphone access (for voice features)

## 🐛 Troubleshooting

### Common Issues

#### RAG System
- **Vector store not initialized**: Run the app once to create FAISS index
- **Knowledge retrieval issues**: Check if knowledge base is properly loaded
- **Slow responses**: Optimize chunk size and embedding configuration

#### Voice Features
- **No intro voice**: Verify ELEVENLABS_API_KEY in .env file
- **Recording issues**: Check microphone permissions
- **Playback problems**: Verify browser audio settings
- **Animation glitches**: Try refreshing the page

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
