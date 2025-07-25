class EnvironmentDetails:
    AWS_ACCOUNT_PROFILE = "BugSprint_DEV"

    # Below are the created lambda functions for BugSprint in all the environments.
    LAMBDA_FUNCTION_DETAILS = {
        "BugSprint_DEV":[
            "dev-BugSprint-admin",
            "dev-BugSprint-bugs",
            "dev-BugSprint-bug_search",
            "dev-BugSprint-common",
            "dev-BugSprint-signin",
            "dev-BugSprint-test_cases",
            "dev-BugSprint-ai-tasks",
            "dev-BugSprint-lambda-acs"

        ],
        "BugSprint_QA":[
            "qa-BugSprint-admin",
            "qa-BugSprint-bugs",
            "qa-BugSprint-bug_search",
            "qa-BugSprint-common",
            "qa-BugSprint-signin",
            "qa-BugSprint-test_cases",
            "qa-BugSprint-ai-tasks",
            "qa-BugSprint-lambda-acs"
        ],
        "BugSprint_STAGING":[
            "staging-BugSprint-admin",
            "staging-BugSprint-bugs",
            "staging-BugSprint-bug_search",
            "staging-BugSprint-common",
            "staging-BugSprint-signin",
            "staging-BugSprint-test_cases",
            "staging-BugSprint-ai-tasks",
            "staging-BugSprint-lambda-acs"
        ],
        "BugSprint_PROD":[
            "prod-BugSprint-admin",
            "prod-BugSprint-bugs",
            "prod-BugSprint-bug_search",
            "prod-BugSprint-common",
            "prod-BugSprint-signin",
            "prod-BugSprint-test_cases",
            "prod-BugSprint-ai-tasks",
            "prod-BugSprint-lambda-acs"
        ]
    }
    LAMBDA_FUNCTIONS = LAMBDA_FUNCTION_DETAILS[AWS_ACCOUNT_PROFILE]
