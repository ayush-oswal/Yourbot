
def process_text(text_bytes: bytes, filename: str, chatbot_id: str):
    """
    Process the downloaded text bytes and extract content.

    Args:
        text_bytes (bytes): The content of the text file in bytes.
        filename (str): The name of the file for processing reference.

    Returns:
        None
    """
    try:
        text_content = text_bytes.decode('utf-8')  # Decode bytes to string
        print(f"Content of '{filename}':\n{text_content}\n")
        
        print(f"Processed text file: {filename}")
    
    except Exception as e:
        raise RuntimeError(f"Error processing the text file '{filename}': {str(e)}")