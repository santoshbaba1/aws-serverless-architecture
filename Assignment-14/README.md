# Assignment On Serverless Architecture and Cloud Automation

# ✅ Assignment 14:

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
                "instance-id": "i-04c329342de2c4491",
                "state": "running"
              }
            }

# Expected Output
    Will receive an email:
    Subject: EC2 State Change Alert
    EC2 Instance State Change Alert
<img width="1360" height="765" alt="email notification send" src="https://github.com/user-attachments/assets/2dc55ab3-a64c-4f8e-bf51-fd1ca7d92a1c" />

    Instance ID: i-0261684ad88a59637
    New State: running
<img width="1362" height="767" alt="change state notigication" src="https://github.com/user-attachments/assets/4c9646db-3417-4366-833a-e2d60c98d667" />
<img width="1354" height="677" alt="ec2-state email alert" src="https://github.com/user-attachments/assets/26f4b787-512a-442a-837f-26d936fc87af" />

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


👨‍💻 Author

Santosh Kumar Sharma (12394), Batch-15

DevOps & Cloud Enthusiast
