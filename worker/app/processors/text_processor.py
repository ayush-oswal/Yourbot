import google.generativeai as genai
import dotenv
import os

dotenv.load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest",system_instruction="Provide a very brief, high-level summary in one sentence. Focus only on the document's main purpose. Summarize what the document is about, not the content of the document itself.")

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
        


        summary = model.generate_content(text_content)

        print(summary.text)
    
    except Exception as e:
        raise RuntimeError(f"Error processing the text file '{key}': {str(e)}")