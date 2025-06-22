import json
import asyncio
import dotenv
from app.services.s3_operations import S3Operations
from app.processors.pdf_processor import process_pdf
from app.processors.text_processor import process_text

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
        return {"statusCode": 200, "body": f"Successfully processed {key}"}
            
    except Exception as e:
        print(f"Error processing task: {str(e)}")
        raise e

def lambda_handler(event, context):
    """Lambda handler function - entry point for AWS Lambda."""
    try:
        # Lambda SQS trigger provides records in event
        for record in event.get('Records', []):
            # Extract message body from SQS record
            message_body = record['body']
            
            print(f"Processing message: {record.get('messageId', 'unknown')}")
            
            # Run async function
            result = asyncio.run(process_file(message_body))
            
        return {
            "statusCode": 200,
            "body": json.dumps("All messages processed successfully")
        }
        
    except Exception as e:
        print(f"Lambda execution error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error: {str(e)}")
        }