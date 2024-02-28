import sys 
import subprocess
import json
import boto3
import os 
import time

def get_home_directory():
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        # Linux or MacOS
        cmd = 'echo $HOME'
    elif sys.platform.startswith('win'):
        # Windows
        cmd = 'echo %USERPROFILE%'
    else:
        print(f'Unsupported platform: {sys.platform}')
        exit(1)

    directory = subprocess.run(cmd, shell=True, capture_output=True)
    directory = directory.stdout.decode('utf-8').strip()
    return directory

def login_utility():
    directory = get_home_directory()

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
        existing_data = ''
        with open(f'{directory}/.aws/config','r') as aws_config_read:
                  existing_data = aws_config_read.read()
                  if profile in existing_data:
                      ts=time.time()
                      existing_data = existing_data.replace(f'{profile}',f'DELETE-{ts}')
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
            aws_config_write.write(f'{aws_config_contents}\n')
            aws_config_write.write(f'{existing_data}\n')
    else:
        existing_data = ''
        with open(f'{directory}/.aws/config','r') as aws_config_read:
                  existing_data = aws_config_read.read()
                  if profile in existing_data:
                      ts=time.time()
                      existing_data = existing_data.replace(f'{profile}',f'DELETE-{ts}')
                    
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
            aws_config_write.write(f'{aws_config_contents}\n')
            aws_config_write.write(f'{existing_data}\n')
        

def get_sso_creds(profile):
    try:
        boto3.setup_default_session(profile_name=f'{profile}-sso')
        client = boto3.client('sts')
        client.get_caller_identity()
    except:
        subprocess.run(['aws','sso','login','--profile',f'{profile}-sso'])


def assume_role_using_sts(config,profile,directory):
    boto3.setup_default_session(profile_name=f'{profile}-sso')
    client = boto3.client('sts')
    response = client.assume_role(RoleArn=config[profile]['destination_role_arn'],RoleSessionName=config[profile]['email_id'])
    aki = response['Credentials']['AccessKeyId']
    sak = response['Credentials']['SecretAccessKey']
    st = response['Credentials']['SessionToken']

    existing_data = ''
    with open(f'{directory}/.aws/credentials','r') as aws_credentials_read:
        existing_data = aws_credentials_read.read()
        if f'[{profile}]' in existing_data:
            ts=time.time()
            existing_data = existing_data.replace(f'{profile}',f'DELETE-{ts}')

    with open(f'{directory}/.aws/credentials','w') as aws_credentials_write:
        aws_credentials_content = f'''[{profile}]
aws_access_key_id = {aki}
aws_secret_access_key = {sak}
aws_session_token = {st}
        '''
        aws_credentials_write.write(f'{aws_credentials_content}\n')
        aws_credentials_write.write(f'{existing_data}\n')
    print("Credentials written in ~/.aws/credentials file and are ready for use.")