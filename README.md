# Assignment 1:
## AWS Lambda Function Automation for EC2 Instance Start/Stop
Project Overview

This project demonstrates how to automatically start and stop Amazon EC2 instances based on tags using an AWS Lambda function written in Python with the Boto3 SDK.

The automation helps organizations optimize cloud costs and simplify infrastructure management by automatically managing EC2 instance states based on predefined tags.

Objective

Create a serverless automation system that:

Stops EC2 instances tagged Auto-Stop

Starts EC2 instances tagged Auto-Start

Logs actions to CloudWatch for monitoring and auditing

Architecture
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

# Technologies Used

AWS Lambda

Amazon EC2

Python

Boto3 (AWS SDK for Python)

AWS IAM

Amazon CloudWatch

# Prerequisites

Before implementing this project, ensure you have:

An AWS account

Permission to create Lambda functions and EC2 instances

Basic knowledge of Python

Basic understanding of AWS services

# Implementation Steps
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

How the Automation Works

The Lambda function performs the following operations:

Connects to EC2 using Boto3.

Searches for instances tagged Action=Auto-Stop that are currently running.

Stops those instances.

Searches for instances tagged Action=Auto-Start that are currently stopped.

Starts those instances.

Logs actions in CloudWatch Logs.

# Testing the Solution

Open the Lambda console.

Click Test.

Create a test event.

Example event:


Run the test.

Verify Results

Open the EC2 dashboard and verify instance states.

Instance	Expected Result
auto-stop-instance	Stopped
auto-start-instance	Running
Logging and Monitoring

Logs are automatically stored in CloudWatch.

Location:

CloudWatch → Log Groups → /aws/lambda/EC2-Auto-Manager

Example log output:

Stopping instances: ['i-1234567890']
Starting instances: ['i-0987654321']

# Optional Automation with Scheduler

You can automate execution using scheduled triggers.

Example schedule:

Start instances: 8:00 AM
Stop instances: 7:00 PM

This helps automatically manage development environments and reduce costs.

# Security Best Practices

For production environments:

Use least privilege IAM policies

Avoid full EC2 access permissions

Enable CloudTrail auditing

Restrict access to specific instances if possible

# Cost Optimization Benefits

This automation helps:

Stop unused development instances

Reduce EC2 operational costs

Automate infrastructure management

Typical savings:

30% – 60% EC2 cost reduction
Learning Outcomes

By completing this project, you learn:

Serverless automation with AWS Lambda

Managing AWS resources using Boto3

EC2 tagging strategies

IAM role configuration

Monitoring using CloudWatch

Cloud cost optimization techniques

# Future Enhancements

Possible improvements:

Add multi-region support

Add Slack or email notifications

Manage additional services (RDS, ECS)

Implement infrastructure using Terraform

Create automated dashboards for monitoring

👨‍💻 Author
Santosh Kumar Sharma
Cloud / DevOps Automation Project
