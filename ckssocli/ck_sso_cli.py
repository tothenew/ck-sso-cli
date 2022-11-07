import sys
from ckssocli.ck_configuration import configure_utility
from ckssocli.ck_help import help_utility
from ckssocli.ck_login import login_utility

def main():
    if len(sys.argv)==1:
        print('ERROR: ck-sso-cli requires atleast one of the following options - configure, login or help. \nRun ck-sso-cli help for more information.')
    elif len(sys.argv)>4:
        print('ERROR: Too many arguments. Run ck-sso-cli help for more information.')
    else: 
        if sys.argv[1]=='configure':
            configure_utility()
        elif sys.argv[1]=='login':
            login_utility()
        elif sys.argv[1]=='help':
            help_utility()
        else:
            print("Invalid arguements. Run ck-sso-cli help for more information.")

if __name__ == "__main__":
    main()
