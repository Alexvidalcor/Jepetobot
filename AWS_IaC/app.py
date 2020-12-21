#!/usr/bin/env python3

from aws_cdk import core
from tel_bot_aws.tel_bot_aws_stack import TelBotAwsStack


app = core.App()
TelBotAwsStack(app, "tel-bot-aws", env={'region': 'us-east-1'})

app.synth()
