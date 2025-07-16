import boto3
import os
from environment_details import EnvironmentDetails
def lambda_handler(event, context):
    lambda_client = boto3.client("lambda")
    ENVIRONMENT_NAME = os.getenv("ENVIRONMENT_NAME", "BugSprint_DEV")
    
    print(f"ENVIRONMENT_NAME environment variable: {ENVIRONMENT_NAME}")
    
    lambda_functions = [func for func in EnvironmentDetails.LAMBDA_FUNCTION_DETAILS.get(ENVIRONMENT_NAME, []) 
                       if not func.endswith("-acs")]
    
    if not lambda_functions:
        return {
            'statusCode': 200,
            'body': f"No lambda functions found for environment: {ENVIRONMENT_NAME}"
        }
    
    try:
        invoked_functions = []
        for function in lambda_functions:
            print(f"Invoking lambda function: {function}")
            response = lambda_client.invoke(
                FunctionName=function,
                InvocationType='Event'
            )
            print(f"Invocation response for {function}: {response['StatusCode']}")
            invoked_functions.append(function)
        
        return {
            'statusCode': 200,
            'body': f"Successfully invoked {len(invoked_functions)} lambda functions in {ENVIRONMENT_NAME}: {invoked_functions}"
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error invoking lambda functions: {str(e)}"
        }
