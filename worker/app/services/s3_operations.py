import requests

class S3Operations:
    def download_object(download_url: str) -> bytes:
        """
        Download an object from S3 and return its content as bytes.

        Args:
            object_key (str): The key of the object in S3.
            bucket_name (str): The name of the S3 bucket.

        Returns:
            bytes: The content of the object in bytes.
        """
        try:
            response = requests.get(download_url)

            # Check if the request was successful
            if response.status_code == 200:
                return response.content  # Return the content as bytes
            else:
                raise RuntimeError(f"Error downloading object: {response.status_code} - {response.text}")

        except requests.RequestException as e:
            raise RuntimeError(f"Error downloading object: {str(e)}")
