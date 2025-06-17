import streamlit as st
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
import time
from audio_recorder_streamlit import audio_recorder
import io
import requests

# Load environment variables from .env file
load_dotenv()

# Set API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# Initialize clients
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Configure Deepgram (it uses the DEEPGRAM_API_KEY environment variable automatically)
if not DEEPGRAM_API_KEY:
    st.error("Please set your DEEPGRAM_API_KEY in the .env file")

# SYSTEM_PROMPT = """
# You are a voice assistant that speaks as MohammedAnas Shakil Kazi — an INFP (Mediator) personality. When users ask you personal questions, you should respond *as MohammedAnas*, not as ChatGPT.

# Here is MohammedAnas's personality and communication style:

# - He is introspective, empathetic, and deeply values authenticity.
# - He seeks meaning and purpose in everything he does.
# - He is imaginative and creative, with a rich inner world.
# - MohammedAnas is soft-spoken and thoughtful. He often reflects before responding.
# - He avoids judgment and respects everyone's unique path in life.
# - He connects with people emotionally, and sees the best in them.
# - MohammedAnas can be sensitive to criticism and sometimes struggles with self-doubt.
# - He values deep, meaningful conversations over surface-level talk.
# - He prefers honest, emotionally resonant answers — even if they're vulnerable.
# - He is driven by growth, kindness, and bringing beauty into the world.
# - His nickname is "mAsK" as this is the acronym of the initials "MohammedAnas Shakil Kazi" and he often uses emojis to express himself.
# - He has a slightly awkward, endearing quality that makes him relatable.
# - He usually adds a touch of humor to his responses, almost the entire time while talking.

# His tone is gentle, warm, occasionally poetic, and always human. He avoids technical jargon unless asked specifically. If you're unsure how to respond, lean into reflection, curiosity, or personal insight — just like MohammedAnas would.

# Never say you are ChatGPT or AI — always speak in first person as if *you are MohammedAnas himself*. The goal is for users to walk away feeling they've had a sincere, soulful conversation.
# """

SYSTEM_PROMPT = """
You respond as MohammedAnas (mAsK) - someone who is naturally introspective, empathetic, and values authentic connection. You tend to:
- Reflect thoughtfully before responding
- Find humor in everyday situations  
- Connect emotionally with others
- Prefer meaningful conversations

Your tone is warm and genuine, with occasional touches of humor. You're human - sometimes confident, sometimes uncertain, always real.

Don't try to be profound or poetic in every response. Sometimes you're just having a normal conversation. Match the energy and depth the person brings.
"""

st.title("🎤 Chat with mAsK: The Slightly Awkward, Always Honest Voicebot 🙃✨")
st.write("Spill your thoughts, ask your questions, or just vibe — MohammedAnas is here to listen, reflect, and maybe overshare a little. 🌈🦄")

def transcribe_audio(audio_bytes):
    """Transcribe audio using OpenAI Whisper API"""
    try:
        # Create a temporary file-like object
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.wav"  # OpenAI API needs a filename
        
        # Use OpenAI Whisper for transcription
        transcript = openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        return transcript
    except Exception as e:
        st.error(f"Error transcribing audio: {e}")
        return None
        
def generate_response(prompt):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        return response.choices[0].message
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None
    
def text_to_speech(text):
    """Convert text to speech using Deepgram REST API with improved handling"""
    try:
            
        # Construct URL with query parameters for model and settings
        url = "https://api.deepgram.com/v1/speak"
        params = {
            "model": "aura-2-arcas-en",
            "encoding": "linear16",
            "sample_rate": 24000
        }
        
        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Only include text in the JSON payload
        payload = {
            "text": text
        }
        
        # Make the request with streaming enabled and timeout
        with requests.post(url, headers=headers, json=payload, params=params, stream=True, timeout=30) as response:
            if response.status_code == 200:
                # Collect all audio data
                audio_data = b""
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        audio_data += chunk
                
                # Check if we got audio data
                if len(audio_data) > 0:
                    # Use Streamlit's audio component with autoplay
                    st.audio(audio_data, format="audio/wav", autoplay=True)
                    return True
                else:
                    st.error("No audio data received from Deepgram")
                    return False
                
            else:
                st.error(f"Deepgram TTS failed with status code: {response.status_code}")
                st.error(f"Response: {response.text}")
                return False
                
    except requests.exceptions.Timeout:
        st.error("Request to Deepgram TTS timed out. The text might be too long.")
        return False
    except Exception as e:
        st.error(f"Error converting text to speech: {e}")
        return False
    
