import pypdf

def extract_text_from_pdf(pdf_file):
    """
    Extracts all plain text from an uploaded PDF file using pypdf.
    
    Args:
        pdf_file: Uploaded file-like object containing the PDF data.
        
    Returns:
        str: Combined plain text extracted from all pages, trimmed of whitespace.
    """
    reader = pypdf.PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()
