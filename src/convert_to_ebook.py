import os
from config import get_coppermind_url_map
from ebooklib import epub
from utils import get_root_directory, sanitize_title
import re

def parse_file(file_path):
    """Parses the content of a file and returns the chapter title and content."""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # First line is the title, the rest is the content
    title = lines[0].strip()
    content = "".join(lines[1:]).strip()
    
    return title, content


def numerical_sort_key(file_name):
    """Extracts the numeric part of the file name for proper sorting."""
    match = re.search(r'(\d+)', file_name)
    return int(match.group()) if match else file_name

def create_epub(book_title, text_files, output_dir):
    # Create an EPUB book object
    book = epub.EpubBook()
    
    # Set metadata
    book.set_title(book_title)
    book.set_language('en')

    # Initialize a list to hold the chapters
    chapters = []

    # Loop through text files and add them as chapters
    for i, text_file in enumerate(text_files, start=1):
        title, content = parse_file(text_file)

        # Skip the Ars Arcanum chapters
        if title == "Ars Arcanum":
            continue

        # Create a chapter for each text file
        chapter = epub.EpubHtml(
            title=title,
            file_name=f'chapter_{i}.xhtml',
            lang='en'
        )
        innerContent = content.replace("\n", "<br>")
        chapter.content = f'<h1>{title}</h1><p>{innerContent}</p>'
        
        # Add chapter to the book
        book.add_item(chapter)
        chapters.append(chapter)

    # Set the table of contents and spine of the book
    book.toc = chapters
    book.spine = ['nav'] + chapters

    # Add default navigation files (required for epub)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Write the EPUB file
    epub_file = os.path.join(output_dir, f'{book_title}_Summary.epub')
    epub.write_epub(epub_file, book, {})

    print(f'Ebook created: {epub_file}')


if __name__ == "__main__":
    os.makedirs('ebooks', exist_ok=True)

    for book_title in get_coppermind_url_map():
        title = sanitize_title(book_title)
        book_dir = os.path.join(get_root_directory(), 'text', title)
        
        # Find all text files in the book directory and sort them numerically
        text_files = sorted(
            [os.path.join(book_dir, f) for f in os.listdir(book_dir) if f.endswith('.txt')],
            key=numerical_sort_key
        )

        if text_files:
            create_epub(title, text_files, 'ebooks')