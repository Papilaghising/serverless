import json
import boto3

def lambda_handler(event, context):
    sns_client = boto3.client('sns')
    
    for record in event['Records']:
        message = record['body']
        sqs_message = json.loads(message)
        s3_bucket = sqs_message['Records'][0]['s3']['bucket']['name']
        s3_key = sqs_message['Records'][0]['s3']['object']['key']
        
        notification = f"Hello, a new object '{s3_key}' has been added to the '{s3_bucket}' bucket."
        print(notification)
        
        response = sns_client.publish(
            TargetArn="arn:aws:sns:us-east-1:426857564226:my-serverless-task-sns",
            Message=json.dumps({'default': notification}),
            MessageStructure='json'
        )

        print("SNS response:", response)
        
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }

