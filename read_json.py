import json
import boto3
import pandas as pd

s3_client = boto3.client('s3')
sns_client = boto3.client('sns')
sns_arn = "arn:aws:sns:us-east-1:381492279969:lambda_transformed_output"


def lambda_handler(event, context):

    try:
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
        body = transformed_data.to_json(orient='records')
        output_bucket = "dd-transform-json"
        output_key = out_key+"_"+"transformed_output.json"
        
        #Adding transformed data to s3
        s3_client.put_object(Bucket = output_bucket, Key = output_key, Body = body)
        
        #Sending message
        message = "Data Transformation and loading SUCESSFUL!!!"
        sns_client_response = sns_client.publish(Subject="Sucessfully transformed delivered data to s3",
                                                TargetArn=sns_arn,
                                                Message=message, 
                                                MessageStructure="text") 
        
    except:
        
        message = "Data Transformation and load FAILED!!!"
        sns_client_response = sns_client.publish(Subject="ERROR!!! In data transformation and loading to s3",
                                        TargetArn=sns_arn,
                                        Message=message, 
                                        MessageStructure="text") 

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
