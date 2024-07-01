class EnvironmentDetails:
    AWS_ACCOUNT_PROFILE = "DEV"

    # Below are the created lambda functions for BugSprint in all the environments.
    LAMBDA_FUNCTION_DETAILS = {
        "DEV": [

        ],
    }
    LAMBDA_FUNCTIONS = LAMBDA_FUNCTION_DETAILS[AWS_ACCOUNT_PROFILE]
