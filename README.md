⚙️ Prerequisites

AWS Account
IAM permissions to create Lambda, SNS, EC2, EventBridge

# Assignment 1:
## AWS Lambda Automation for EC2 Instance Start/Stop
    Project Overview
    This project demonstrates how to automatically start and stop Amazon EC2 instances based on tags using an AWS Lambda function written in Python with the Boto3 SDK.
    The automation helps organizations optimize cloud costs and simplify infrastructure management by automatically managing EC2 instance states based on predefined tags.

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

**************************************************************
# Assignment 5:

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
               "instance-id": "i-1234567890",
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

This project demonstrates a real-world DevOps automation pattern used in enterprises to ensure all resources are properly tagged for cost tracking, compliance, and operational efficiency.
************************************************************************************
# Assignment 14:
## EC2 Instance State Monitoring using AWS Lambda, SNS & EventBridge
    Project Overview
    This project implements an event-driven monitoring system for EC2 instances.
    Whenever an EC2 instance is started or stopped, a Lambda function is triggered automatically and sends a notification via SNS.
# Objective
    Monitor EC2 instance state changes (start/stop)
    Send real-time notifications via email
    Automate infrastructure monitoring using serverless architecture

# Architecture
        EC2 Instance (Start/Stop)
                │
                ▼
        EventBridge Rule
                │
                ▼
        AWS Lambda Function
                │
                ▼
        SNS Topic
                │
                ▼
        Email Notification

# Technologies Used
    AWS Lambda
    Amazon EC2
    Amazon EventBridge
    Amazon SNS
    Boto3 (Python SDK)
    AWS IAM
    Amazon CloudWatch
<img width="1316" height="717" alt="ec2-state-config-vm" src="https://github.com/user-attachments/assets/5bfd0115-09dd-4478-aa35-4b442644d028" />

# Deployment Steps
    Step 1: Create SNS Topic
    Go to SNS → Topics → Create Topic
    Select:
    Type: Standard
    Name: ec2-state-alerts
    
    Create topic
    Create Subscription:
    Protocol: Email
    santoshxxxxxx@gmail.com
    Confirm subscription from your inbox
 <img width="1310" height="719" alt="sns config" src="https://github.com/user-attachments/assets/8d5f4fba-e91b-4f7a-aa03-9531d91b5132" />

    Step 2: Create IAM Role for Lambda
    Go to IAM → Roles → Create Role
    Select:
    Trusted Entity: Lambda
    Attach policies:
        AmazonEC2ReadOnlyAccess
        AmazonSNSFullAccess
    Role name:
        Lambda-EC2-Monitor-Role

    Step 3: Create Lambda Function
        Go to Lambda → Create Function
        Configure:
            Function Name: EC2-State-Monitor
            Runtime: Python 3.x
            Execution Role: Lambda-EC2-Monitor-Role
            Click Create Function
 
    Step 4: Add Lambda Code
                
                import boto3
                import json
                
                sns = boto3.client('sns')
                
                SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:251478238405:ec2-state-alerts"
                
                def lambda_handler(event, context):
                
                    print("Received event:", json.dumps(event))
                
                    try:
                        instance_id = event['detail']['instance-id']
                        state = event['detail']['state']
                
                        message = f"""
                EC2 Instance State Change Alert
                
                Instance ID: {instance_id}
                New State: {state}
                """
                
                        sns.publish(
                            TopicArn=SNS_TOPIC_ARN,
                            Subject="EC2 State Change Alert",
                            Message=message
                        )
                
                        print("Notification sent successfully")
                
                    except KeyError:
                        print("Invalid event format")
                
👉 Replace YOUR_SNS_TOPIC_ARN with your actual ARN

# Click Deploy

    Step 5: Create EventBridge Rule
        Go to EventBridge → Rules → Create Rule
        Basic Configuration:
        Rule Name: EC2-State-Change-Rule
        Event Bus: default
        Rule Type: Event pattern
        Event Pattern:

        Select:
            Event Source: AWS services
            Service: EC2
            Event Type: EC2 Instance State-change Notification
<img width="1320" height="723" alt="change state event config" src="https://github.com/user-attachments/assets/3286febc-22bb-4c4d-97a8-c93b363c5ffe" />

        Add filter:
            State: running, stopped
            JSON Pattern:
                    {
                      "source": ["aws.ec2"],
                      "detail-type": ["EC2 Instance State-change Notification"],
                      "detail": {
                        "state": ["running", "stopped"]
                      }
                    }

    Step 6: Attach Target
        Target Type : AWS Service
        Service     : Lambda
        Function    : EC2-State-Monitor

        Click Create Rule

# Testing
    Test Method 1
        Go to EC2 Dashboard
        Select an instance
        Click Start or Stop

    Test Method 2 (Manual Event)
        Use this test event:

            {
              "detail": {
                "instance-id": "i-1234567890",
                "state": "running"
              }
            }

# Expected Output
    Will receive an email:
    Subject: EC2 State Change Alert
    EC2 Instance State Change Alert
<img width="1360" height="765" alt="email notification send" src="https://github.com/user-attachments/assets/2dc55ab3-a64c-4f8e-bf51-fd1ca7d92a1c" />

    Instance ID: i-1234567890
    New State: running
<img width="1362" height="767" alt="change state notigication" src="https://github.com/user-attachments/assets/4c9646db-3417-4366-833a-e2d60c98d667" />

# Monitoring & Logs
    Go to:
    CloudWatch → Log Groups → /aws/lambda/EC2-State-Monitor

    Logs:
        Received event {...}
        Notification sent successfully
<img width="1353" height="767" alt="email notification" src="https://github.com/user-attachments/assets/39c2a777-e4fc-4c71-a190-4a59ac8dbd4b" />

# Security Best Practices
    Avoid using full access policies in production
    Use least privilege:
        sns:Publish
        ec2:DescribeInstances

# Benefits
    Real-time monitoring
    Automated alerting
    Improved system visibility
    Reduced manual effort

# Learning Outcomes
    Event-driven AWS architecture
    Lambda automation
    SNS notifications
    EventBridge rule configuration
    Debugging event-based systems

# Future Enhancements
    Teams notifications
    Auto-recovery actions (restart instances)
    Multi-region monitoring
    Infrastructure as Code
    CloudWatch dashboards

# Conclusion
    This project demonstrates a real-world monitoring solution widely used in DevOps environments to track infrastructure changes and respond proactively to system events.



# Author

Santosh Kumar Sharma (12394)-Batch-15

Cloud / DevOps Automation Project
