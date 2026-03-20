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
        
**************************************************************
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
<img width="1320" height="631" alt="as2-s3 bucket policy" src="https://github.com/user-attachments/assets/d79d8dde-e2dc-4f73-b4a0-f9f308a4081d" />

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

**************************************************************
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
    This project demonstrates a real-world DevOps automation pattern used in enterprises to ensure all resources are properly      tagged for cost tracking, compliance,       and operational efficiency.
************************************************************************************
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
                "instance-id": "i-1234567890",
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
*******************************************************************************************************************************************************

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
            
            sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard

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

    Step 4: Create IAM Role for Lambda
        Attach these policies:
        AmazonEC2ReadOnlyAccess
        CloudWatchReadOnlyAccess
        AmazonSNSFullAccess

    Step 5: Create Lambda Function
        Configuration
        Name        : EC2-Disk-Monitor
        Runtime     : Python 3.x
        Role        : IAM role created above

# Lambda Code

                import boto3
                from datetime import datetime, timedelta
                
                cloudwatch = boto3.client('cloudwatch')
                sns = boto3.client('sns')
                
                SNS_TOPIC_ARN = 'YOUR_SNS_TOPIC_ARN'
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

        Real Test (Simulate High Disk Usage)
        ## fallocate -l 6G testfile
        Wait 2–5 minutes → Trigger Lambda

# Expected Output
    Email alert:
    # Subject: EC2 Disk Alert
    Message: Disk usage is 90%

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

***********************************************************************************************************************************************
# ✅ Assignment 17:

    Restore EC2 Instance from Snapshot
    This is a classic disaster recovery automation used in DevOps.
        use:
            Amazon EC2
            AWS Lambda
            Amazon EventBridge
            Boto3

# Objective
    Automatically:

        Find latest snapshot
                ↓
        Create volume
                ↓
        Launch new EC2 instance

# Architecture
        EBS Snapshots
              │
              ▼
        Lambda Function
              │
              ▼
        New EC2 Instance Created
              │
              ▼
        (Optional) EventBridge Trigger

# Deployment
## Prerequisite
    Must have:
    ✔ Existing EC2 instance
    ✔ Snapshots created 
    Check:
        EC2 → Elastic Block Store → Snapshots

# Create IAM Role for Lambda
    Go to:
    IAM → Roles → Create Role
        Attach policies:
        AmazonEC2FullAccess
    Role:
        Name: Lambda-EC2-Restore-Role
<img width="1318" height="675" alt="as17-iam role" src="https://github.com/user-attachments/assets/c67f4bf3-eb71-4842-9ee1-5b9b70adfdbb" />

# Create Lambda Function
    Go to:
    Lambda → Create Function
    Settings:
    Field	        Value
    Name	        EC2-Restore-From-Snapshot
    Runtime	        Python 3.x
    Role	        Lambda-EC2-Restore-Role
<img width="1316" height="659" alt="as17-lambda-funj" src="https://github.com/user-attachments/assets/ab6a6cd0-02d4-449c-89a9-789015042168" />

# Lambda Code (Core Logic)
            import boto3
            
            ec2 = boto3.client('ec2')
            
            def lambda_handler(event, context):
            
                # Get latest AMI
                images = ec2.describe_images(Owners=['self'])['Images']
            
                latest_image = sorted(
                    images,
                    key=lambda x: x['CreationDate'],
                    reverse=True
                )[0]
            
                image_id = latest_image['ImageId']
            
                print(f"Latest AMI: {image_id}")
            
                # Launch instance
                instance = ec2.run_instances(
                ImageId='ami-0d9ee65a2a86e323b',
                InstanceType='t4g.micro',
                MinCount=1,
                MaxCount=1,
            
                #  REQUIRED FIX
                NetworkInterfaces=[
                    {
                        'SubnetId': 'subnet-05fd5e23acdd5b9e8',
                        'DeviceIndex': 0,
                        'AssociatePublicIpAddress': True,
                        'Groups': ['sg-0328dc2b2e1069b9b']
                    }
                    ]
                )
            
                instance_id = instance['Instances'][0]['InstanceId']
            
                print(f"Instance created: {instance_id}")

# Testing
    Manual Test
        Click:
        Lambda → Test
<img width="1310" height="669" alt="as17-ec2-restore" src="https://github.com/user-attachments/assets/0b178519-b4b6-4098-95fc-650b89a53d65" />
<img width="1310" height="669" alt="as17-ec2-restore-1" src="https://github.com/user-attachments/assets/6e67f72c-136b-45c5-80b0-ece7beb2a2cc" />

# Logs:

    Latest snapshot: snap-12345
    New EC2 instance launched: i-12345
<img width="1316" height="667" alt="as17-launch-ec2-inst" src="https://github.com/user-attachments/assets/fcd7db9f-17e0-4984-a733-6bd7b4cefed5" />

<img width="1314" height="663" alt="as17-log" src="https://github.com/user-attachments/assets/9e188509-99dc-4340-9a63-033640bb75c7" />

# Real Use Cases
    Disaster recovery
    Backup restore
    Auto failover
    Testing environments

# Final Flow
    Snapshot → EC2 Instance

