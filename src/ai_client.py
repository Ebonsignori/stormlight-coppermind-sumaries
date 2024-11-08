import os
from dotenv import load_dotenv
from openai import OpenAI
from TTS.api import TTS
from config import get_openai_to_vits_voice_map

client = None
def get_openai_client():
    # Load environment variables from .env file
    load_dotenv('.env.local')
    global client
    if client is None:
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
    return client

def convert_text_to_speech(text, output_path, voice="alloy", method="local"):
    """
    Convert text to speech and write the output to a file. Either use OpenAI API or local method.

    Args:
        text (str): The input text to convert to speech.
        output_path (str): The path to save the resulting audio file.
        voice (str): The voice model to use for conversion.
        method (str): The method to use for conversion, "api" or "local".

    Returns:
        None: Writes the output to the specified file.
    """
    if method == "api":
        client = get_openai_client()
        try:
            response = client.audio.speech.create(
                model="tts-1-hd",
                input=text,
                voice=voice,
                response_format="mp3",
            )
            # Save the response directly to the file
            with open(output_path, 'wb') as audio_file:
                audio_file.write(response.content)

        except Exception as e:
            raise Exception(f"Failed to convert text to speech via API: {e}")
    
    elif method == "local":
        # Get the VITS voice mapping from config
        vits_voice_map = get_openai_to_vits_voice_map()
        vits_voice = vits_voice_map.get(voice, vits_voice_map.get("alloy"))  # Default to 'alloy' if not found

        try:
            # Load the TTS model and use the correct speaker for the voice
            tts = TTS(vits_voice["model"])
            tts.tts_to_file(
                text=text,
                speaker=vits_voice["speaker"],
                file_path=output_path
            )
        except Exception as e:
            raise Exception(f"Failed to convert text to speech locally: {e}")