# Whoami Lambda API 

Whoami is part of an ongoing security project of mine. The goal of this project is to determine as much information can be gleaned a website's visitor in under 30 seconds. Whoami is an application that is served by Lambda and is written in python. This is the same code that drives the Whoami page on my personal [blog](http://gotcipher.io/default/whoami/).  

This application was built using the AWS Severless Application model or SAM. SAM is a method of packaging and templatizing production Lambda functions. 

## Requirements
- An API key from [IPStack](https://ipstack.com/)
- AWS SecretsManager (To store the API keys for IPStack)
- [AWS Severless Application Model CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
 
## Deployment
1. Store your IPStack API key in AWS SecretsManager ```aws secretsmanager create-secret --name api_key --secret-string "{\"ipstack\": \"API_KEY\"}"``` 
2. Take note of the ARN. You'll need this to deploy the API. 
3. Run ```deploy.sh```. You will be prompted to enter the ARN of the secret you created for the API Key. 
4. You'll receive the URL for your Lambda when the script completes.  
