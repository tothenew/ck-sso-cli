import sys 
import subprocess
import json
import boto3
import os 

def login_utility():
    directory = subprocess.run(['pwd'], capture_output=True)
    directory = directory.stdout.decode('utf-8')
    directory = directory.split('\n')
    directory = directory[0]

    profile = 'default'

    if len(sys.argv) == 2:
        print('Using default profile')
    elif len(sys.argv) == 4:
        if sys.argv[2] == '--profile':
            profile = sys.argv[3]
            print(f'Using {profile} profile')
        else:
            print(f'Invalid flag {sys.argv[2]}. Acceptable flag is --profile.')
            exit()

    config = {}
    with open(f'{directory}/.ck-sso-cli/config.json', 'r') as config_file_read:
        try:
            config = json.load(config_file_read)
            check = config[profile]
        except:
            if profile!='default':
                print(f'Profile {profile} not found. To configure the profile, run ck-sso-cli configure --profile {profile}')
            else:
                print('No default profile configured. To configure a default profile, run ck-sso-cli configure')
            exit()
    update_aws_config(config=config,profile=profile,directory=directory)
    get_sso_creds(profile=profile)
    assume_role_using_sts(config=config,profile=profile,directory=directory)



def update_aws_config(config,profile,directory):
    try:
        aws_config_read = open(f'{directory}/.aws/config','r')
        aws_config_read.close()
    except:
        os.system(f'mkdir {directory}/.aws > file.tmp')
        os.system(f'touch {directory}/.aws/config')
        os.system(f'touch {directory}/.aws/credentials')
    if profile != 'default':
        with open(f'{directory}/.aws/config','w') as aws_config_write:
            aws_config_contents = f'''[profile {profile}-sso]
sso_start_url = {config[profile]['sso_start_url']}
sso_region = {config[profile]['sso_region']}
sso_account_id = {config[profile]['sso_account_id']}
sso_role_name = {config[profile]['sso_role_name']}
region = {config[profile]['region']}
output = {config[profile]['output']}

[profile {profile}]
output = json
            '''
            aws_config_write.write(aws_config_contents)
    else:
        with open(f'{directory}/.aws/config','w') as aws_config_write:
            aws_config_contents = f'''[profile {profile}-sso]
sso_start_url = {config[profile]['sso_start_url']}
sso_region = {config[profile]['sso_region']}
sso_account_id = {config[profile]['sso_account_id']}
sso_role_name = {config[profile]['sso_role_name']}
region = {config[profile]['region']}
output = {config[profile]['output']}

[{profile}]
output = json
            '''
            aws_config_write.write(aws_config_contents)
        

def get_sso_creds(profile):
    try:
        boto3.setup_default_session(profile_name=f'{profile}-sso')
        client = boto3.client('sts')
        client.get_caller_identity()
        # print(response)
    except:
        subprocess.run(['aws','sso','login','--profile',f'{profile}-sso'])


def assume_role_using_sts(config,profile,directory):
    boto3.setup_default_session(profile_name=f'{profile}-sso')
    client = boto3.client('sts')
    response = client.assume_role(RoleArn=config[profile]['destination_role_arn'],RoleSessionName=config[profile]['email_id'])
    aki = response['Credentials']['AccessKeyId']
    sak = response['Credentials']['SecretAccessKey']
    st = response['Credentials']['SessionToken']

    with open(f'{directory}/.aws/credentials','w') as aws_credentials_write:
        aws_credentials_content = f'''[{profile}]
aws_access_key_id = {aki}
aws_secret_access_key = {sak}
aws_session_token = {st}
        '''
        aws_credentials_write.write(aws_credentials_content)
    print("Credentials written in ~/.aws/credentials file and are ready for use.")