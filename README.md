# Sanity Backup to S3

This project provides a script to export data from Sanity and upload it to an AWS S3 bucket.

## Requirements

- Python 3.12 or higher

## Installation

1. Clone the repository:

```sh
$ git clone <repository-url>
$ cd sanity-backup-to-s3
```

2. Install the dependencies:

```sh
$ pip install poetry
$ poetry install
```

## Configuration

1. Copy the `.env.example` file to `.env` and fill in your credentials:

```sh
$ cp .env.example .env
```

2. Edit the `.env` file and add your Sanity project ID, API token, and AWS credentials:

```
SANITY_PROJECT_ID=<your-sanity-project-id>
SANITY_API_READ_TOKEN=<your-sanity-api-token>
AWS_ACCESS_KEY_ID=<your-aws-access-key-id>
AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key>
AWS_BUCKET_NAME=<your-s3-bucket-name>
```

## Usage

Run the main script to export data from Sanity and upload it to S3:

```sh
$ poetry run sanity
```

## Project Structure

- `main.py`: The main script to run the backup process.
- `sanity_backup_to_s3/`: Contains the modules for exporting data and uploading to S3.
  - `export_data.py`: Module to export data from Sanity.
  - `upload_to_s3.py`: Module to upload the exported data to S3.
- `tests/`: Contains test cases for the project.

## License

This project is licensed under the MIT License.
