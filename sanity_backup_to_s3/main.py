import logging
from dotenv import load_dotenv
import os
from export_data import export_data
from upload_to_s3 import upload_to_s3

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

# Validate environment variables
required_env_vars = [
    "SANITY_PROJECT_ID",
    "SANITY_API_READ_TOKEN", 
    "AWS_BUCKET_NAME"
]

missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

sanity_project_id = os.getenv("SANITY_PROJECT_ID")
sanity_api_token = os.getenv("SANITY_API_READ_TOKEN")
aws_bucket_name = os.getenv("AWS_BUCKET_NAME")

def main():
    logger.info(f"Starting backup process for project: {sanity_project_id}")
    try:
        output_file = f"production_backup_{sanity_project_id}.ndjson"
        export_data("production", output_file)
        
        # Upload the exported file to S3
        success = upload_to_s3(output_file, aws_bucket_name)
        if success:
            logger.info(f"Successfully uploaded {output_file} to {aws_bucket_name}")
            # Clean up local file after successful upload
            try:
                os.remove(output_file)
                logger.info(f"Removed local file: {output_file}")
            except OSError as e:
                logger.warning(f"Failed to remove local file: {e}")
        else:
            logger.error(f"Failed to upload {output_file} to {aws_bucket_name}")
    except Exception as e:
        logger.error(f"Backup process failed: {e}")
        raise

if __name__ == "__main__":
    main()
