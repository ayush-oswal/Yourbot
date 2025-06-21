import boto3
import json
import os
from typing import Dict, Any
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
        
    def send_message(self, queue_name: str, message: Dict[Any, Any]):
        """Send a message to SQS queue"""
        try:
            json_message = json.dumps(message)
            
            response = self.sqs.send_message(
                QueueUrl=self.queue_url,
                MessageBody=json_message,
                MessageAttributes={
                    'queue_name': {
                        'StringValue': queue_name,
                        'DataType': 'String'
                    }
                }
            )
            
            message_id = response['MessageId']
            return message_id
            
        except ClientError as e:
            print(f"Error sending message to SQS: {e}")
            raise e
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise e

# Initialize SQS client
sqs_client = SQSClient()

# Function to replace lpush_to_queue
def send_to_queue(queue_name: str, message: Dict[Any, Any]):
    """Send message to SQS queue (replaces lpush_to_queue)"""
    return sqs_client.send_message(queue_name, message)