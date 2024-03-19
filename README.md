## aws_sns notification project

This project involves creating an automated AWS-based solution for processing daily delivery data from a .json file containing delivery records, these records will be uploaded to an Amazon S3 bucket. An AWS Lambda function, triggered by the file upload, will filter teh records based on delivery status and save the filtered data to another S3 bucket.
Notifications regarding the processing outcome will be sent via Amazon SNS.

## Steps:

## Setting up S3 buckets: 
amazonmachine-cicd 
    To create json content needed to upload to S3
gen-dd-json
    Json data is uploated into this S3 bucket, which will invoke trigger to start a lambda function that transforms and filters data and save the required data into another S3 bucket
dd-transform-json
    The final output is stored in this S3 Bucket as a .json file


## Setting up Amazon SNS Topic:
    Created an SNS topic for sending processing notifications to my email "yenumula.bhanu@gmail.com"

## Creating IAM Role for Lambda
    Created an IAM role with permissions to read from "gen-dd-json" write to "dd-transform-json" and publish messages to SNS topic

## Created and configured AWS Lambda Function:
    Created a Lambda function using Python runtime
    Added the pandas library as a lambda layer 
        functionality of lambda function include:
        Reading JSON file into a pandas DataFrame
        Filtering records where status is "delivered"
        Writting the filtered DataFrame to a new JSON file in "gen-dd-json" using datetime naming format
        Publishing a success or failure message to the SNS topic
    Activated S3 triggers to invoke the function upon file uploads to "gen-dd-json"

## AWS CodeBuild for CI/CD:
    Used GitHub to host lambda function code by setting up AWS CodeBuild linked to my project reprository
    Configured buildspec.yml to automate deployment of lambda function code updates

## Testing and verification:
    Ensured lambda function trigger functonality by manual uploads
    Checking the output for correct implementation of code and processed output of data
    Confirmation of sns topic notification 


