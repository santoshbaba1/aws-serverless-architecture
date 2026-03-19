import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')

BUCKET_NAME = 'santosh-cleanup-bucket'   
DAYS = 30

def lambda_handler(event, context):

    print("Starting S3 cleanup...")

    # Calculate cutoff date (30 days ago)
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=DAYS)

    # List objects in bucket
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if 'Contents' not in response:
        print("Bucket is empty")
        return "No files found"

    deleted_files = []

    for obj in response['Contents']:
        file_name = obj['Key']
        last_modified = obj['LastModified']

        print(f"Checking file: {file_name} | Last Modified: {last_modified}")

        # Check if file is older than 30 days
        if last_modified < cutoff_date:
            print(f"Deleting: {file_name}")

            s3.delete_object(
                Bucket=BUCKET_NAME,
                Key=file_name
            )

            deleted_files.append(file_name)
        else:
            print(f"Keeping: {file_name}")

    print(f"Deleted files: {deleted_files}")

    return {
        "status": "completed",
        "deleted_files": deleted_files
    }