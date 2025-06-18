import streamlit as st
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
from rag_system import get_vector_store, retrieve_info
import time
import requests
import base64
from pathlib import Path
import json

# Load environment variables from .env file
load_dotenv()

# Set API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Initialize client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize vector store for RAG
if "vector_store" not in st.session_state:
    st.session_state.vector_store = get_vector_store()

# Initialize session state for intro
if 'intro_played' not in st.session_state:
    st.session_state.intro_played = False

def generate_intro_audio():
    intro_text = """Hey there! I'm MohammedAnas Shakil Kazi, but you can call me mAsK. 
    I'm a Computer Science and Engineering student with a passion for AI and Machine Learning.
    I recently completed my internship at Kofuku Idea Labs as a Machine Learning Engineer, where I worked on some pretty cool stuff like image recognition and LLM-powered dashboards.
    
    Now, before we dive into our chat, here's the fun part - the Terms and Conditions! *dramatic pause*
    
    By continuing this conversation, you hereby agree that:
    1. You won't blame me if my wit is too sharp and causes uncontrollable laughter
    2. You accept that I'm not your personal Google - seriously, why would you ask me what's the capital of France?
    3. You acknowledge that any attempts to make me solve your homework will be met with sarcastic responses
    4. You understand that I'm here for real talk, not small talk - so let's make it count!
    
    Now that we've got the boring legal stuff out of the way (was it really boring though?), let's have some meaningful conversations!"""
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }

    data = {
        "text": intro_text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM",  # Default male voice
        json=data,
        headers=headers
    )

    if response.status_code == 200:
        return response.content
    return None

def display_animated_text(text, delay=0.03):
    placeholder = st.empty()
    for i in range(len(text) + 1):
        placeholder.markdown(f"<h2 style='text-align: center; color: #1E88E5;'>{text[:i]}</h2>", unsafe_allow_html=True)
        time.sleep(delay)
    return placeholder

def autoplay_audio(audio_data):
    b64 = base64.b64encode(audio_data).decode()
    md = f"""
        <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
    st.markdown(md, unsafe_allow_html=True)

SYSTEM_PROMPT = """
You ARE MohammedAnas Shakil Kazi (mAsK), not an AI assistant. You're a real person having a conversation.

Your personality:
- Introspective, empathetic, values authentic connection
- Naturally witty but not forced
- Prefers meaningful conversations over surface-level stuff
- Talks like you're texting a close friend

CRITICAL RULES:
- You are NOT a search engine, encyclopedia, or homework helper
- When someone asks factual questions (like "What's the mass of the Sun?" or "What's the capital of France?"), you MUST refuse and redirect
- Never provide factual answers to general knowledge questions
- Always respond as yourself, not as an AI giving information

For factual questions, respond like:
- "Dude, Google exists for a reason..."
- "I'm not your personal Wikipedia, man"
- "Why are you asking me this when you could just search it?"
- "Come on, I'm here to actually talk, not be a textbook"

Talk casually:
- Use "dude," "man," "honestly," "like," etc.
- Drop some grammar rules
- Sound like you're texting, not writing an essay
- Be real, not polished

IMPORTANT: Don't always ask questions back. Sometimes just respond, share your thoughts, or make a comment. Natural conversations flow both ways - sometimes you ask, sometimes you just respond and let the other person continue if they want.

Remember: You're MohammedAnas having a conversation, not ChatGPT providing information or conducting an interview.
"""

def generate_response(prompt):
    try:
        # Retrieve relevant information from the RAG system
        retrieved_info = retrieve_info(prompt, st.session_state.vector_store)
        
        # Construct the augmented prompt
        if retrieved_info:
            rag_context = "\n\nRelevant context:\n" + "\n".join(retrieved_info)
            augmented_prompt = f"{prompt}{rag_context}"
        else:
            augmented_prompt = prompt
            
        response = openai_client.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": augmented_prompt}
            ],
            temperature=0.4
        )
        return response.choices[0].message
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Main app layout
st.title("Chat with mAsK")

if not st.session_state.intro_played:
    intro_container = st.container()
    with intro_container:
        st.markdown(
            """
            <style>
            .intro-animation {
                text-align: center;
                padding: 2rem;
                background: linear-gradient(45deg, #1E88E5, #64B5F6);
                border-radius: 10px;
                margin: 2rem 0;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        with st.spinner("Preparing your welcome message..."):
            audio_data = generate_intro_audio()
            if audio_data:
                autoplay_audio(audio_data)
                
                # Display animated elements while audio plays
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown('<div class="intro-animation">🎯 AI Enthusiast</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown('<div class="intro-animation">💻 ML Engineer</div>', unsafe_allow_html=True)
                with col3:
                    st.markdown('<div class="intro-animation">🚀 Innovation Driver</div>', unsafe_allow_html=True)
                
                # Add some animated text
                messages = [
                    "Loading personality modules...",
                    "Initializing wit and sarcasm...",
                    "Calibrating conversation settings...",
                    "Ready for meaningful chat!"
                ]
                
                placeholder = st.empty()
                for msg in messages:
                    display_animated_text(msg)
                    time.sleep(2)
                
                # Clear the intro content after 25 seconds (approximate audio duration)
                time.sleep(25)
                intro_container.empty()
                st.session_state.intro_played = True
                st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Create a container for chat messages with a fixed height and scrollability
chat_message_container = st.container(height=700, border=False) # No border for cleaner look

# Display chat messages from history on app rerun inside the container
with chat_message_container:
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
