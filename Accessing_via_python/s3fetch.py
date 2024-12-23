import boto3
import os

AWS_ACCESS_KEY = "put your key"
AWS_SECRET_KEY = "place ur key"
AWS_REGION = "us-east-1"  # e.g., us-east-1

# S3 bucket and file details
BUCKET_NAME = "si-global-elb-logs-demo"
S3_FOLDER = ""  # Folder path in S3 (or leave empty for root)
LOCAL_DEST = "./local-logs/"  # Local destination folder

# Create an S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# Ensure the local destination directory exists
os.makedirs(LOCAL_DEST, exist_ok=True)

# Fetch and download all files in the S3 folder
def download_logs_from_s3():
    try:
        # List objects in the S3 folder
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=S3_FOLDER)

        if 'Contents' in response:
            for obj in response['Contents']:
                s3_key = obj['Key']
                local_file_path = os.path.join(LOCAL_DEST, os.path.basename(s3_key))

                # Download the file
                print(f"Downloading {s3_key} to {local_file_path}")
                s3_client.download_file(BUCKET_NAME, s3_key, local_file_path)
        else:
            print(f"No files found in S3 bucket '{BUCKET_NAME}' under folder '{S3_FOLDER}'")
    except Exception as e:
        print(f"Error: {e}")

# Run the script
download_logs_from_s3()
