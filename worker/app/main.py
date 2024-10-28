import json
from redis import Redis
from rq import Worker, Queue, Connection
from services.s3_operations import S3Operations
from processors.pdf_processor import process_pdf
from processors.text_processor import process_text
import os
import dotenv

dotenv.load_dotenv()

# Constants
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# Initialize Redis connection
redis_conn = Redis.from_url("redis://localhost:6379")

def worker_task(data):
    """
    This function will be executed by the worker.
    
    Args:
        data (str): JSON string containing file information from the queue.
    
    Returns:
        None
    """
    message = json.loads(data)  # Decode the JSON message from the Redis queue

    download_url = message["download_url"]
    chatbot_id = message["chatbot_id"]
    filename = message["filename"]


    # Download the file from S3 using the download_object method
    s3_operations = S3Operations()
    file_bytes = s3_operations.download_object(download_url)

    # Determine file type and process accordingly
    if filename.endswith('.pdf'):
        process_pdf(file_bytes, filename, chatbot_id)
    elif filename.endswith('.txt'):
        process_text(file_bytes, filename, chatbot_id)
    else:
        print(f"Unsupported file type for '{filename}'")

# Setup the worker
if __name__ == "__main__":
    with Connection(redis_conn):
        worker = Worker(Queue("process_file"))
        print("Worker is starting...")
        while True:
            worker.work()
