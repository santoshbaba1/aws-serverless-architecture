import boto3
from datetime import datetime

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    print("Received event:", event)

    # Get instance ID
    instance_id = event['detail']['instance-id']

    # Current date
    today = datetime.utcnow().strftime('%Y-%m-%d')

    # Tags to apply
    tags = [
        {'Key': 'LaunchDate', 'Value': today},
        {'Key': 'HeroVired', 'Value': 'DevOps-Santosh'}
    ]

    # Apply tags
    ec2.create_tags(
        Resources=[instance_id],
        Tags=tags
    )

    print(f"Successfully tagged instance {instance_id}")