# What,I Learnt
    Snapshot vs AMI difference
    Lambda automation
    EC2 provisioning via Boto3
    Disaster recovery design

***********************************************************************************************************************************************
# ✅ Assignment 19: Load Balancer Health Checker using AWS Lambda

# Overview

    This project implements a serverless monitoring solution using AWS services to automatically check the health of instances registered behind an Elastic Load         Balancer (ELB).
    If any instance becomes unhealthy, the system sends an alert notification using Amazon SNS.

# Objective

        1-Monitor the health of instances behind an ELB
        2-Detect unhealthy instances automatically
        3-Send notifications via SNS
        4-Run checks every 10 minutes using scheduled events

# Architecture
           
            CloudWatch (EventBridge Rule - 10 min)
                        ↓
                    AWS Lambda
                        ↓
               ELB Target Group Health Check
                        ↓
                 If Unhealthy Found
                        ↓
                    Amazon SNS
                        ↓
                    Email Alert

# Services Used
        
        AWS Lambda
        Elastic Load Balancing (ALB)
        Amazon SNS
        Amazon CloudWatch (EventBridge)
        IAM (Roles & Policies)
        Boto3 (Python SDK)

# Prerequisites
        AWS Account
        Existing Application Load Balancer (ALB)
        Target Group with registered EC2 instances
        Verified email for SNS subscription

# Setup Instructions
    
    Step 1: Create SNS Topic
            Go to SNS Dashboard
            Create a topic: Standard
            Name: elb-health-alerts
            Create a subscription:
            Protocol: Email
            Endpoint: santoshxxxxx@gmail.com
            Confirm subscription via email

    Step 2: Create IAM Role for Lambda
            Attach the following policies:
                ElasticLoadBalancingReadOnly
                AmazonSNSFullAccess
                CloudWatchFullAccess
            Role Name:
                Lambda-ELB-Health-Checker-Role
                
    Step 3: Create Lambda Function
            Name            : elb-health-checker
            Runtime         : Python 3.x
            Execution Role  : Lambda-ELB-Health-Checker-Role

    Step 4: Lambda Function Code
                    
                    import boto3
                    
                    def lambda_handler(event, context):
                        elbv2 = boto3.client('elbv2')
                        sns = boto3.client('sns')
                        
                        TARGET_GROUP_ARN = "arn:aws:elasticloadbalancing:ap-south-1:251478238405:targetgroup/elb-sns-tgt/3470af8b7d587097"
                        SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:251478238405:elb-health-alerts"
                        
                        response = elbv2.describe_target_health(
                            TargetGroupArn=TARGET_GROUP_ARN
                        )
                        
                        unhealthy_instances = []
                        
                        for target in response['TargetHealthDescriptions']:
                            instance_id = target['Target']['Id']
                            state = target['TargetHealth']['State']
                            
                            if state != 'healthy':
                                unhealthy_instances.append({
                                    "InstanceId": instance_id,
                                    "State": state
                                })
                        
                        if unhealthy_instances:
                            message = "Unhealthy Instances Detected:\n"
                            
                            for inst in unhealthy_instances:
                                message += f"Instance: {inst['InstanceId']} | State: {inst['State']}\n"
                            
                            sns.publish(
                                TopicArn=SNS_TOPIC_ARN,
                                Subject="ALB Health Alert",
                                Message=message
                            )
                            
                            print(message)
                        else:
                            print("All instances are healthy")
                        
                        return {
                            'statusCode': 200,
                            'body': unhealthy_instances
                        }
    
    Step 5: Configure Environment Variables
            Instead of hardcoding values:
            TARGET_GROUP_ARN     : arn:aws:elasticloadbalancing:ap-south-1:251478238405:targetgroup/elb-sns-tgt/3470af8b7d587097
            SNS_TOPIC_ARN        : arn:aws:sns:ap-south-1:251478238405:elb-health-alerts

    Step 6: Test the Lambda Function
            Deploy the function
            Create a test event
            Run the test
            Check logs in CloudWatch

    Step 7: Setup Scheduled Trigger
            Go to CloudWatch → EventBridge Rules

            Create rule:
                Type          : Schedule
                Expression    : rate(10 minutes)
                Target        : Lambda function (elb-health-checker)

# Output
    ✔ Healthy State
    All instances are healthy
    ❌ Unhealthy State
    Unhealthy Instances Detected:
    Instance: i-1234567890 | State: unhealthy

    📩 Email notification will also be sent

# Security Considerations
    Follow least privilege principle for IAM roles
    Avoid using full access policies in production
    Store ARNs in environment variables or AWS Secrets Manager

# Key Learnings
    1-Serverless monitoring using Lambda
    2-AWS ELB health check automation
    3-Event-driven architecture using CloudWatch
    4-Alerting via SNS
    5-Boto3 integration with AWS services

# Conclusion

    This project demonstrates a real-world DevOps monitoring solution using AWS services. It ensures high availability by proactively detecting unhealthy instances      and notifying stakeholders immediately.

👨‍💻 Author

Santosh Kumar Sharma (12394), Batch-15

DevOps & Cloud Enthusiast
