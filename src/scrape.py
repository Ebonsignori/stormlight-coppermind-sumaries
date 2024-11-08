import requests
import os
from bs4 import BeautifulSoup
from utils import get_root_directory, write_to_error_log

def scrape_summary(url, title_output_directory):
    """Scrape the webpage at the given url and save each chapter to individual files."""

    def get_title(parent_element):
        """Extract the title from a parent element."""
        span_tag = parent_element.find('span', class_='mw-headline')
        if span_tag:
            a_tag = span_tag.find('a')
            if a_tag:
                return a_tag.get_text()
            else:
                return span_tag.get_text()
        return None

    def fetch_page():
        """Fetch the page content."""
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            write_to_error_log(f"Failed to retrieve the webpage: {url}. Status code: {response.status_code}")
            return None

    page_content = fetch_page()
    if not page_content:
        return

    soup = BeautifulSoup(page_content, 'html.parser')
    content_div = soup.find('div', class_='mw-parser-output')

    current_part = None
    current_chapter = None
    current_content = []
    chapter_number = 0
    part_has_direct_content = False  # Track if the part has direct content

    def save_chapter_to_file(chapter, content, chapter_num):
        """Helper function to save chapter content to a file."""
        with open(f"{title_output_directory}/{chapter_num}.txt", 'w', encoding='utf-8') as f:
            if chapter:  # If there's a chapter title, include it
                f.write(chapter + "\n\n")
            if content:  # Write the content only if it's present
                f.write('\n'.join(content))

    def save_part_with_direct_content_to_file(part, content, chapter_num):
        """Helper function to save part content (without chapters) to a file."""
        with open(f"{title_output_directory}/{chapter_num}.txt", 'w', encoding='utf-8') as f:
            f.write(part + "\n\n")
            if content:  # Write the content only if it's present
                f.write('\n'.join(content))

    def save_current_content():
        """Decide whether to save a chapter or a part with direct content."""
        nonlocal chapter_number
        if current_chapter:  # If we're dealing with a chapter, save it
            chapter_number += 1
            save_chapter_to_file(current_chapter, current_content, chapter_number)
        elif current_part and part_has_direct_content:  # If the part has direct content, save it
            chapter_number += 1
            save_part_with_direct_content_to_file(current_part, current_content, chapter_number)

    for element in content_div.children:
        if element.name == 'h2':  # Part title (new section)
            # Save the previous part's contents (if it has direct content) or chapter contents
            save_current_content()

            # Now reset for the new part
            current_part = get_title(element)  # Reset to the new part
            current_chapter = None  # Reset the chapter for the new part
            current_content = []  # Reset content for the new part
            part_has_direct_content = False  # Reset the direct content tracker for the new part

        elif element.name == 'h3':  # Chapter title (within the part)
            # Save the previous chapter's content before starting a new one
            save_current_content()

            # Now handle the new chapter
            current_chapter = get_title(element)
            current_content = []  # Reset content for the new chapter
            part_has_direct_content = False  # This part now contains chapters, not direct content

        elif element.name == 'p':  # Content (either for chapter or part)
            if current_part:  # Only append content if we are within a part
                if current_chapter:  # If we're in a chapter, append to the chapter's content
                    current_content.append(element.get_text().strip())
                else:  # If there's no chapter yet, it's direct content for the part
                    current_content.append(element.get_text().strip())
                    part_has_direct_content = True  # Track that this part has direct content

    # Save the last chapter or part content if available
    save_current_content()

# Example usage:
if __name__ == "__main__":
    output_directory = os.join(get_root_directory(), 'text', 'The_Way_of_Kings')
    url = 'https://coppermind.net/wiki/Summary:The_Way_of_Kings'
    os.makedirs(output_directory, exist_ok=True)
    scrape_summary(url, output_directory)
