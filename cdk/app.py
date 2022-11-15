from aws_cdk import App, Environment, Tags
from cdk_vpc_ec2.cdk_vpc_ec2_stack import CdkVpcEc2Stack


env_aws = Environment(account="YOUR_ACCOUNT_ID_WITHOUT_HYPHEN", region="eu-west-1")

app = App()
CdkVpcEc2Stack(app, "cdk-vpc-ec2", env=env_aws)

Tags.of(CdkVpcEc2Stack).add("Group", "group_name").add("Name", "name")

app.synth()
