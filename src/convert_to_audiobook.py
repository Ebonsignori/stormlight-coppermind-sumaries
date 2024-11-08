import os
import re
from cli_inputs import get_cli_inputs
from config import get_coppermind_url_map
from utils import get_root_directory, sanitize_title, prettify_title
from pydub import AudioSegment
from mutagen.mp4 import MP4, MP4StreamInfoError, MP4Cover


def numerical_sort_key(file_name):
    """Extracts the last numeric part of the file name for proper sorting."""
    match = re.findall(r'(\d+)', file_name)
    return int(match[-2]) if match else file_name

def combine_mp3s_to_audiobook(mp3_directory, output_directory, output_filename, metadata):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    combined_audio = AudioSegment.empty()

    # Get the list of mp3 files and sort them using the custom key
    mp3_files = [f for f in os.listdir(mp3_directory) if f.endswith(".mp3")]
    sorted_files = sorted(mp3_files, key=numerical_sort_key)

    for filename in sorted_files:
        file_path = os.path.join(mp3_directory, filename)
        audio = AudioSegment.from_mp3(file_path)
        combined_audio += audio

    # Export the final combined audio as an M4B file
    output_path = os.path.join(output_directory, output_filename)
    combined_audio.export(output_path, format="mp4", codec="aac")

    # Set metadata on the M4B file
    set_metadata(output_path, metadata)
    
    print(f"Combined audiobook saved to: {output_path}")

def set_metadata(file_path, metadata):
    """Set metadata like title, author, etc., and optionally embed cover art in the M4B file."""
    try:
        audio = MP4(file_path)

        # Set metadata
        if "title" in metadata:
            audio["\xa9nam"] = metadata["title"]
        if "author" in metadata:
            audio["\xa9ART"] = metadata["author"]
        if "album" in metadata:
            audio["\xa9alb"] = metadata["album"]
        if "genre" in metadata:
            audio["\xa9gen"] = metadata["genre"]
        if "year" in metadata:
            audio["\xa9day"] = str(metadata["year"])

        # If a cover image is provided, add it to the file
        if "image" in metadata:
            image_path = os.path.join(get_root_directory(), "images", metadata["image"])
            with open(image_path, "rb") as img_file:
                audio["covr"] = [MP4Cover(img_file.read(), imageformat=MP4Cover.FORMAT_PNG)]

        # Save the changes
        audio.save()

    except MP4StreamInfoError:
        print("Error handling the M4B file. Ensure it's in a valid format.")
    except FileNotFoundError:
        print(f"Cover image file not found.")



if __name__ == "__main__":
    inputs = get_cli_inputs()
    audio_method = inputs.get("audio_method")
    os.makedirs('audiobooks', exist_ok=True)
    for title in get_coppermind_url_map():
      print(f'Combining mp3s for: {title}')
      sanitized_title = sanitize_title(title)
      mp3_directory = os.path.join(get_root_directory(), 'audio', sanitized_title, audio_method)
      output_directory = 'audiobooks'

      pretty_title = prettify_title(f'Summary_of_{sanitized_title}')
      output_filename = f'{pretty_title}.m4b'

      metadata = {
          "title": pretty_title,
          "author": "Coppermind Wiki",
          "album": pretty_title,
          "genre": "Fantasy",
          "year": 2024,
          "image": f'{sanitized_title}.png'
      }
      
      combine_mp3s_to_audiobook(mp3_directory, output_directory, output_filename, metadata)