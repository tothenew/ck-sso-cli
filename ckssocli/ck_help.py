import sys 


def help_utility():
    help_content='''
Welcome to ck-sso-cli
This CLI tool can be used by entities that have AWS Accounts configured as External AWS Accounts in IAM Identity Center.
To configure the CLI, run ck-sso-cli configure
For named profiles, run ck-sso-cli configure --profile my_profile

Once configured, you can run ck-sso-cli login to log into the destination role
For named profiles, run ck-sso-cli login --profile my_profile

Thank you.
    '''
    print(help_content)