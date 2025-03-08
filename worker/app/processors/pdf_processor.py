import io
from PyPDF2 import PdfReader  # Ensure you have PyPDF2 installed for PDF processing
from app.core.text_chunker import TextChunker
from app.core.jina_ai import JinaAI
from app.core.user import get_user_details, update_user_tokens
from app.core.store_chunks import store_chunks
from app.core.pinecone import upsert_chunks
from app.services.send_mail import send_mail

async def process_pdf(pdf_bytes: bytes, key: str, chatbot_id: str, user_id: str):
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
        for page in pdf_reader.pages:
            text = page.extract_text()  # Extract text from the page
            all_text += text
        print(f"Processing PDF file: {key}")

        # Chunking the text into smaller chunks
        chunks = TextChunker().chunk_text(all_text) 

        # Get user tokens from postgres
        user_tokens, user_email = await get_user_details(user_id)

        # Get embeddings from Jina AI

        embeddings, total_tokens = JinaAI().fetch_embeddings(chunks, user_tokens)
        print(f"Embeddings: {len(embeddings)}")
        print(f"Total tokens used: {total_tokens}")

        # Update user tokens in postgres
        await update_user_tokens(user_id, user_tokens - total_tokens)

        # for len of embeddings, store in postgres, then store in pinecone along with metadata which includes the chatbot_id and chunk_id from postgres

        chunks = chunks[:len(embeddings)]
        chunk_ids = await store_chunks(chunks)

        # Store in pinecone
        await upsert_chunks(chunk_ids, embeddings, chatbot_id)

        # Send email to user of successful processing and also if 0 tokens left
        await send_mail(subject="PDF processed successfully", body="Your PDF has been processed successfully", to_email=user_email)
        if user_tokens == 0:
            await send_mail(subject="Your tokens have run out", body="Please recharge your tokens", to_email=user_email)


    except Exception as e:
        raise RuntimeError(f"Error processing the PDF file '{key}': {str(e)}")