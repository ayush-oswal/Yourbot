import io
from PyPDF2 import PdfReader  # Ensure you have PyPDF2 installed for PDF processing
import google.generativeai as genai
import dotenv
import os

dotenv.load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest",system_instruction="Provide a very brief, high-level summary in one to two sentences. Focus only on the document's main purpose. Summarize what the document is about, not the content of the document itself.")

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
        all_text = ""
        for page_num, page in enumerate(pdf_reader.pages):
            text = page.extract_text()  # Extract text from the page
            print(f"Page {page_num + 1} content:\n{text}\n")
            all_text += text
        print(f"Processed PDF file: {key}")

        summary = model.generate_content(all_text)

        print(summary.text)
    
    except Exception as e:
        raise RuntimeError(f"Error processing the PDF file '{key}': {str(e)}")