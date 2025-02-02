from app.core.text_chunker import TextChunker
from app.core.jina_ai import JinaAI
from app.core.user import get_user_details, update_user_tokens
from app.core.store_chunks import store_chunks
from app.core.pinecone import upsert_chunks

async def process_text(text_bytes: bytes, key: str, chatbot_id: str, user_id: str):
    """
    Process the downloaded text bytes and extract content.

    Args:
        text_bytes (bytes): The content of the text file in bytes.
        key (str): The name of the file for processing reference.

    Returns:
        None
    """
    try:
        text_content = text_bytes.decode('utf-8')  # Decode bytes to string
        

        # Chunking the text into smaller chunks
        chunks = TextChunker().chunk_text(text_content)

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
        
    except Exception as e:
        raise RuntimeError(f"Error processing the text file '{key}': {str(e)}")