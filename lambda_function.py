import json
import random
from datetime import datetime
import boto3
# imp main module
def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    bucket = "gen-dd-json"
    key = ((datetime.now().date()).strftime("%Y-%m-%d"))+"-"+"raw_input.json"
    data_list = []
    for i in range(10):
        data = {"id": i+1,
                "status":random.choice(["delivered","cancelled","order placed"]),
                "amount":round(random.uniform(10,100),2),
                "date":((datetime.now().date()).strftime("%Y-%m-%d"))}
        data_list.append(data)
    ex=json.dumps(data_list)   
    s3_client.put_object(Bucket=bucket,Key=key,Body=ex)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }







