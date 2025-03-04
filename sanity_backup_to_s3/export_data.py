import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

sanity_project_id = os.getenv("SANITY_PROJECT_ID")
sanity_api_token = os.getenv("SANITY_API_READ_TOKEN")

# Debug prints to verify environment variables
print(f"SANITY_PROJECT_ID: {sanity_project_id}")
print(f"SANITY_API_READ_TOKEN: {sanity_api_token}")

def export_data(dataset_name: str, output_file: str):
    headers = {
        "Authorization": f"Bearer {sanity_api_token}",
    }

    sanity_api_url = f"https://{sanity_project_id}.api.sanity.io/v2021-06-07/data/export/{dataset_name}"

    # Debug print to verify constructed URL
    print(f"Sanity API URL: {sanity_api_url}")

    # Send GET request to Sanity API
    response = requests.get(sanity_api_url, headers=headers, stream=True)

    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Data successfully exported to {output_file}")
    else:
        print(f"Failed to export data: {response.status_code}")
        print(response.text)
