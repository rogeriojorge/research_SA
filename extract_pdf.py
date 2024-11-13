import fitz  # PyMuPDF
import os

import re

def extract_title_from_pdf(pdf_path):
    """
    Extracts the title from the first page of a PDF.
    Assumes that the title is the first line or block of text.
    """
    document = fitz.open(pdf_path)
    first_page = document[0]
    text = first_page.get_text("text")
    
    # Remove any leading/trailing whitespace
    lines = text.split('\n')
    
    # Heuristic: The title is usually the first non-empty line
    for line in lines:
        if line.strip():
            title = line.strip()
            return title
    return "Unknown Title"  # Default return if no title found

def extract_year_from_pdf(pdf_path):
    """
    Extracts the publication year from the PDF.
    The year is often in the metadata or the first few lines of text.
    """
    document = fitz.open(pdf_path)
    
    # Check the metadata for the year
    metadata = document.metadata
    if 'year' in metadata:
        return metadata['year']
    
    # Otherwise, extract the first page and try to find the year in the text
    first_page = document[0]
    text = first_page.get_text("text")
    
    # Try to find a year in the text (e.g., in the form of 2021 or [2021])
    year_match = re.search(r"\b(20\d{2})\b", text)
    if year_match:
        return year_match.group(1)
    
    # If not found, return a placeholder or estimate based on available metadata
    return "Unknown Year"  # Default return if no year found

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text("text")
    return text

# Assuming all PDFs are in a directory
pdf_dir = "path_to_pdfs"
papers = {}

for filename in os.listdir(pdf_dir):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_dir, filename)
        text = extract_text_from_pdf(pdf_path)
        # Extract metadata from PDF (e.g., year, title, abstract)
        # You can use pdfmetadata or regex to capture this info
        papers[filename] = {
            'text': text,
            'year': extract_year_from_pdf(pdf_path),  # Need to implement
            'title': extract_title_from_pdf(pdf_path),  # Need to implement
        }