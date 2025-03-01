class EnvironmentDetails:
    AWS_ACCOUNT_PROFILE = "BugSprint_DEV"

    # Below are the created lambda functions for BugSprint in all the environments.
    LAMBDA_FUNCTION_DETAILS = {
        "BugSprint_DEV": [
            "dev-BugSprint-admin",
            "dev-BugSprint-bugs",
            "dev-BugSprint-bug_search",
            "dev-BugSprint-common",
            "dev-BugSprint-signin",
            "dev-BugSprint-test_cases",
            "dev-BugSprint-ai-tasks",
        ],
    }
    LAMBDA_FUNCTIONS = LAMBDA_FUNCTION_DETAILS[AWS_ACCOUNT_PROFILE]
