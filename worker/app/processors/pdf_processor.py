import io
from PyPDF2 import PdfReader  # Ensure you have PyPDF2 installed for PDF processing

def process_pdf(pdf_bytes: bytes, key: str, chatbot_id: str, user_id: str):
    """
    Process the downloaded PDF bytes and extract content.

    Args:
        pdf_bytes (bytes): The content of the PDF in bytes.
        key (str): The name of the file for processing reference.

    Returns:
        None
    """
    try:
        # Create a PDF reader object using the bytes
        pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
        
        # Iterate through the pages and extract text or perform any other processing
        for page_num, page in enumerate(pdf_reader.pages):
            text = page.extract_text()  # Extract text from the page
            print(f"Page {page_num + 1} content:\n{text}\n")
        
        print(f"Processed PDF file: {key}")
    
    except Exception as e:
        raise RuntimeError(f"Error processing the PDF file '{key}': {str(e)}")