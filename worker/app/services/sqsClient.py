import boto3
import os
from botocore.exceptions import ClientError

class SQSClient:
    def __init__(self):
        # Initialize SQS client
        self.sqs = boto3.client(
            'sqs',
            region_name=os.getenv('AWS_REGION', 'us-east-1'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        
        # Get queue URL from environment
        self.queue_url = os.getenv('AWS_SQS_URL')
        if not self.queue_url:
            raise ValueError("AWS_SQS_URL environment variable is required")
        
        print(f"SQS Client initialized with queue: {self.queue_url}")
    
    def receive_messages(self, max_messages=1, wait_time=20):
        """Receive messages from SQS queue"""
        try:
            response = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=wait_time,  # Long polling
                MessageAttributeNames=['All']
            )
            
            messages = response.get('Messages', [])
            print(f"Received {len(messages)} messages from SQS")
            return messages
            
        except ClientError as e:
            print(f"Error receiving messages from SQS: {e}")
            raise e
    
    def delete_message(self, receipt_handle):
        """Delete a processed message from SQS"""
        try:
            self.sqs.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle
            )
            print("Message deleted successfully")
        except ClientError as e:
            print(f"Error deleting message from SQS: {e}")
            raise e

# Initialize SQS client
sqs_client = SQSClient()
