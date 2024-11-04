import io
from PyPDF2 import PdfReader  # Ensure you have PyPDF2 installed for PDF processing
from app.core.text_chunker import TextChunker
from app.core.jina_ai import JinaAI

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

        # Chunking the text into smaller chunks
        chunks = TextChunker().chunk_text(all_text) 

        embeddings, total_tokens = JinaAI().fetch_embeddings(chunks)
        print(f"Embeddings: {len(embeddings)}")
        print(f"Total tokens used: {total_tokens}")
        # For every chunk, store in postgres, obtain embeddings from Jina AI, then store in pinecone along with metadata which includes the chatbot_id and chunk_id from postgres

    except Exception as e:
        raise RuntimeError(f"Error processing the PDF file '{key}': {str(e)}")