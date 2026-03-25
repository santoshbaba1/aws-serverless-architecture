# Assignment On Serverless Architecture and Cloud Automation

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
<img width="1318" height="672" alt="as19-elb active" src="https://github.com/user-attachments/assets/0efe529d-e193-4485-b9a4-6041202a3228" />

# Setup Instructions
    
    Step 1: Create SNS Topic
            Go to SNS Dashboard
            Create a topic: Standard
            Name: elb-health-alerts
            Create a subscription:
            Protocol: Email
            Endpoint: santoshxxxxx@gmail.com
            Confirm subscription via email
<img width="1365" height="668" alt="as19-subcription request" src="https://github.com/user-attachments/assets/054be9b7-1297-4c0d-b5ab-d19a8bb24fb1" />
<img width="1362" height="367" alt="as19-subcription confirm" src="https://github.com/user-attachments/assets/0ee4d253-63a9-4b3b-abe7-7f2b3969c72e" />

    Step 2: Create IAM Role for Lambda
            Attach the following policies:
                ElasticLoadBalancingReadOnly
                AmazonSNSFullAccess
                CloudWatchFullAccess
            Role Name:
                Lambda-ELB-Health-Checker-Role
<img width="1318" height="665" alt="as19-iam role" src="https://github.com/user-attachments/assets/d65177e2-4381-47bb-b090-c172418c3ba6" />
      
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
<img width="1317" height="669" alt="as19-schdule setup" src="https://github.com/user-attachments/assets/0a608202-d099-498a-a90f-44da6e5fdcc3" />
<img width="1317" height="669" alt="as19-schdule setup" src="https://github.com/user-attachments/assets/9883922d-ae74-4cfb-b4ea-8ed476125774" />

# Output
    ✔ Healthy State
    All instances are healthy
    ❌ Unhealthy State
    Unhealthy Instances Detected:
    Instance: i-1234567890 | State: unhealthy
<img width="1317" height="673" alt="as19 hc-status ok on tg" src="https://github.com/user-attachments/assets/70fefce7-7f77-4887-a818-324b9e6b4b13" />
<img width="1310" height="662" alt="as19-unhealthy" src="https://github.com/user-attachments/assets/b60c59f9-a8c9-43e5-a23f-fb00786ef599" />

    📩 Email notification will also be sent
<img width="1351" height="721" alt="as19-alb-health email" src="https://github.com/user-attachments/assets/5b984ee3-81b6-44ec-9a25-0deace35a16a" />
<img width="1361" height="669" alt="as19-unh-email" src="https://github.com/user-attachments/assets/522ba676-9676-45d2-b167-fac1ff5cdcda" />

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
<img width="1304" height="671" alt="as19-status" src="https://github.com/user-attachments/assets/5491ec91-e66e-4f6b-8a91-a0402b21b6c6" />

# Conclusion

    This project demonstrates a real-world DevOps monitoring solution using AWS services. It ensures high availability by proactively detecting unhealthy instances      and notifying stakeholders immediately.

👨‍💻 Author

Santosh Kumar Sharma (12394), Batch-15

DevOps & Cloud Enthusiast