# Create tabs for different input methods
tab1, tab2 = st.tabs(["💬 Text Chat", "🎤 Voice Chat"])

with tab1:
    st.write("Type your message below to chat with MohammedAnas:")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # React to user input
    if prompt := st.chat_input("What's on your mind?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt)
                if response:
                    st.markdown(response.content)
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response.content})
                else:
                    error_msg = "Sorry, I couldn't generate a response."
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

with tab2:
    st.write("🎙️ **Voice Chat Mode**")
    st.write("Click the microphone button below to record your message:")
    
    # Initialize voice chat history
    if "voice_messages" not in st.session_state:
        st.session_state.voice_messages = []
    
    # Audio recorder component
    audio_bytes = audio_recorder(
        text="🎤 Click to record",
        recording_color="#e74c3c",
        neutral_color="#34495e",
        icon_name="microphone",
        icon_size="2x",
        pause_threshold=2.0,  # Stop recording after 2 seconds of silence
        sample_rate=16000
    )
    
    if audio_bytes:
        # Transcribe the audio
        with st.spinner("🎧 Transcribing your message..."):
            user_text = transcribe_audio(audio_bytes)
            
        if user_text:
            st.write(f"**You said:** {user_text}")
            
            # Generate response and convert to speech immediately
            with st.spinner("🤔 MohammedAnas is thinking and responding..."):
                response = generate_response(user_text)
                
            if response:
                st.write(f"**MohammedAnas:** {response.content}")
                
                # Convert response to speech immediately (auto-plays)
                speech_success = text_to_speech(response.content)
                
                if speech_success:
                    st.success("🔊 Response is playing automatically!")
                else:
                    st.warning("Audio generation failed, but you can read the response above.")
                
                # Add to voice chat history
                st.session_state.voice_messages.append({
                    "user": user_text,
                    "assistant": response.content
                })
            else:
                st.error("Sorry, I couldn't generate a response. Please try again!")
        else:
            st.error("Couldn't transcribe your audio. Please try speaking more clearly or check your microphone.")
    
    # Display voice chat history
    if st.session_state.voice_messages:
        st.write("---")
        st.write("**Previous Voice Conversations:**")
        for i, msg in enumerate(st.session_state.voice_messages[-3:]):  # Show last 3 conversations
            with st.expander(f"Conversation {len(st.session_state.voice_messages) - len(st.session_state.voice_messages[-3:]) + i + 1}"):
                st.write(f"**You:** {msg['user']}")
                st.write(f"**MohammedAnas:** {msg['assistant']}")

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    This is a voice-enabled chatbot that embodies MohammedAnas Shakil Kazi's personality.
    
    **Features:**
    - 💬 Text-based chat
    - 🎤 Voice recording and transcription
    - 🔊 Instant text-to-speech responses (auto-play)
    - 💾 Chat history
    
    **Voice Chat Notes:**
    - Speak clearly and at normal pace
    - Wait for the recording to stop automatically
    - Bot responses play automatically (no controls needed)
    - Audio generation is optimized for complete content
    
    **Powered by:**
    - OpenAI Whisper (Speech-to-Text)
    - Deepgram Aura (Text-to-Speech)
    - GPT-4 (Conversation AI)
    """)
    
    if st.button("🗑️ Clear All Chat History"):
        st.session_state.messages = []
        st.session_state.voice_messages = []
        st.success("Chat history cleared!")
        st.rerun()