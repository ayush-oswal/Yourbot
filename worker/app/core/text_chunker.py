import google.generativeai as genai
import dotenv
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
import time
from app.constants.prompts import SYSTEM_INSTRUCTION

dotenv.load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(model_name="gemini-2.0-flash-thinking-exp-01-21",system_instruction=SYSTEM_INSTRUCTION)

class TextChunker:
    def __init__(self):
        pass
    
    def get_summary(self, text: str):
        while True:
            try:
                summary = model.generate_content(text).text
                return summary
            except Exception as e:
                print(f"Error occurred: {e}. Retrying in 20 seconds...")
                time.sleep(20)

    def chunk_text(self, text: str, chunk_size=550, chunk_overlap=75):
        summary = self.get_summary(text)
        chunks = self.text_splitter(text,summary, chunk_size, chunk_overlap)
        return chunks

    def text_splitter(self, text: str, summary: str, chunk_size: int, chunk_overlap: int, separators: list[str] = ["\n\n", "\n"]) -> list[str]:
        """
        Splits text into chunks based on specified size, overlap, and separators.

        Args:
        - text (str): The text to be chunked.
        - chunk_size (int): The maximum size of each chunk.
        - chunk_overlap (int): The number of overlapping characters between chunks.
        - separators (list): List of separator strings to use for splitting.

        Returns:
        - List[str]: A list of text chunks.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap,
            separators=separators
            )
        chunks = text_splitter.split_text(text)
        
        # include some text to previous chunk into current chunk and add summary to the chunk and print in formatted way
        formatted_chunks = []

        for i, chunk in enumerate(chunks):
            # Get overlap text from the end of the previous chunk if it's not the first chunk
            if i > 0:
                previous_chunk = chunks[i - 1]
                overlap_text = previous_chunk[-chunk_overlap:]  # Extract overlap from the end of the previous chunk
                combined_chunk = f"{overlap_text}{chunk}\n{summary}"  # Add overlap and summary to the current chunk
            else:
                # For the first chunk, we don't have a previous chunk to get overlap from
                combined_chunk = f"{chunk}\n{summary}"

            # Append the formatted chunk to the list and print it
            formatted_chunks.append(combined_chunk)
            print(combined_chunk)

        print(f"Total number of chunks: {len(formatted_chunks)}")
        return formatted_chunks
