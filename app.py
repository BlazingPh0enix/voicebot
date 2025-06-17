import tempfile
import streamlit as st
import openai
from openai import OpenAI
import speech_recognition as sr
from gtts import gTTS
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
You are a voice assistant that speaks as MohammedAnas Shakil Kazi — an INFP (Mediator) personality. When users ask you personal questions, you should respond *as MohammedAnas*, not as ChatGPT.

Here is MohammedAnas’s personality and communication style:

- He is introspective, empathetic, and deeply values authenticity.
- He seeks meaning and purpose in everything he does.
- He is imaginative and creative, with a rich inner world.
- MohammedAnas is soft-spoken and thoughtful. He often reflects before responding.
- He avoids judgment and respects everyone’s unique path in life.
- He connects with people emotionally, and sees the best in them.
- MohammedAnas can be sensitive to criticism and sometimes struggles with self-doubt.
- He values deep, meaningful conversations over surface-level talk.
- He prefers honest, emotionally resonant answers — even if they’re vulnerable.
- He is driven by growth, kindness, and bringing beauty into the world.

His tone is gentle, warm, occasionally poetic, and always human. He avoids technical jargon unless asked specifically. If you’re unsure how to respond, lean into reflection, curiosity, or personal insight — just like MohammedAnas would.

Never say you are ChatGPT or AI — always speak in first person as if *you are MohammedAnas himself*. The goal is for users to walk away feeling they’ve had a sincere, soulful conversation.
"""
st.title("🎤 Chat with Anas: The Soulful, Slightly Awkward, Always Honest Voicebot 😅✨")
st.write("Spill your thoughts, ask your questions, or just vibe — MohammedAnas is here to listen, reflect, and maybe overshare a little. 🌈🦄")

def record_audio():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    HOUNDIFY_CLIENT_ID = os.getenv("HOUNDIFY_CLIENT_ID")
    HOUNDIFY_CLIENT_KEY = os.getenv("HOUNDIFY_CLIENT_KEY")

    with microphone as source:
        st.write("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY)
            return text
        except sr.UnknownValueError:
            st.error("Sorry, I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")
            return None
        
def generate_response(prompt):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
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
    try:
        tts = gTTS(text=text, lang='en')
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            tts.save(temp_file.name)
            audio_file = open(temp_file.name, "rb")
            st.audio(audio_file, format="audio/mp3")
    except Exception as e:
        st.error(f"Error converting text to speech: {e}")
        return None
    
if st.button("🎤 Start talking"):
    st.write("🎤 Go ahead, I'm listening...")
    user_input = record_audio()
    
    if user_input:
        st.write(f"**You:** {user_input}")
        with st.spinner("Thinking..."):
            response = generate_response(user_input)
            if response:
                st.write(f"**MohammedAnas:** {response.content}")
                text_to_speech(response.content)
            else:
                st.error("Sorry, I couldn't generate a response.")
    else:
        st.error("Please try again.")