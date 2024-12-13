import os
import json
from PyPDF2 import PdfReader

def read_pdf_file(file_path):
    """Reads the content of a PDF file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_text(text, chunk_size):
    """Splits the text into chunks of approximately `chunk_size` characters."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0

    for word in words:
        word_length = len(word) + 1  # +1 for the space
        if current_size + word_length > chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_size = 0
        current_chunk.append(word)
        current_size += word_length

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def format_chunks(chunks):
    """Formats chunks into the desired output structure."""
    formatted_chunks = []
    for idx, chunk in enumerate(chunks, start=1):
        formatted_chunks.append({"id": f"chunk{idx}", "text": chunk})
    return formatted_chunks

def save_chunks_to_file(chunks, output_path):
    """Saves the formatted chunks to a JSON file."""
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(chunks, file, indent=4)

if __name__ == "__main__":
    input_path = input("Enter the path to the PDF file: ").strip()
    if not os.path.exists(input_path):
        print("The specified PDF file does not exist. Exiting.")
        exit()

    output_path = input("Enter the path for the output JSON file: ").strip()
    chunk_size = int(input("Enter the chunk size (number of characters): ").strip())

    try:
        text = read_pdf_file(input_path)
        chunks = chunk_text(text, chunk_size)
        formatted_chunks = format_chunks(chunks)
        save_chunks_to_file(formatted_chunks, output_path)
        print(f"Chunks saved successfully to {output_path}")
    except Exception as e:
        print(f"Error: {e}")
