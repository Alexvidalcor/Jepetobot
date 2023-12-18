# AWS libraries
from aws_cdk import (
    Stack,
    aws_lambda as lambda1,
    aws_s3 as _s3,
    aws_events as events,
    aws_events_targets as targets,
    aws_iam as iam
)
from constructs import Construct

# Custom importation
from env.cdk_public_env import appName
from env.cdk_secrets_env import envDeploy, awsRegion


# MainClass
class Lambda1Stack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        with open("lambda/lambda1/ec2_start_instance.py", "r") as fLambdaRead:
            lambdaData=fLambdaRead.read()

        lambdaDataProcessed = lambdaData.replace("REPLACEREGION", awsRegion).replace("REPLACEAPPNAME", appName).replace("REPLACEENVDEPLOY", envDeploy)

        # Instance Role and managed Polices
        lambdaRole = iam.Role(self, appName + "_Lambda1_Role",
                        assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"))
        lambdaRole.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2FullAccess"))


        # Create ec2_start lambda function
        function1 = lambda1.Function(self, "ec2_start_lambda",
                                    runtime=lambda1.Runtime.PYTHON_3_10,
                                    handler="index.ec2_start_function",
                                    code=lambda1.Code.from_inline(lambdaDataProcessed),
                                    role=lambdaRole)


        # Define the event rule to execute the Lambda at time specified
        rule = events.Rule(
            self, appName + "_Lambda1_event1",
            schedule=events.Schedule.cron(hour='07', minute='0'),
        )

        # Associate the Lambda as the target of the event rule
        rule.add_target(targets.LambdaFunction(function1))