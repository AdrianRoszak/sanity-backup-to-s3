from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

# Access variables using os.getenv
sanity_project_id = os.getenv("SANITY_PROJECT_ID")
sanity_api_token = os.getenv("SANITY_API_BACKUP_TOKEN")

# Sanity Export API URL
sanity_api_url = os.getenv("SANITY_API_URL")

def export_data(dataset_name: str, output_file: str):
    # Set headers with the authorization token
    headers = {
        "Authorization": f"Bearer {sanity_api_token}",
    }

    # Set the parameters for the export (e.g., dataset name and format)
    params = {
        "dataset": dataset_name,
        "format": "ndjson",  # Format the data as ndjson
    }

    # Send GET request to the Sanity API
    response = requests.get(sanity_api_url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"Data successfully exported to {output_file}")
    else:
        print(f"Failed to export data: {response.status_code}")
        print(response.text)

# Export the production dataset
export_data("production", "production_backup.ndjson")
