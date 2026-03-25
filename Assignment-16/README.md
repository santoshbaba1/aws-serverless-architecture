# Assignment On Serverless Architecture and Cloud Automation

# ✅ Assignment 16: 
    
    Automated SNS Alerts for EC2 Disk Space Utilization
# Objective
    Build an automated monitoring system that:
    Checks EC2 disk usage
    Triggers alert if usage exceeds 85%
    Sends notification via SNS
    Runs automatically every day

# Architecture
        EC2 Instance
           ↓
        CloudWatch Agent (collect disk metrics)
           ↓
        CloudWatch Metrics (CWAgent)
           ↓
        Lambda Function (evaluate usage)
           ↓
        SNS Topic (send alert)
           ↓
        EventBridge (daily trigger)

# Deployments /Prerequisites
    EC2 instance (Ubuntu 24 / ARM64)
    AWS CLI / Console access
    Email ID for alerts

    Step 1: Install CloudWatch Agent on EC2
        Install Agent
        wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/arm64/latest/amazon-cloudwatch-agent.deb
        sudo dpkg -i amazon-cloudwatch-agent.deb
        Attach IAM Role to EC2

        Attach policy:
            CloudWatchAgentServerPolicy
            Configure Agent
<img width="1316" height="675" alt="as16-cw-log2" src="https://github.com/user-attachments/assets/5a4b2a36-ae25-41e2-b1c3-f2eecdec5966" />

            sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
<img width="1317" height="674" alt="as-16 cwagent" src="https://github.com/user-attachments/assets/f462399d-445d-43e1-b27d-3b4f735b84ca" />   
        Choose:
            Metrics collection → YES
            Disk metrics → YES

            Mount path → /
            Start Agent
                sudo systemctl start amazon-cloudwatch-agent
                sudo systemctl enable amazon-cloudwatch-agent
                
    Step 2: Verify Metrics
        Go to:
        CloudWatch → Metrics → All Metrics → CWAgent
        Check metric:

        disk_used_percent

    Step 3: Create SNS Topic
        Open SNS → Create Topic
        Name: EC2-Disk-Alert
        Create Subscription:
        Protocol: Email
        Endpoint: santoshxxxx@gmail.com
        Confirm subscription via email
<img width="1365" height="669" alt="as16-email-alert-2" src="https://github.com/user-attachments/assets/f5704602-e31b-4570-b25e-91cfbe8c7b0c" />
<img width="1312" height="620" alt="as16-subctiprtion" src="https://github.com/user-attachments/assets/0c8e7a7f-3eae-4084-a054-0cd2dc77fe47" />

    Step 4: Create IAM Role for Lambda
        Attach these policies:
        AmazonEC2ReadOnlyAccess
        CloudWatchReadOnlyAccess
        AmazonSNSFullAccess
<img width="1310" height="664" alt="as16-iam-disk role" src="https://github.com/user-attachments/assets/710da6e8-0112-4916-ad4d-47fa9215c841" />

    Step 5: Create Lambda Function
        Configuration
        Name        : EC2-Disk-Monitor
        Runtime     : Python 3.x
        Role        : IAM role created above
<img width="1315" height="672" alt="as16-inst-role ec2" src="https://github.com/user-attachments/assets/24626dad-9099-43db-af53-621f3718514c" />
<img width="1321" height="676" alt="as16-lamda-fun" src="https://github.com/user-attachments/assets/8a680e5a-a5ae-4ac1-b17f-d0b250540203" />

# Lambda Code

                import boto3
                from datetime import datetime, timedelta
                
                cloudwatch = boto3.client('cloudwatch')
                sns = boto3.client('sns')
                
                SNS_TOPIC_ARN = 'arn:aws:sns:ap-south-1:251478238405:ec2-state-alerts'
                THRESHOLD = 85
                
                def lambda_handler(event, context):
                
                    response = cloudwatch.get_metric_statistics(
                        Namespace='CWAgent',
                        MetricName='disk_used_percent',
                        Dimensions=[
                            {'Name': 'InstanceId', 'Value': 'YOUR_INSTANCE_ID'},
                            {'Name': 'path', 'Value': '/'},
                            {'Name': 'device', 'Value': 'nvme0n1p1'}
                        ],
                        StartTime=datetime.utcnow() - timedelta(minutes=10),
                        EndTime=datetime.utcnow(),
                        Period=300,
                        Statistics=['Average']
                    )
                
                    datapoints = response['Datapoints']
                
                    if not datapoints:
                        print("No data found")
                        return
                
                    latest = sorted(datapoints, key=lambda x: x['Timestamp'])[-1]
                    usage = latest['Average']
                
                    print(f"Disk usage: {usage}%")
                
                    if usage > THRESHOLD:
                        message = f"⚠️ EC2 Disk usage is {usage}%"
                
                        sns.publish(
                            TopicArn=SNS_TOPIC_ARN,
                            Subject="EC2 Disk Alert",
                            Message=message
                        )
                
                        print("Alert sent")
                        
    Step 6: Create EventBridge Rule (Daily Trigger)
        Go to EventBridge → Rules → Create Rule

    Step 7: Testing
        Manual Test
        Run Lambda with:
<img width="1362" height="673" alt="as16-email-alert" src="https://github.com/user-attachments/assets/79b792ab-f326-4f10-8468-dd31f68e1785" />

        Real Test (Simulate High Disk Usage)
        ## fallocate -l 6G testfile
        Wait 2–5 minutes → Trigger Lambda

# Expected Output
    Email alert:
    # Subject: EC2 Disk Alert
    Message: Disk usage is 90%
<img width="1364" height="306" alt="as16-subctiprtion email confirm" src="https://github.com/user-attachments/assets/23a07a49-4e48-442a-ad5f-944d8a2cb751" />
<img width="1365" height="675" alt="as16-subctiprtion email" src="https://github.com/user-attachments/assets/331c94d2-a1b5-4536-be09-0ba333ff12f5" />

# Best Practices
    Avoid hardcoding instance ID (use dynamic discovery)
    Use least privilege IAM roles
    Monitor multiple instances (advanced)
    Use CloudWatch Alarms as alternative

# Learning Outcome
    EC2 monitoring using CloudWatch Agent
    Custom metrics handling
    Lambda automation
    SNS alert integration
    Event-driven architecture

    # Resume Line
        Implemented automated EC2 disk utilization monitoring using AWS Lambda, CloudWatch Agent, SNS, and EventBridge with threshold-based alerting.

# Conclusion
    This project provides a production-ready monitoring solution that helps:
    Prevent disk failures
    Improve system uptime
    Automate alerting and response


👨‍💻 Author

Santosh Kumar Sharma (12394), Batch-15

DevOps & Cloud Enthusiast
