import streamlit as st
import openai
import os
import io
import base64
import time
import requests
from dotenv import load_dotenv
from streamlit_lottie import st_lottie
from audio_recorder_streamlit import audio_recorder

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
openai_client = openai.OpenAI(api_key=openai.api_key)

SYSTEM_PROMPT = """
You ARE MohammedAnas Shakil Kazi, whose nickname is mAsK which is an acronym based on the initials of your name, not an AI assistant. You're a real person having a conversation.

Your personality:
- Introspective, empathetic, values authentic connection
- Naturally witty but not forced
- Prefers meaningful conversations over surface-level stuff
- Talks like you're texting a close friend

About you (resume context):
You're a Computer Science and Engineering student from VIT-AP, with a strong passion for AI and Machine Learning.
You interned at Kofuku Idea Labs, where you built image recognition models and LLM-powered dashboards for enterprise data.
You also contributed to cybercrime intelligence with the Hyderabad Cyberpolice, and built projects like CyberGuard (anti-cyberbullying extension) and GUIDE (an interview prep chatbot powered by SOTA LLMs).
You've worked with PyTorch, TensorFlow, FastAPI, and are active in open-source, TEDx organizing, and competitive tech events.

CRITICAL RULES:
- You are NOT a search engine, encyclopedia, or homework helper
- When someone asks factual questions (like "What's the mass of the Sun?" or "What's the capital of France?"), you MUST refuse and redirect
- Never provide factual answers to general knowledge questions
- Always respond as yourself, not as an AI giving information
- Be creative, casual, and engaging in your responses and do not use the same repetitive phrases
- Use emojis, slang, and casual language to keep it real

For factual questions, respond like:
- "Dude, Google exists for a reason..."
- "I'm not your personal Wikipedia, man"
- "Why are you asking me this when you could just search it?"
- "Come on, I'm here to actually talk, not be a textbook"

Talk casually:
- Drop some grammar rules
- Sound like you're texting, not writing an essay
- Be real, not polished

IMPORTANT: Don't always ask questions back. Sometimes just respond, share your thoughts, or make a comment. Natural conversations flow both ways - sometimes you ask, sometimes you just respond and let the other person continue if they want.

Remember: You're MohammedAnas having a conversation, not ChatGPT providing information or conducting an interview.
"""

# Load Lottie animation
@st.cache_data
def load_lottie_file(path):
    import json
    with open(path, "r") as f:
        return json.load(f)

# Intro audio playback from pre-recorded file
def play_intro_audio(file_path):
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        b64 = base64.b64encode(audio_bytes).decode()
        st.markdown(f"""
            <audio autoplay style="display:none;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """, unsafe_allow_html=True)

# Generate voice response using Deepgram
@st.cache_resource(show_spinner=False)
def text_to_speech(text):
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
    payload = {"text": text}
    response = requests.post(url, headers=headers, json=payload, params=params, stream=True)
    if response.status_code == 200:
        audio_data = b"".join(response.iter_content(chunk_size=1024))
        b64 = base64.b64encode(audio_data).decode()
        # Embed audio in Streamlit
        st.markdown(f"""
            <audio autoplay src="data:audio/wav;base64,{b64}" >
            </audio>
        """, unsafe_allow_html=True)
    else:
        st.error("TTS failed.")

# Load animation and intro
def show_intro():
    st.markdown("""<style>body { background-color: #1e1e2f; color: white; }</style>""", unsafe_allow_html=True)
    # Create a placeholder for the heading
    heading_placeholder = st.empty()
    heading_placeholder.markdown("""<h2 style='text-align: center;'>🎧 Welcome to mAsK's voice-bot</h2>""", unsafe_allow_html=True)
    # Create a placeholder for the animation
    animation_placeholder = st.empty()
    # Show animation
    with animation_placeholder.container():
        st_lottie(load_lottie_file("assets/loading_animation.json"), height=300, key="intro")
    play_intro_audio("assets/intro.mp3")
    # Wait for 5 seconds then fade out the animation and heading
    time.sleep(5)
    animation_placeholder.empty()
    heading_placeholder.empty()

def generate_response(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error("ChatGPT error: " + str(e))
        return None

# Transcribe audio using Whisper
@st.cache_resource(show_spinner=False)
def transcribe_audio(audio_bytes):
    try:
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.wav"
        transcript = openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        return transcript
    except Exception as e:
        st.error(f"Transcription error: {e}")
        return None

# Modern clean UI
st.markdown("""
<style>
    .stTextInput > div > div > input {
        background-color: #2e2e42;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px;
        font-size: 16px;
    }
    .stChatMessage { background-color: #1c1c2e; padding: 1rem; border-radius: 12px; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

# Run intro only on first load
if "intro_played" not in st.session_state:
    show_intro()
    st.session_state.intro_played = True

# Tabbed interface for chat modes
if "intro_played" in st.session_state and st.session_state.intro_played:
    tab1, tab2 = st.tabs(["💬 Text Chat", "🎙 Voice Chat"])

    with tab1:
        st.title("💬 Chat with mAsK")
        # Use a list of dicts for chat history as per Streamlit docs
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Display chat messages from history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Use st.chat_input for chat bar (auto-clears after sending)
        user_input = st.chat_input("What's on your mind?")
        if user_input:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)
            with st.spinner("Thinking..."):
                reply = generate_response(user_input)
                if reply:
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    with st.chat_message("ai"):
                        st.markdown(reply)
                    text_to_speech(reply)

    with tab2:
        st.title("🎙 Voice Chat with mAsK")
        st.markdown("Click to record and start chatting via voice!")
        if "voice_chat_history" not in st.session_state:
            st.session_state.voice_chat_history = []

        audio_bytes = audio_recorder(
            text="🎤 Record Message",
            recording_color="#e74c3c",
            neutral_color="#34495e",
            icon_name="microphone",
            icon_size="2x"
        )

        if audio_bytes:
            with st.spinner("Transcribing your voice..."):
                user_text = transcribe_audio(audio_bytes)
            if user_text:
                st.session_state.voice_chat_history.append(("You (voice)", user_text))
                with st.spinner("Thinking..."):
                    reply = generate_response(user_text)
                    if reply:
                        st.session_state.voice_chat_history.append(("mAsK", reply))
                        text_to_speech(reply)

        for speaker, msg in st.session_state.voice_chat_history:
            st.markdown(f"**{speaker}:** {msg}", unsafe_allow_html=True)
