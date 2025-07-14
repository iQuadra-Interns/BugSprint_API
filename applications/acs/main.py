import boto3
import os

lambda_functions = [
    "dev-BugSprint-admin",
    "dev-BugSprint-bugs",
    "dev-BugSprint-bug_search",
    "dev-BugSprint-common",
    "dev-BugSprint-signin",
    "dev-BugSprint-test_cases",
    "dev-BugSprint-ai-tasks",

]
def lambda_handler(event, context):
    lambda_client = boto3.client("lambda")
    ENVIRONMENT_NAME = os.getenv("ENVIRONMENT_NAME")
    
    print(f"ENVIRONMENT_NAME environment variable: {ENVIRONMENT_NAME}")
    
    if ENVIRONMENT_NAME == "DEV":
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
                'body': f"Successfully invoked {len(invoked_functions)} lambda functions: {invoked_functions} (ENVIRONMENT_NAME: {ENVIRONMENT_NAME})"
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': f"Error invoking lambda functions: {str(e)}"
            }
    
    return {
        'statusCode': 200,
        'body': f"No need of ACS (ENVIRONMENT_NAME: {ENVIRONMENT_NAME})"
    }
