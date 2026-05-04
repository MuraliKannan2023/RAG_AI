import os
from pypdf import PdfReader  # Library to read and extract text from PDF files

def read_pdf(pdf_path):
    """
    Reads a PDF file and extracts text from all pages.
    
    Args:
        pdf_path (str): The file path to the PDF document.
    
    Returns:
        list[str]: A list of strings, where each string contains 
                   the text extracted from one page of the PDF.
    """

    # Check if the file exists before trying to read it
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"The file {pdf_path} does not exist.")
    
    # Create a PdfReader object to parse the PDF file
    reader = PdfReader(pdf_path)

    # Loop through each page and extract its text content into a list
    pages = [page.extract_text() for page in reader.pages]

    # Return the list of page texts
    return pages