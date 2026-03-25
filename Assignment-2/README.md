# Assignment On Serverless Architecture and Cloud Automation

# ✅ Assignment 2: 

    Automated S3 Bucket Cleanup Using AWS Lambda and Boto3
# Objective

    Automate the deletion of files older than 30 days from an S3 bucket using AWS Lambda and Boto3.

# Overview Of Task
    This solution automatically:
        1-Scans an S3 bucket
        2-Identifies files older than 30 days
        3-Deletes old files
        4-Logs actions for tracking

# Architecture
                Amazon S3 Bucket
                        ↓
                AWS Lambda Function
                        ↓
                Boto3 (Python SDK)
                        ↓
                Deletes files older than 30 days

# Prerequisites
    AWS account
    S3 bucket created    
    Files uploaded
    IAM permissions
    Step 1: Create S3 Bucket
        Go to S3 → Create bucket

        Bucket name    :    santosh-cleanup-bucket
        Upload test files:
            Old files (>30 days)
        Recent files
<img width="1320" height="631" alt="as2-s3 bucket policy" src="https://github.com/user-attachments/assets/77084a52-3a29-41d6-92a2-46ccdcbd17b9" />

    Step 2: Create IAM Role for Lambda
        Go to IAM → Roles → Create role
        Select: Lambda
            Attach policy:
            AmazonS3FullAccess
    

    Step 3: Create Lambda Function
        Go to Lambda → Create function
        Configure:
            Setting	        Value
            Name        	S3-Cleanup
            Runtime        	Python 3.x
            Role	        IAM role created
<img width="1306" height="617" alt="lambda role" src="https://github.com/user-attachments/assets/6e1b4ae2-c2de-4710-ad32-a69339f3077c" />
 
    Step 4: Add Lambda Code
                
                import boto3
                from datetime import datetime, timezone, timedelta
                
                s3 = boto3.client('s3')
                
                BUCKET_NAME = 'santosh-cleanup-bucket'
                DAYS = 30
                
                def lambda_handler(event, context):
                
                    print("Starting S3 cleanup...")
                
                    cutoff_date = datetime.now(timezone.utc) - timedelta(days=DAYS)
                
                    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
                
                    if 'Contents' not in response:
                        print("Bucket is empty")
                        return
                
                    for obj in response['Contents']:
                        file_name = obj['Key']
                        last_modified = obj['LastModified']
                
                        if last_modified < cutoff_date:
                            print(f"Deleting: {file_name}")
                
                            s3.delete_object(
                                Bucket=BUCKET_NAME,
                                Key=file_name
                            )
                        else:
                            print(f"Keeping: {file_name}")
                            
    Step 5: Manual Testing
        Go to Lambda → Test
        Use test event:
        Run function
<img width="1304" height="659" alt="as2-s3 bucket del completed" src="https://github.com/user-attachments/assets/9c837780-4212-4659-bb95-1a76afcbe905" />

    Step 6: Verify Results
        Go to S3 bucket

        Confirm:
        Old files → deleted
        New files → remain

<img width="1317" height="669" alt="as2-other files" src="https://github.com/user-attachments/assets/a5c3fbae-a63c-4542-8644-e80faf794021" />


# Recommended IAM Policy

            {
              "Version": "2012-10-17",
              "Statement": [
                {
                  "Effect": "Allow",
                  "Action": ["s3:ListBucket"],
                  "Resource": "arn:aws:s3:::santosh-cleanup-bucket"
                },
                {
                  "Effect": "Allow",
                  "Action": ["s3:GetObject", "s3:DeleteObject"],
                  "Resource": "arn:aws:s3:::santosh-cleanup-bucket/*"
                }
              ]
            }

# IT Can Be Run Automate Cleanup Daily 
<img width="1313" height="674" alt="as2-s3 log" src="https://github.com/user-attachments/assets/e41bc88d-8539-4ff3-9372-f0202fea71dc" />
<img width="1304" height="659" alt="as2-s3 bucket del completed" src="https://github.com/user-attachments/assets/0375d38c-93cd-4ca9-a7aa-04b799588558" />

# Learning Outcomes
    AWS Lambda automation
    S3 object management
    Boto3 usage
    IAM role configuration

    Automated S3 bucket cleanup using AWS Lambda and Boto3 to delete objects older than 30 days, improving storage management      and cost efficiency.

# Conclusion
    This solution helps:
    Maintain clean storage
    Reduce unnecessary costs
    Automate routine maintenance tasks


👨‍💻 Author

Santosh Kumar Sharma (12394), Batch-15

DevOps & Cloud Enthusiast
