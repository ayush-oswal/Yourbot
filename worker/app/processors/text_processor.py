from app.core.text_chunker import TextChunker
from app.core.jina_ai import JinaAI
def process_text(text_bytes: bytes, key: str, chatbot_id: str, user_id: str):
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
        print(f"Content of '{key}':\n{text_content}\n")
        



        # Chunking the text into smaller chunks
        chunks = TextChunker().chunk_text(text_content)

        embeddings, total_tokens = JinaAI().fetch_embeddings(chunks)
        print(f"Embeddings: {len(embeddings)}")
        print(f"Total tokens used: {total_tokens}")

        # For every chunk store in postgres, then store in pinecone along with metadata which includes the chatbot_id and chunk_id from postgres
    
    except Exception as e:
        raise RuntimeError(f"Error processing the text file '{key}': {str(e)}")