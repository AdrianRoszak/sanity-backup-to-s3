import os
import logging
from dotenv import load_dotenv

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
