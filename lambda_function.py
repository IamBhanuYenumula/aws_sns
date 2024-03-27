import json
import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import boto3

load_dotenv()

# imp main module
def lambda_handler(event, context):

    sns_client = boto3.client('sns')
    s3_client=boto3.client('s3')

    bucket = event["Records"][0]['s3']["bucket"]["name"]
    key = event["Records"][0]['s3']["object"]["key"]
    response = s3_client.get_object(Bucket=bucket,Key=key)
    file_content = response['Body'].read().decode('utf-')
    
    #JSON to pandas dataframe
    data = pd.read_json(file_content)
    data.set_index('id',inplace=True)

    #Filter dataframe
    transformed_data = data[data['status'] == 'delivered']
    
    #saving delivered status json to dd-transform-json
    out_key = key[0:10]
    body = transformed_data.to_csv(index=False)
    output_bucket = os.getenv('output_bucket')
    output_key = out_key+"_"+"transformed_output.csv"


    try:     
        #Adding transformed data to s3
        s3_client.put_object(Bucket = output_bucket, Key = output_key, Body = body)
        
        #Sending message
        message = "Data Transformation and loading SUCESSFUL!!!"
        sns_client_response = sns_client.publish(Subject="Sucessfully transformed delivered data to s3",
                                                TargetArn=os.getenv('sns_arn'),
                                                Message=message, 
                                                MessageStructure="text")     
    except:
        message = "Data Transformation and load FAILED!!!"
        sns_client_response = sns_client.publish(Subject="ERROR!!! In data transformation and loading to s3",
                                        TargetArn=os.getenv('sns_arn'),
                                        Message=message, 
                                        MessageStructure="text") 
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }







