import google.generativeai as genai
import dotenv
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter


dotenv.load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest",system_instruction="Provide a very brief, high-level summary, please emphazise on the following points: length of the summary should be proportional to the length of the document but not more than 75 words, the smaller the document the shorter the summary should be. Focus only on the document's main purpose. Summarize what the document is about, not the content of the document itself. Again, the summary should be very brief and to the point.")

class TextChunker:
    def __init__(self):
        pass
    
    def get_summary(self, text: str):
        summary = model.generate_content(text)
        return summary.text

    def chunk_text(self, text: str, chunk_size=350, chunk_overlap=50):
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
                combined_chunk = f"{summary}\n{overlap_text}{chunk}"  # Add overlap and summary to the current chunk
            else:
                # For the first chunk, we don't have a previous chunk to get overlap from
                combined_chunk = f"{summary}{chunk}"

            # Append the formatted chunk to the list and print it
            formatted_chunks.append(combined_chunk)
            print(combined_chunk, "\n\n")  # Print each formatted chunk with overlap and summary

        print(f"Total number of chunks: {len(formatted_chunks)}")
        return formatted_chunks
