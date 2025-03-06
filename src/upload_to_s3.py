import os
import logging
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import time
from botocore.config import Config

# Configure logging
logger = logging.getLogger(__name__)

# Configure retry strategy
retry_config = Config(
    retries={
        'max_attempts': 3,
        'mode': 'standard'
    }
)

def upload_to_s3(file_name, bucket, object_name=None):
    logger.info(f"Uploading {file_name} to S3 bucket {bucket}")
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)
    # Upload the file with error handling
    s3_client = boto3.client('s3', config=retry_config)
    try:
        s3_client.upload_file(file_name, bucket, object_name)
        logger.info(f"Successfully uploaded {file_name} to {bucket}")
        return True
    except (BotoCoreError, ClientError) as e:
        logger.error(f"Error uploading {file_name} to {bucket}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error uploading {file_name}: {e}")
    return False
