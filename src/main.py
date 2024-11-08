import os
import asyncio 
from cli_inputs import get_cli_inputs
from config import get_coppermind_url_map
from scrape import scrape_summary
from to_audio import process_text_to_audio
from utils import get_root_directory, sanitize_title, error_log_has_new_errors

coppermind_url_mappings = get_coppermind_url_map()

async def main(cli_inputs):
    audio_method = cli_inputs.get("audio_method")

    root_directory = get_root_directory()
    text_output_directory = os.path.join(root_directory, 'text')
    os.makedirs(text_output_directory, exist_ok=True)
    output_audio_directory_root = os.path.join(root_directory, 'audio')
    os.makedirs(output_audio_directory_root, exist_ok=True)

    for title, url in coppermind_url_mappings.items():
        sanitized_title = sanitize_title(title)
        text_output_directory_for_item = f'{text_output_directory}/{sanitized_title}'

        # Make sure the text directory for the title exists
        os.makedirs(text_output_directory_for_item, exist_ok=True)

        print(f'Scraping summary for: {title}')
        scrape_summary(url, text_output_directory)
        print(f'Text finished scraping for: {title}')

        print(f'Converting text to audio for: {title}')
        text_files = sorted(os.listdir(text_output_directory_for_item), key=lambda file: int(os.path.splitext(file)[0]))

        output_audio_directory = f'{output_audio_directory_root}/{sanitized_title}/{audio_method}'
        os.makedirs(output_audio_directory, exist_ok=True)

        global_index = 1  # Keep track of a global index for the audio files
        for text_file in text_files:
            if title == "The Way of Kings" and text_file.endswith('8.txt'):
                break
            global_index = await process_text_to_audio(
                text_file, text_output_directory_for_item, output_audio_directory, global_index, audio_method
            )
    
    # If after running the error log isn't empty, let the user know
    if error_log_has_new_errors() == True:
        print("There were errors during processing. Please see error.log for more information.")

if __name__ == "__main__":
    asyncio.run(main(get_cli_inputs()))
