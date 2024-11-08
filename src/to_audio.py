import os
from ai_client import convert_text_to_speech
from config import get_character_to_openai_voice_map
from utils import has_next, write_to_error_log

character_voice_mapping = get_character_to_openai_voice_map()

def split_by_character(text):
    """Split the content by character name and return a list of dicts mapping character to their content."""
    lines = text.split('\n')
    character_content = []  # array to preserve order of lines

    # Handle the title at the top of the text
    title = lines[0].strip() if lines else None
    if title:
        # Assign the title to the "default" narrator
        character_content.append({"voice": "default", "content": title + ' <break time="2s" />'})

    # Iterate over the remaining lines, starting from the second line
    last_voice = "default"
    i = 1
    while i < len(lines):
        current_line = lines[i].strip()

        if not current_line:
            # Skip empty lines
            i += 1
            continue

        # Determine if the current line is a character name which tells us it's their POV
        split_line = current_line.strip().split(" ")
        first_word = split_line[0].lower()
        add_break = False
        # The character's names are no more than 3 words
        if len(split_line) <= 3:
            add_break = True
        if first_word in character_voice_mapping:
            voice = character_voice_mapping.get(first_word, "default")
            last_voice = voice
        else:
            voice = last_voice

        # Combine content from subsequent lines if they share the same voice
        if has_next(lines, i):
            next_line = lines[i + 1].strip()
            if add_break:
                content = current_line + '<break time="2s" />' + "\n" + next_line
            else:
                content = current_line + "\n" + next_line
            i += 2  # Skip the next line because we just included it
        else:
            content = current_line
            i += 1

        # Check if the current voice is the same as the last appended voice
        if character_content and character_content[-1]['voice'] == voice:
            # Combine content with the previous entry if the voice matches
            character_content[-1]['content'] += "\n" + content
        else:
            # Create a new entry for a different voice
            character_content.append({"voice": voice, "content": content})
        
        # If it's the last line, add a break
        if not has_next(lines, i):
            character_content[-1]['content'] += '<break time="2s" />'

    # Remove any empty content
    character_content = [c for c in character_content if c["content"]]

    return character_content

async def process_text_to_audio(scraped_text_file, text_output_directory, output_audio_directory, index, audio_method):
    """Process a single text file and convert it to multiple audio files by character."""
    text_file_path = os.path.join(text_output_directory, scraped_text_file)
    text_file_number = os.path.splitext(scraped_text_file)[0]  # Extract chapter number from file name

    print(f'Processing file: {scraped_text_file} to audio...')
    with open(text_file_path, 'r', encoding='utf-8') as f:
        text_file_contents = f.read()

    if text_file_contents.startswith("Ars Arcanum\n"):
        # Skip the Ars Arcanum chapters
        return index

    # Split the text by character
    character_contents = split_by_character(text_file_contents)

    # Process each character's content asynchronously
    for char_index, character_content in enumerate(character_contents):
        voice = character_content["voice"]
        content = character_content["content"]

        # Split content if greater than 4095 characters
        max_length = 4095
        content_parts = [content[i:i+max_length] for i in range(0, len(content), max_length)]

        # Create multiple audio files if content is split
        for part_index, content_part in enumerate(content_parts):
            # Create the filename with the format: file_X_XXX.mp3
            file_name = f"file_{text_file_number}_{str(index).zfill(3)}.mp3"
            output_audio_path = os.path.join(output_audio_directory, file_name)

            # Increment the global index
            index += 1

            if voice == "default":
                voice = character_voice_mapping.get("default")

            # Save the character's content part as audio
            try:
                convert_text_to_speech(content_part, output_audio_path, voice, audio_method)
                print(f"Audio file saved at: {output_audio_path}")
            except Exception as e:
                print(f"Error processing text to speech: {e}")
                write_to_error_log(f"For {output_audio_path}: Error processing text to speech: {e}")

    return index  # Return the updated index for the next chapter
