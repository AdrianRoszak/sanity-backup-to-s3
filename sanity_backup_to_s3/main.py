from dotenv import load_dotenv
import os
import requests

load_dotenv()

sanity_project_id = os.getenv("SANITY_PROJECT_ID")
sanity_api_token = os.getenv("SANITY_API_BACKUP_TOKEN")

def export_data(dataset_name: str, output_file: str):
    headers = {
        "Authorization": f"Bearer {sanity_api_token}",
    }

    sanity_api_url = f"https://{sanity_project_id}.api.sanity.io/v2021-06-07/data/export/{dataset_name}"

    # Wyślij żądanie GET do API Sanity
    response = requests.get(sanity_api_url, headers=headers, stream=True)

    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Dane zostały pomyślnie wyeksportowane do {output_file}")
    else:
        print(f"Nie udało się wyeksportować danych: {response.status_code}")
        print(response.text)

def main():
    print("")
    print(f"Witaj, jesteś w module - {__name__}. Miłej zabawy.")
    print("---------------------------------------------------------------------")
    print("")
    export_data("production", "production_backup.ndjson")

if __name__ == "__main__":
    main()