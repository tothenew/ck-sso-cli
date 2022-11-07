from setuptools import setup, find_packages, os

here = os.path.abspath(os.path.dirname(__file__))
exec(open(os.path.join(here, 'ckssocli/version.py')).read())


setup(
    name='ck-sso-cli',
    version=__version__,
    description='Provides a wrapper for AWS IAM Identity Center authentication to an External AWS Account',
    packages=find_packages(),
    license='Apache License 2.0',
    author='Aditya Ajay',
    author_email='aditya.ajay@tothenew.com',
    url='https://github.com/okta-awscli/okta-awscli',
    entry_points={
        'console_scripts': [
            'ck-sso-cli=ckssocli.ck_sso_cli:main',
        ],
    },
    install_requires=[
        'boto3'
        ]
)

# export PATH="/home/aditya/.local/bin:$PATH"