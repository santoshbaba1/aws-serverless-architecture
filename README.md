# Assignment 1:
AWS Lambda Automation for EC2 Instance Start/Stop
📌 Project Overview

This project demonstrates how to automatically start and stop Amazon EC2 instances based on tags using an AWS Lambda function written in Python with the Boto3 SDK.

The automation helps organizations optimize cloud costs and simplify infrastructure management by automatically managing EC2 instance states based on predefined tags.

🎯 Objective

Create a serverless automation system that:

Stops EC2 instances tagged Auto-Stop

Starts EC2 instances tagged Auto-Start

Logs actions to CloudWatch for monitoring and auditing

🏗️ Architecture
Manual Trigger / EventBridge Schedule
              │
              ▼
         AWS Lambda
      (Python + Boto3)
              │
              ▼
        EC2 Describe API
              │
              ▼
     Detect Instance Tags
       │             │
       ▼             ▼
 Stop Instances   Start Instances
       │             │
       └──────► CloudWatch Logs
🧰 Technologies Used

AWS Lambda

Amazon EC2

Python

Boto3 (AWS SDK for Python)

AWS IAM

Amazon CloudWatch

⚙️ Prerequisites

Before implementing this project, ensure you have:

An AWS account

Permission to create Lambda functions and EC2 instances

Basic knowledge of Python

Basic understanding of AWS services

🚀 Implementation Steps
Step 1: Create EC2 Instances

Create two EC2 instances.

Instance 1

Name:

auto-stop-instance

Tags:

Key: Action
Value: Auto-Stop
Instance 2

Name:

auto-start-instance

Tags:

Key: Action
Value: Auto-Start

Instance type can be:

t2.micro
Step 2: Create IAM Role for Lambda

Create an IAM role with permissions to manage EC2 instances.

Recommended permissions:

ec2:DescribeInstances
ec2:StartInstances
ec2:StopInstances

Attach the role to the Lambda function.

Example role name:

LambdaEC2ManagerRole
Step 3: Create Lambda Function

Configuration:

Function Name: EC2-Auto-Manager
Runtime: Python 3.x
Execution Role: LambdaEC2ManagerRole

Deploy the Python script that performs EC2 automation.

🧠 How the Automation Works

The Lambda function performs the following operations:

Connects to EC2 using Boto3.

Searches for instances tagged Action=Auto-Stop that are currently running.

Stops those instances.

Searches for instances tagged Action=Auto-Start that are currently stopped.

Starts those instances.

Logs actions in CloudWatch Logs.

🧪 Testing the Solution

Open the Lambda console.

Click Test.

Create a test event.

Example event:

{}

Run the test.

🔍 Verify Results

Open the EC2 dashboard and verify instance states.

Instance	Expected Result
auto-stop-instance	Stopped
auto-start-instance	Running
📊 Logging and Monitoring

Logs are automatically stored in CloudWatch.

Location:

CloudWatch → Log Groups → /aws/lambda/EC2-Auto-Manager

Example log output:

Stopping instances: ['i-1234567890']
Starting instances: ['i-0987654321']
⏰ Optional Automation with Scheduler

You can automate execution using scheduled triggers.

Example schedule:

Start instances: 8:00 AM
Stop instances: 7:00 PM

This helps automatically manage development environments and reduce costs.

🔐 Security Best Practices

For production environments:

Use least privilege IAM policies

Avoid full EC2 access permissions

Enable CloudTrail auditing

Restrict access to specific instances if possible

💰 Cost Optimization Benefits

This automation helps:

Stop unused development instances

Reduce EC2 operational costs

Automate infrastructure management

Typical savings:

30% – 60% EC2 cost reduction
🎓 Learning Outcomes

By completing this project, you learn:

Serverless automation with AWS Lambda

Managing AWS resources using Boto3

EC2 tagging strategies

IAM role configuration

Monitoring using CloudWatch

Cloud cost optimization techniques

📌 Future Enhancements

Possible improvements:

Add multi-region support

Add Slack or email notifications

Manage additional services (RDS, ECS)

Implement infrastructure using Terraform

Create automated dashboards for monitoring


**************************************************************
# Assignment 5:
Auto-Tagging EC2 Instances on Launch using AWS Lambda & Boto3
📌 Project Overview

This project demonstrates how to automatically tag EC2 instances at launch using a serverless approach.

Whenever a new EC2 instance is launched and enters the running state, a Lambda function is triggered to:

Add a LaunchDate tag (current date)

Add a custom tag (e.g., Environment = Dev)

This helps in:

Resource tracking

Cost management

Governance and compliance

🎯 Objective

Automatically tag EC2 instances with:

LaunchDate = current date

Environment = Dev (custom tag)

🏗️ Architecture
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
🧰 Technologies Used

AWS Lambda

Amazon EC2

Amazon EventBridge

Boto3 (Python SDK)

AWS IAM

Amazon CloudWatch (logs)

⚙️ Prerequisites

Before starting, ensure:

AWS account access

Permission to create EC2, Lambda, IAM roles

Basic understanding of AWS services

🚀 Deployment Steps
Step 1: EC2 Setup

Go to EC2 Dashboard

Click Launch Instance

Configure:

Name: auto-tag-test
Instance Type: t2.micro
AMI: Amazon Linux

Launch instance

Step 2: Create IAM Role for Lambda

Go to IAM → Roles → Create Role

Select:

Trusted Entity: Lambda

Attach policy:

AmazonEC2FullAccess

Role name:

Lambda-EC2-AutoTag-Role

Create role

Step 3: Create Lambda Function

Go to Lambda → Create Function

Choose:

Function Name: EC2-Auto-Tag
Runtime: Python 3.x
Execution Role: Lambda-EC2-AutoTag-Role

Click Create Function

Step 4: Add Lambda Code

Replace default code with:

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
        {'Key': 'Environment', 'Value': 'Dev'}
    ]

    # Apply tags
    ec2.create_tags(
        Resources=[instance_id],
        Tags=tags
    )

    print(f"Instance {instance_id} tagged successfully")

Click Deploy

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

Generated JSON:

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

🧪 Testing
Method 1 (Recommended)

Launch a new EC2 instance

Wait 20–30 seconds

Method 2 (Manual Test Event)

Use this test event:

{
 "detail": {
   "instance-id": "i-1234567890",
   "state": "running"
 }
}
🔍 Verification

Go to:

EC2 → Instances → Select Instance → Tags

Expected output:

Key	Value
LaunchDate	2026-03-17
Environment	Dev
📊 Logs & Monitoring

Go to:

CloudWatch → Log Groups → /aws/lambda/EC2-Auto-Tag

Example logs:

Received event {...}
Instance i-123456 tagged successfully
🔐 Security Best Practices

Avoid using full EC2 access in production

Use least privilege policy:

ec2:CreateTags
ec2:DescribeInstances
💰 Benefits

Automatic tagging (no manual work)

Improved cost tracking

Better governance

Standardized resource management

🎓 Learning Outcomes

Event-driven architecture

Lambda automation

EC2 tagging strategy

IAM role configuration

CloudWatch logging

🚀 Future Enhancements

Add Owner and CostCenter tags

Multi-region support

Slack / Email notifications

Terraform automation

Enforce mandatory tagging policies

📌 Conclusion

This project demonstrates a real-world DevOps automation pattern used in enterprises to ensure all resources are properly tagged for cost tracking, compliance, and operational efficiency.

👨‍💻 Author

Cloud / DevOps Automation Project
