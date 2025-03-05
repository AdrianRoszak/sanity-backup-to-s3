import os
import logging
import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv(verbose=True, override=True)

sanity_project_id = os.getenv("SANITY_PROJECT_ID")
sanity_api_token = os.getenv("SANITY_API_READ_TOKEN")

# Configure retry strategy
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[408, 429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)

def export_data(dataset_name: str, output_file: str):
    logger.info(f"Exporting data from {dataset_name} dataset")
    headers = {
        "Authorization": f"Bearer {sanity_api_token}",
    }

    sanity_api_url = f"https://{sanity_project_id}.api.sanity.io/v2021-06-07/data/export/{dataset_name}"

    try:
        # Send GET request to Sanity API with retry logic
        response = http.get(sanity_api_url, headers=headers, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        bytes_written = 0
        
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    bytes_written += len(chunk)
                    logger.debug(f"Written {bytes_written}/{total_size} bytes")
        
        logger.info(f"Successfully exported {bytes_written} bytes to {output_file}")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to export data: {e}")
        return False
