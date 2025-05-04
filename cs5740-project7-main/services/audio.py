import os
import base64
import tempfile
import datetime

from dotenv import load_dotenv
from gtts import gTTS
from openai import OpenAI

from services import llm

# Load .env file
load_dotenv()

# Initialize the OpenAI client with the modern API pattern
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url = os.getenv('OPENAI_API_BASE_URL'),
)

def transcribe_audio(audio_data):
    try:
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
            temp_audio.write(audio_data)
            temp_audio_path = temp_audio.name

        with open(temp_audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,

            )

        os.unlink(temp_audio_path)
        return transcript.text

    except Exception as e:
        print(f"Error in transcribe_audio: {e}")
        return ""

def generate_gpt_response(prompt, messages=None):
    try:
        if messages is None:
            messages = [{"role": "user", "content": prompt}]
        else:
            messages.append({"role": "user", "content": prompt})

        last_user_prompt = messages[-1]["content"]
        response, updated_messages = llm.converse_sync(
            prompt=last_user_prompt,
            messages=messages[:-1],
            model="gpt-4-turbo-preview"
        )
        return response

    except Exception as e:
        print(f"Error in generate_gpt_response: {e}")
        return "Error generating response."

def speak_text(text, lang="en"):
    try:
        tts = gTTS(text=text, lang=lang)
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio:
            tts.save(temp_audio.name)
            with open(temp_audio.name, 'rb') as audio_file:
                audio_data = audio_file.read()
                base64_audio = base64.b64encode(audio_data).decode('utf-8')
            os.unlink(temp_audio.name)
            return f"data:audio/mp3;base64,{base64_audio}"
    except Exception as e:
        print(f"Error in speak_text: {e}")
        return None
