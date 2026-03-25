# Assignment On Serverless Architecture and Cloud Automation

# ✅ Assignment 1:

    AWS Lambda Automation for EC2 Instance Start/Stop
# Project Overview
        This project demonstrates how to automatically start and stop Amazon EC2 instances based on tags using an AWS Lambda function written in Python with the             Boto3 SDK.
        The automation helps organizations optimize cloud costs and simplify infrastructure management by automatically managing EC2 instance states based on                predefined tags.

# Objective
    Create a serverless automation system that:
    Stops EC2 instances tagged Auto-Stop, Starts EC2 instances tagged Auto-Start
    Logs actions to CloudWatch for monitoring and auditing

# Architecture
    Manual Trigger / EventBridge Schedule
              │
              ▼
         AWS Lambda
      (Python + Boto3)
              │
              ▼
              │
              ▼
     Detect Instance Tags
       │             │
       ▼             ▼
     Stop Instances   Start Instances
       │             │
       └──────► CloudWatch Logs

# Technologies Used
      AWS Lambda
      Amazon EC2
      Python
      Boto3 (AWS SDK for Python)
      AWS IAM
      Amazon CloudWatch

# Implementation Steps
    Step 1: Create EC2 Instances
      Create two EC2 instances.
    Instance 1
      Name:auto-stop
    # Tags:
      Name: Action
      Value: Auto-Stop
    Instance 2
      Name:auto-start
    # Tags:
      Name: Action
      Value: Auto-Start
    Instance type : t4g.micro
<img width="1311" height="709" alt="ec2 instance 2" src="https://github.com/user-attachments/assets/ec64101b-9022-4612-88a2-68f10bce3e60" />

    Step 2: Create IAM Role for Lambda
      Create an IAM role with permissions to manage EC2 instances.
<img width="1306" height="617" alt="lambda role" src="https://github.com/user-attachments/assets/66db46e9-7330-4f4b-9b28-8c330c8bbf74" />

    Recommended permissions:
      AmazonEC2FullAccess
      CloudWatchFullAccess
    Attach the role to the Lambda function.
    Example role name:my-lambda-role

    Step 3: Create Lambda Function
      Configuration:
        Function Name : Auto-Manager
        Runtime       : Python 3.x
        Execution Role: my-lambda-role

# Deploy the Python script that performs EC2 automation.
        import boto3
        
        def lambda_handler(event, context):
            
            ec2 = boto3.client('ec2')
            
            # Find Auto-Stop instances
            stop_instances = ec2.describe_instances(
                Filters=[
                    {'Name': 'tag:Action', 'Values': ['Auto-Stop']},
                    {'Name': 'instance-state-name', 'Values': ['running']}
                ]
            )
            
            stop_ids = []
            
            for reservation in stop_instances['Reservations']:
                for instance in reservation['Instances']:
                    stop_ids.append(instance['InstanceId'])
            
            if stop_ids:
                ec2.stop_instances(InstanceIds=stop_ids)
                print("Stopped instances:", stop_ids)
            
            
            # Find Auto-Start instances
            start_instances = ec2.describe_instances(
                Filters=[
                    {'Name': 'tag:Action', 'Values': ['Auto-Start']},
                    {'Name': 'instance-state-name', 'Values': ['stopped']}
                ]
            )
            
            start_ids = []
            
            for reservation in start_instances['Reservations']:
                for instance in reservation['Instances']:
                    start_ids.append(instance['InstanceId'])
            
            if start_ids:
                ec2.start_instances(InstanceIds=start_ids)
                print("Started instances:", start_ids)
            
            
            return {
                'statusCode': 200,
                'body': 'EC2 automation completed'
            }

#  How the Automation Works
    
    The Lambda function performs the following operations:
    Connects to EC2 using Boto3.
    
    Searches for instances tagged Action=Auto-Stop that are currently running.
    Stops those instances.

    Searches for instances tagged Action=Auto-Start that are currently stopped.
    Starts those instances.

# Logs actions in CloudWatch Logs.
    Testing the Solution
    1-Open the Lambda console.
    2-Click Test.
    3-Create a test event.
    4-Run the test.
<img width="1317" height="719" alt="auto-mation-status" src="https://github.com/user-attachments/assets/0912b1ac-ce4b-44f2-b635-8edd1d577ce9" />

# Results Verify 
    Open the EC2 dashboard and verify instance states.
    Instance	        Expected Result
    auto-stop-instance	Stopped
    auto-start-instance	Running

# Logging and Monitoring
    Logs are automatically stored in CloudWatch.
    Location:
        CloudWatch → Log Groups → /aws/lambda/Auto-Manager
<img width="1314" height="720" alt="log 11" src="https://github.com/user-attachments/assets/9e35763b-316c-4b9a-a18d-57809bcaab60" />

    log output:
        Stopping instances: ['i-04c3e18ac5480ab34']
        Starting instances: ['i-001dddadfbeb1ff35']

# Learning Outcomes
    
    By completing this project, I learnt.
        1-Serverless automation with AWS Lambda
        2-Managing AWS resources using Boto3
        3-EC2 tagging strategies
        4-IAM role configuration
        5-Monitoring using CloudWatch
        
👨‍💻 Author

Santosh Kumar Sharma (12394), Batch-15

DevOps & Cloud Enthusiast
