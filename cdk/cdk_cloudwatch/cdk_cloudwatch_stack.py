
# AWS libraries
from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_logs as logs,
    aws_lambda as _lambda,
    RemovalPolicy,
    Duration
)
from constructs import Construct


# Custom importation
from modules.cdk_support import *


class CloudWatchStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the CloudWatch log group
        logGroup = logs.LogGroup(self, "{appName}-log_group",
            log_group_name=f"{appName}-log_group",
            retention=logs.RetentionDays.TWO_WEEKS,
            removal_policy=RemovalPolicy.DESTROY,
        )

        listLogsPath = ["/var/log/application/app.log",
                        "/var/log/application/errors.log",
                        "/var/log/application/user.log",]

        # Creates log streams for each file at the specified path
        for logsFilename in listLogsPath:
            logStream = logs.LogStream(
                self,
                f'{appName}-{logsFilename.split("/")[-1]}-stream',
                log_group=logGroup,
                log_stream_name=f'{appName}-{logsFilename.split("/")[-1]}-stream'
            )
