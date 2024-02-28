# CK-SSO-CLI - Retrieve AWS Credentials when Using External AWS Accounts in IAM Identity Center
Authenticates a user against AWS IAM Identity Center (SSO) and then retrieves the credentials to update the ~/.aws/credentials file
## Operating System Support
This project is currently supported in the following Operating Systems -
- `macOS`
- `Linux`
- `WSL on Windows`
- `Windows`

## Python Support
This project is written for **Python 3.6 and above**. 

*Older versions of Python are not supported.*
## Prerequisites
### AWS IAM Identity Center (SSO) Prerequisites
- Create a Permission Set in the SSO account which has the permission to perform sts:AssumeRole on any resource (*)
- Go to IAM Roles in the SSO account and retrieve the Role ARN of the newly created Permission Set
- Attach the Permission Set to the required Users/Groups
- Go to the destination account and create a new IAM Role where the trusted entity is the Role ARN retrieved in the previous step
- Attach the requisite permissions that you wish for the user to access in the destination account

### Software Prerequisites
- macOS, Linux or WSL on Windows OS
- [Python 3.6 or above](https://www.python.org/downloads/)
- [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
## Installation

- `pip3 install ck-sso-cli`
- Execute `ck-sso-cli help` to check if the tool is installed correctly
- If you get an error saying `Command ck-sso-cli not found` then add the Python packages installation folder to the Path environment variable. 
   - For Linux, it would be `/home/{username}/.local/bin`

  -  For macOS, it would be `/Users/{username}/Library/Python/{Python Version}/bin`

    - To make sure that you don't have to do this everytime, modify your `~/.bashrc` to add the Python Packages folder to the Path


- Execute `ck-sso-cli configure` and follow the steps to configure your IAM Identity Center profile OR
- Configure ck-sso-cli via the `~/.ck-sso-cli/config.json` file with the following parameters:
```
{
  "default": {
    "sso_start_url": "https://d-xxxxxx.awsapps.com/start/",
    "sso_region": "us-east-1",
    "sso_account_id": "4xxxxxxxxx8",
    "sso_role_name": "AssumeRole_AdminAccess",
    "region": "us-east-1",
    "output": "json",
    "destination_role_arn": "arn:aws:iam::2xxxxxxxxx4:role/SSO_CLI_AdminAccess",
    "email_id": "myemailid@mydomain.com"
  }
}
```
- Named profiles can also be created by executing `ck-sso-cli configure --profile my_profile`
- Named profiles can be directly created in the `~/.ck-sso-cli/config.json` by creating a separate section
```
{
  "myprofile": {
    "sso_start_url": "https://d-yyyyy.awsapps.com/start/",
    "sso_region": "us-east-1",
    "sso_account_id": "4xxxxxxxxx8",
    "sso_role_name": "AssumeRole_AdminAccess",
    "region": "us-east-1",
    "output": "json",
    "destination_role_arn": "arn:aws:iam::2xxxxxxxxx4:role/SSO_CLI_AdminAccess",
    "email_id": "myemailid@mydomain.com"
  },
  "default": {
    "sso_start_url": "https://d-xxxxxx.awsapps.com/start/",
    "sso_region": "us-east-1",
    "sso_account_id": "4xxxxxxxxx8",
    "sso_role_name": "AssumeRole_ROAccess",
    "region": "us-east-1",
    "output": "json",
    "destination_role_arn": "arn:aws:iam::2yyyyyyyyyy4:role/SSO_CLI_ROAccess",
    "email_id": "myemailid@mydomain.com"
  }
}
```
## About the Parameters
- `email_id`: Your official email ID that is used for logging into SSO
- `sso_start_url`: The start URL of the SSO page. This should be in the format of `https://{domain-name}.awsapps.com/start/`
- `sso_region`: The region where SSO is provisioned. For example, `us-east-1`
- `sso_account_id`: The AWS account ID where SSO is provisioned
- `sso_role_name`: The name of the Permission Set that would be used for CLI access
- `destination_role_arn`: The ARN of the IAM Role created in the destination account which the above Permission Set is allowed to assume

All the above parameters are mandatory.

## Usage
- Configure ck-sso-cli by running `ck-sso-cli configure` (or `ck-sso-cli configure --profile my_profile`)
- Once configured, run `ck-sso-cli login` (or `ck-sso-cli login --profile my_profile`)
- In case of default, the credentials will be written in the `~/.aws/credentials` file under the default section
- In case of a named profile, the credentials will be writtne in the `~/.aws/credentials` file under the named profile section
- You can now start using AWS CLI
- Once the credentials expire, run `ck-sso-cli login` (or `ck-sso-cli login --profile my_profile`) again and the credentials would be updated