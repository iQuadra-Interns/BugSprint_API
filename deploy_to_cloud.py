import os
import subprocess
import patoolib

from environment_details import EnvironmentDetails

# Project-Account-Lambda Specific info: *DOUBLE-CHECK THESE*
LAMBDA_FUNCTIONS_LIST = EnvironmentDetails.LAMBDA_FUNCTIONS
AWS_ACCOUNT_PROFILE = EnvironmentDetails.AWS_ACCOUNT_PROFILE


# Code Hyper-Params
zip_name = "lambda-deploy.zip"

excluded_folders = [".git", ".gitignore", ".idea", "__pycache__", ".env",
                    "README.md", "_MACOSX", ".DS_Store", "venv", "lambda-deploy.zip", "deploy_to_lambda.py",
                    "deploy_to_cloud.py", "environment_details.py", "delete.py", "test.py", "mainapp.log"]

project_folder = os.getcwd()

# Delete the zip file and the temp folder if exists
existing_zip_file_path = os.path.join(project_folder, zip_name)
if os.path.exists(existing_zip_file_path):
    os.remove(existing_zip_file_path)

# Zipping project excluding the special files and folder
zip_file_path = os.path.join(project_folder, zip_name)
folders_to_include = [folder for folder in os.listdir(project_folder) if folder not in excluded_folders]
patoolib.create_archive(zip_name, folders_to_include, verbosity=-1)

for LAMBDA_FUNCTION_NAME in LAMBDA_FUNCTIONS_LIST:
    try:
        # Deploy
        subprocess.check_output(['aws', 'lambda', 'update-function-code', '--function-name', LAMBDA_FUNCTION_NAME,
                                 '--zip-file', 'fileb://' + zip_file_path, '--profile', AWS_ACCOUNT_PROFILE])
    except subprocess.CalledProcessError as e:
        # If the lambda isn't there, continue.
        print(f"{LAMBDA_FUNCTION_NAME} is not present in the {AWS_ACCOUNT_PROFILE} environment")

    finally:
        print(f"Project successfully Zipped and uploaded to:\n"
              f"Lambda Name:{LAMBDA_FUNCTION_NAME}\n"
              f"Using profile: {AWS_ACCOUNT_PROFILE}")

# Delete the existing zip
if os.path.exists(existing_zip_file_path):
    os.remove(existing_zip_file_path)
