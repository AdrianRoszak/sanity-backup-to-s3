from dotenv import load_dotenv
import os
import requests
import boto3

load_dotenv()

sanity_project_id = os.getenv("SANITY_PROJECT_ID")
sanity_api_token = os.getenv("SANITY_API_READ_TOKEN")
aws_bucket_name = os.getenv("AWS_BUCKET_NAME")

def export_data(dataset_name: str, output_file: str):
    headers = {
        "Authorization": f"Bearer {sanity_api_token}",
    }

    sanity_api_url = f"https://{sanity_project_id}.api.sanity.io/v2021-06-07/data/export/{dataset_name}"

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

def upload_to_s3(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except Exception as e:
        print(f"Error uploading {file_name} to {bucket}: {e}")
        return False
    return True

def main():
    print("")
    print(f"Welcome, you are in the module - {__name__}. Have fun.")
    print("---------------------------------------------------------------------")
    print("")
    output_file = f"production_backup_{sanity_project_id}.ndjson"
    export_data("production", output_file)
    
    # Upload the exported file to S3
    success = upload_to_s3(output_file, aws_bucket_name)
    if success:
        print(f"Successfully uploaded {output_file} to {aws_bucket_name}")
    else:
        print(f"Failed to upload {output_file} to {aws_bucket_name}")

if __name__ == "__main__":
    main()