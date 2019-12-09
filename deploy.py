import os
from subprocess import call, PIPE
from zipfile import ZipFile

STACK_NAME = 'BowlPickerBackend'
TEMPLATE_NAME = 'template.yaml'


def call_command(command):
    source_dir = os.getcwd()
    print(f'COMMAND: {command}')
    call(command.split(), stdout=PIPE, cwd=source_dir)


def get_lambdas():
    return ['get_picks', 'save_picks']


def zip_lambda(lambda_):
    with ZipFile(f'./build/{lambda_}.zip', 'w') as myzip:
        myzip.write(f'./lambdas/{lambda_}.py', f'{lambda_}.py')


def push_lambda_to_s3(lambda_):
    bucket_name = 'jtcruthers-lambda-zipfiles'
    zip_name = f'{lambda_}.zip'
    path_to_zip = f'./build/{zip_name}'

    command = f'aws s3api put-object --body {path_to_zip} --bucket {bucket_name} --key {zip_name}'
    call_command(command)


def zip_and_push_lambdas():
    lambdas = get_lambdas()
    for lambda_ in lambdas:
        zip_lambda(lambda_)
        push_lambda_to_s3(lambda_)


def update_cfn_stack():
    command = f'aws cloudformation update-stack --stack-name {STACK_NAME} --template-body file://{TEMPLATE_NAME} --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND'
    call_command(command)


def deploy_cfn():
    zip_and_push_lambdas()
    update_cfn_stack()


if __name__ == '__main__':
    deploy_cfn()