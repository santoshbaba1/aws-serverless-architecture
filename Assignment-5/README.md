# Assignment On Serverless Architecture and Cloud Automation

# ✅ Assignment 5:

    ## Auto-Tagging EC2 Instances on Launch using AWS Lambda & Boto3
    Project Overview
    This project demonstrates how to automatically tag EC2 instances at launch using a serverless approach.
    Whenever a new EC2 instance is launched and enters the running state, a Lambda function is triggered to:

    Add a LaunchDate tag (current date)
    Add a custom tag (HeroVired = DevOps-Santosh)

# Objective
    Automatically tag EC2 instances with:
    LaunchDate = current date
    HeroVired = DevOps-Santosh

# Architecture
    EC2 Instance Launch
            │
            ▼
    EventBridge Rule (State = running)
            │
            ▼
    AWS Lambda Function (Python + Boto3)
            │
            ▼
    EC2 create_tags() API
            │
            ▼
    Tags added automatically

# Technologies Used
    AWS Lambda
    Amazon EC2
    Amazon EventBridge
    Boto3 (Python SDK)
    AWS IAM
    Amazon CloudWatch (logs)

# Deployment Steps
    Step 1: EC2 Setup
        Go to EC2 Dashboard
        Click Launch Instance
        Configure:
            Name: auto-tag
            Instance Type: t4g.micro
            AMI: Ubuntu24
            Launch instance

    Step 2: Create IAM Role for Lambda
        Go to IAM → Roles → Create Role
        Select:
        Trusted Entity: Lambda
        Attach policy:
            AmazonEC2FullAccess
        Role name:
            LambdaEC2AutoTagRole
            Create role
<img width="1309" height="678" alt="lambda auto tag" src="https://github.com/user-attachments/assets/3ebb6a49-761a-410e-b7c7-f1731d6e419e" />

    Step 3: Create Lambda Function
        Go to Lambda → Create Function

        Choose:
            Function Name: EC2-Auto-Tag
            Runtime: Python 3.x
            Execution Role: LambdaEC2AutoTagRole
            Click Create Function
<img width="1318" height="670" alt="lambda auto tag 2" src="https://github.com/user-attachments/assets/2f747ce5-413e-48d7-a246-e15ea166a416" />

    Step 4: Add Lambda Code
       

            import boto3
            from datetime import datetime
            
            ec2 = boto3.client('ec2')
            
            def lambda_handler(event, context):
            
                print("Received event:", event)
            
                # Extract instance ID
                instance_id = event['detail']['instance-id']
            
                # Get current date
                today = datetime.utcnow().strftime('%Y-%m-%d')
            
                # Define tags
                tags = [
                    {'Key': 'LaunchDate', 'Value': today},
                    {'Key': 'HeroVired', 'Value': 'DevOps-Santosh'}
                ]
            
                # Apply tags
                ec2.create_tags(
                    Resources=[instance_id],
                    Tags=tags
                )
            
                print(f"Instance {instance_id} tagged successfully")

# Deploy

    Step 5: Create EventBridge Rule
        Go to EventBridge → Rules → Create Rule

        Configure:
            Rule Name: EC2-AutoTag-Rule
            Event Bus: default
            Rule Type: Event pattern
            Event Pattern Configuration
        Choose:
            Event Source: AWS services
            Service: EC2
            Event Type: EC2 Instance State-change Notification

        Add filter:

            State = running

               # Generated JSON:
                
                {
                 "source": ["aws.ec2"],
                 "detail-type": ["EC2 Instance State-change Notification"],
                 "detail": {
                   "state": ["running"]
                 }
                }
                
    Step 6: Add Target
        Target Type: AWS Service
        Service: Lambda
        Function: EC2-Auto-Tag
        Click Create Rule

# Testing
    Method 1 
        Launch a new EC2 instance
        Wait 20–30 seconds

    Method 2 
        Use this test event:
            {
             "detail": {
               "instance-id": "i-09da0c42dd0c4e222",
               "state": "running"
             }
            }
            
# Verification

    Go to:
        EC2 → Instances → Select Instance → Tags
        
        Expected output:
        Name:    	Value
        LaunchDate	2026-03-17
        HeroVired	DevOps-Santosh

<img width="1315" height="722" alt="autotag-ec2 name " src="https://github.com/user-attachments/assets/80140d65-98e9-4d0a-90e1-4ed745207046" />

# Logs & Monitoring

    Go to:
        CloudWatch → Log Groups → /aws/lambda/EC2-Auto-Tag
    logs:
<img width="1310" height="718" alt="state notific log" src="https://github.com/user-attachments/assets/8eefc986-aba8-4bc5-91e7-c48c9a38956f" />

# Learning Outcomes
   
    Event-driven architecture
    Lambda automation
    EC2 tagging strategy
    IAM role configuration
    CloudWatch logging

# Future Enhancements
    
    Email notifications

# Conclusion
    
    This project demonstrates a real-world DevOps automation pattern used in enterprises to ensure all resources are properly      tagged for cost tracking, compliance,       and operational efficiency.

👨‍💻 Author

Santosh Kumar Sharma (12394), Batch-15

DevOps & Cloud Enthusiast
