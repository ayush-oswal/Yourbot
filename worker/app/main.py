# import json
# import time
# from redis import Redis
# import os
# import dotenv
# from app.services.s3_operations import S3Operations
# from app.processors.pdf_processor import process_pdf
# from app.processors.text_processor import process_text
# import asyncio



# dotenv.load_dotenv()

# # Constants
# redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

# # Initialize Redis connection
# redis_conn = Redis.from_url(redis_url)

# async def process_file(data):
#     """Process the data received from the queue."""
#     try:

#         if isinstance(data, bytes):
#             data = data.decode('utf-8')

#         message = json.loads(data) if isinstance(data, str) else data
        
#         download_url = message["download_url"]
#         chatbot_id = message["chatbot_id"]
#         key = message["key"]
#         user_id = message["user_id"]

#         # Download the file from S3
#         s3_operations = S3Operations()
#         file_bytes = s3_operations.download_object(download_url)

#         # Determine file type and process accordingly
#         if key.endswith('.pdf'):
#             await process_pdf(file_bytes, key, chatbot_id, user_id)
#         elif key.endswith('.txt'):
#             await process_text(file_bytes, key, chatbot_id, user_id)
#         else:
#             print(f"Unsupported file type for '{key}'")
            
#     except Exception as e:
#         print(f"Error processing task: {str(e)}")

# async def start_worker():
#     """Continuously listen for new jobs in the Redis queue."""
#     while True:
#         try:
#             # Use BRPOP to wait for messages on the queue
#             data = redis_conn.brpop("process_file", timeout=0)  # Timeout 0 means wait indefinitely
#             if data:
#                 # The data returned by brpop is a tuple (queue_name, message)
#                 message = data[1]  # Extract the message from the tuple
#                 await process_file(message)  # Process the message
#         except Exception as err:
#             print(f"Error {err}")
#             time.sleep(1)  # Optional: Sleep before retrying


# if __name__ == "__main__":
#     print("Worker is starting...")
#     asyncio.run(start_worker())


import json
import time
import dotenv
import asyncio
from app.services.s3_operations import S3Operations
from app.processors.pdf_processor import process_pdf
from app.processors.text_processor import process_text
from app.services.sqsClient import sqs_client

dotenv.load_dotenv()

async def process_file(message_body):
    """Process the data received from SQS."""
    try:
        if isinstance(message_body, str):
            message = json.loads(message_body)
        else:
            message = message_body
        
        download_url = message["download_url"]
        chatbot_id = message["chatbot_id"]
        key = message["key"]
        user_id = message["user_id"]

        print(f"Processing file: {key} for chatbot: {chatbot_id}")

        # Download the file from S3
        s3_operations = S3Operations()
        file_bytes = s3_operations.download_object(download_url)

        # Determine file type and process accordingly
        if key.endswith('.pdf'):
            await process_pdf(file_bytes, key, chatbot_id, user_id)
        elif key.endswith('.txt'):
            await process_text(file_bytes, key, chatbot_id, user_id)
        else:
            print(f"Unsupported file type for '{key}'")
            
        print(f"Successfully processed file: {key}")
            
    except Exception as e:
        print(f"Error processing task: {str(e)}")
        raise e

async def start_sqs_worker():
    """Continuously poll SQS for new messages."""
    print("SQS Worker is starting...")
    print(f"Polling queue: {sqs_client.queue_url}")
    
    while True:
        try:
            messages = sqs_client.receive_messages(max_messages=1, wait_time=20)
            
            if not messages:
                print("No messages received, continuing to poll...")
                continue
            
            for message in messages:
                try:
                    message_body = json.loads(message['Body'])
                    receipt_handle = message['ReceiptHandle']
                    
                    print(f"Received message: {message['MessageId']}")
                    
                    await process_file(message_body)
                    
                    sqs_client.delete_message(receipt_handle)
                    print(f"Message {message['MessageId']} processed and deleted successfully")
                    
                except Exception as e:
                    print(f"Error processing message {message.get('MessageId', 'unknown')}: {str(e)}")
                    # Don't delete the message - it will become visible again after visibility timeout
                    # SQS will retry the message automatically
                    
        except Exception as err:
            print(f"Error in SQS polling: {err}")
            time.sleep(5)

if __name__ == "__main__":
    print("Starting SQS Worker...")
    asyncio.run(start_sqs_worker())