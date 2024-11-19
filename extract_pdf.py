import fitz  # PyMuPDF
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
    full_title = ""
    for i, line in enumerate(lines):
        if line.strip():
            title = line.strip()
            if '0-D' in title or '1-D' in title or '2-D' in title or '3-D' in title or '0D' in title or '1D' in title or '2D' in title or '3D' in title:
                full_title += title + ' '
            elif title[0]=="a" or '202' in title or '201' in title or title=='1' or '(CERN)' in title or 'PREPRINT' in title or 'preprint' in title or 'CMS-' in title or 'et al' in title or title=='Highlights' or 'consideration for publication in' in title:
                continue
            elif '1' in title or '2' in title or '3' in title or '4' in title or '5' in title or '6' in title or '7' in title or '8' in title or '9' in title:# or '0' in title:
                continue
            elif '@' in title or '*' in title or '∗' in title:
                break
            elif 'Institute for' in title or 'a)' in title or 'b)' in title or 'c)' in title or 'd)' in title or 'e)' in title or 'f)' in title or 'g)' in title:
                break
            elif 'Department of ' in title or 'DIFFER' in title or 'Department of' in title or 'University' in title or 'Laboratory' in title or 'Institute' in title or 'Center' in title or 'College' in title or 'School' in title or 'Institut' in title or 'Facility' in title or 'Instituto' in title or 'Faculdade' in title or 'Universidade' in title or 'Universidad' in title or 'Université' in title or 'Università' in title or 'Universität' in title:
                break
            elif 'A.' in title or 'B.' in title or 'C.' in title or 'D.' in title or 'E.' in title or 'F.' in title or 'G.' in title or 'H.' in title or 'I.' in title or 'J.' in title or 'K.' in title or 'L.' in title or 'M.' in title or 'N.' in title or 'O.' in title or 'P.' in title or 'Q.' in title or 'R.' in title or 'S.' in title or 'T.' in title or 'U.' in title or 'V.' in title or 'W.' in title or 'X.' in title or 'Y.' in title or 'Z.' in title:
                break
            elif 'Abstract.' in title or 'USA' in title or 'Culham' in title or 'Princeton' in title:
                break
            elif i>=4:
                break
            else:
                full_title += title + ' '
        if i>=3:
            break
    return full_title

def extract_year_from_pdf(pdf_path):
    """
    Extracts the publication year from the PDF.
    The year is often in the metadata or the first few lines of text.
    """
    document = fitz.open(pdf_path)
    
    
    # Otherwise, extract the first page and try to find the year in the text
    first_page = document[0]
    text = first_page.get_text("text")
    
    year_match_arxiv = re.search(r"arXiv:\d{2}", text)
    matches = re.findall(r"arXiv:\d{2}", text)
    if matches:
        return '20'+matches[0][-2:]
    # Try to find a year in the text (e.g., in the form of 2021 or [2021])
    year_match = re.search(r"\b(20\d{2})\b", text)
    if year_match:
        return year_match.group(1)
    
    # Check the metadata for the year
    metadata = document.metadata
    if 'year' in metadata:
        return metadata['year']
    
    # If not found, return a placeholder or estimate based on available metadata
    return "Unknown Year"  # Default return if no year found

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text("text")
    return text

