import os
from aws_cdk.core import App, Environment
from stack_api import LambdaStack


app = App()
LambdaStack(
    app,
    "LambdaStack",
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
    stack_name="aws-etl-scheduler",
)
app.synth()
