from dotenv import load_dotenv
import os
from export_data import export_data
from upload_to_s3 import upload_to_s3

load_dotenv()

sanity_project_id = os.getenv("SANITY_PROJECT_ID")
sanity_api_token = os.getenv("SANITY_API_READ_TOKEN")
aws_bucket_name = os.getenv("AWS_BUCKET_NAME")

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