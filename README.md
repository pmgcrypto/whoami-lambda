# Whoami Lambda API 

Whoami is part of an ongoing security project of mine. The goal of this project is to determine as much information can be gleaned a website's visitor in under 30 seconds. Whoami is an application that is served by Lambda and is written in python. This is the same code that drives the Whoami page on my personal [blog](http://gotcipher.io/default/whoami/).  

This application was built using the AWS Severless Application model or SAM. SAM is a method of packaging and templatizing production Lambda functions. 

## Requirements
- An API key from [IPStack](https://ipstack.com/)
- AWS SecretsManager (To store the API keys for IPStack)
- [AWS Severless Application Model CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
 
## Deployment
1. ```git clone git@github.com:pmgcrypto/whoami-lambda.git```
2. ``` cd whoami-lambda```
3. Store your IPStack API key in AWS SecretsManager. Replace API_KEY with the API key provided to you by IPStack. 
   
    ```aws secretsmanager create-secret --name api_key --secret-string "{\"ipstack\": \"API_KEY\"}"```

5. Take note of the ARN assigned to the IPStack API key. You'll need this to deploy the API. 
6. Run ```deploy.sh```. First, you will be prompted to enter the ARN of the secret you created for the API Key. Lastly, you'll be asked to provide the name of the bucket used to store your AWS Lambda code. You would have specified this while setting up the AWS SAM CLI.
```
Enter the ARN of the secret in AWS SecretsManager that contains your IPStack API Key.
> arn:aws:secretsmanager:us-east-1:123456789012:secret:api_key-3ABCe

Enter the bucket were you will be storing your code. This is the bucket you specified while configuring AWS SAM
> lambda-sam-bucket

Collecting requests
  Using cached requests-2.24.0-py2.py3-none-any.whl (61 kB)
Collecting chardet<4,>=3.0.2
  Using cached chardet-3.0.4-py2.py3-none-any.whl (133 kB)
Collecting idna<3,>=2.5
  Using cached idna-2.10-py2.py3-none-any.whl (58 kB)
Collecting urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1
  Using cached urllib3-1.25.10-py2.py3-none-any.whl (127 kB)
Collecting certifi>=2017.4.17
  Using cached certifi-2020.6.20-py2.py3-none-any.whl (156 kB)
Installing collected packages: chardet, idna, urllib3, certifi, requests
Successfully installed certifi-2020.6.20 chardet-3.0.4 idna-2.10 requests-2.24.0 urllib3-1.25.10
Building function 'WhoamiFunc'
Running PythonPipBuilder:ResolveDependencies
Running PythonPipBuilder:CopySource

Build Succeeded

Built Artifacts  : .aws-sam/build
Built Template   : .aws-sam/build/template.yaml

Commands you can use next
=========================
[*] Invoke Function: sam local invoke
[*] Deploy: sam deploy --guided
    
Uploading to d7b4c375398b912175a99336ef74d163  541709 / 541709.0  (100.00%)

Successfully packaged artifacts and wrote output template to file /Users/JohnDoe/Git/whoami-lambda/_deploy/deploy-1600041265.yaml.
Execute the following command to deploy the packaged template
sam deploy --template-file /Users/JohnDoe/Git/whoami-lambda/_deploy/deploy-1600041265.yaml --stack-name <YOUR STACK NAME>


        Deploying with following values
        ===============================
        Stack name                 : whoami-api-stack
        Region                     : None
        Confirm changeset          : False
        Deployment s3 bucket       : None
        Capabilities               : ["CAPABILITY_IAM"]
        Parameter overrides        : {'SecretArnParam': 'arn:aws:secretsmanager:us-east-1:123456789012:secret:api_key-3ABC'}

Initiating deployment
=====================
WhoamiFunc may not have authorization defined.

Waiting for changeset to be created..

CloudFormation stack changeset
------------------------------------------------------------------------------------------------------------------------------------------------------
Operation                                          LogicalResourceId                                  ResourceType                                     
------------------------------------------------------------------------------------------------------------------------------------------------------
* Modify                                           ServerlessRestApi                                  AWS::ApiGateway::RestApi                         
* Modify                                           WhoamiFunc                                         AWS::Lambda::Function                            
------------------------------------------------------------------------------------------------------------------------------------------------------

Changeset created successfully. arn:aws:cloudformation:us-east-1:123456789012:changeSet/samcli-deploy1600041423/089be292-8c16-4bdd-bf00-88421ddb6042


2020-09-13 16:57:14 - Waiting for stack create/update to complete

CloudFormation events from changeset
-----------------------------------------------------------------------------------------------------------------------------------------------------
ResourceStatus                        ResourceType                          LogicalResourceId                     ResourceStatusReason                
-----------------------------------------------------------------------------------------------------------------------------------------------------
UPDATE_IN_PROGRESS                    AWS::Lambda::Function                 WhoamiFunc                            -                                   
UPDATE_COMPLETE                       AWS::Lambda::Function                 WhoamiFunc                            -                                   
UPDATE_COMPLETE                       AWS::CloudFormation::Stack            whoami-api-stack                      -                                   
UPDATE_COMPLETE_CLEANUP_IN_PROGRESS   AWS::CloudFormation::Stack            whoami-api-stack                      -                                   
-----------------------------------------------------------------------------------------------------------------------------------------------------

CloudFormation outputs from deployed stack
------------------------------------------------------------------------------------------------------------------------------------------------------
Outputs                                                                                                                                              
------------------------------------------------------------------------------------------------------------------------------------------------------
Key                 whoamiApi                                                                                                                        
Description         This is the URL of your new Lambda function:                                                                 
Value               https://akdfisow3465.execute-api.us-east-1.amazonaws.com/Prod/whoami/                                                              
------------------------------------------------------------------------------------------------------------------------------------------------------

Successfully created/updated stack - whoami-api-stack in None


########
URL for whoami API:
"https://akdfisow3465.execute-api.us-east-1.amazonaws.com/Prod/whoami/"
```
7. Once the deplyoment script completes, browse to the Lambda function using your favorite browser. 
```json
{
  "UserAgent": "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0",
  "IPAddress": "104.149.141.66",
  "ISP": "AS40676, US",
  "Referrer": "Unknown",
  "IsTor": true,
  "OpenPorts": [
    22,
    23,
    110,
    143
  ],
  "ClosedPorts": [
    21,
    25,
    80,
    135,
    139,
    443,
    445,
    993,
    995,
    3306,
    3389,
    5900,
    8080
  ],
  "GeographicInformation": {
    "Continent": "North America",
    "Country": "United States",
    "Region": "California",
    "City": "Walnut"
  }
}
```