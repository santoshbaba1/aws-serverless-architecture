import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    # List all buckets
    buckets = s3.list_buckets()['Buckets']
    
    unencrypted_buckets = []
    
    for bucket in buckets:
        bucket_name = bucket['Name']
        
        try:
            # Check encryption configuration
            s3.get_bucket_encryption(Bucket=bucket_name)
        
        except Exception as e:
            # If encryption not found, it throws error
            error_code = str(e)
            
            if "ServerSideEncryptionConfigurationNotFoundError" in error_code:
                print(f"❌ Bucket WITHOUT encryption: {bucket_name}")
                unencrypted_buckets.append(bucket_name)
            else:
                print(f"⚠️ Error checking bucket {bucket_name}: {error_code}")
    
    # Summary log
    print("====== SUMMARY ======")
    print(f"Total Unencrypted Buckets: {len(unencrypted_buckets)}")
    print(unencrypted_buckets)
    
    return {
        'statusCode': 200,
        'body': unencrypted_buckets
    }