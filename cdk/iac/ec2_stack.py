# AWS libraries
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
    aws_iam as iam
)
from constructs import Construct
import json

# Custom importation
from env.cdk_public_env import showPublicIp, appName, createSG
from env.cdk_secrets_env import awsRegion, vpcId, ec2Type, sgID, sgPorts, ec2Key, envDeploy, tz

# User data imported
with open("./user_data/config.json") as fconfig:
    cloudwatchConfig = json.load(fconfig)

with open("./user_data/install_docker.sh", "r") as fdocker:
    userData=fdocker.read()
    userData += f'echo \'{json.dumps(cloudwatchConfig)}\' > /opt/aws/amazon-cloudwatch-agent/bin/config.json'
    userData += "\n/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json -s"

userDataProcessed = userData.replace("REPLACEREGION", awsRegion).replace("REPLACEAPPNAME", appName).replace("REPLACEENVNAME", envDeploy).replace("REPLACETZ", tz)


# AMI used
amazonLinux = ec2.MachineImage.latest_amazon_linux2(
    cpu_type=ec2.AmazonLinuxCpuType.ARM_64,
    edition=ec2.AmazonLinuxEdition.STANDARD
)

# EC2 configuration
class Ec2Stack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Existing VPC
        vpc = ec2.Vpc.from_lookup(
            self, appName + "-" + envDeploy + "_Ec2-vpc", vpc_id=vpcId, is_default=True)

        # Existing SG or create a new one
        if createSG:
            sg = ec2.SecurityGroup(
                self,
                id = appName + "-" + envDeploy + "_Ec2-sg",
                vpc = vpc,
                allow_all_outbound=True,
                description = "CDK Security Group",
                security_group_name = appName + "-" + envDeploy + "_Ec2-sg"
            )

            for element in range(len(sgPorts)):
                sg.add_ingress_rule(
                    peer=ec2.Peer.any_ipv4(),
                    connection=ec2.Port.tcp(sgPorts[element]),
                    description="CDK Rule",
                )

        else:
            sg = ec2.SecurityGroup.from_security_group_id(
                self, appName + "-" + envDeploy + "_Ec2-sg", sgID, mutable=False)

        # Instance Role and managed Polices
        role = iam.Role(self, appName + "-" + envDeploy + "_Ec2-role",
                        assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"))
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("SecretsManagerReadWrite"))
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchLogsFullAccess"))

        # Set Ec2 key pair
        key_pair = ec2.KeyPair.from_key_pair_attributes(self, appName + "-" + envDeploy + "_Ec2-key1",
            key_pair_name= ec2Key,
        )

        # Ec2 instance creation
        host = ec2.Instance(self, appName + "-" + envDeploy + "_Ec2",
                            instance_type=ec2.InstanceType(
                                instance_type_identifier=ec2Type),
                            instance_name=appName + "-" + envDeploy + "_Ec2-instance",
                            machine_image=amazonLinux,
                            vpc=vpc,
                            key_pair=key_pair,
                            security_group=sg,
                            vpc_subnets=ec2.SubnetSelection(
                                subnet_type=ec2.SubnetType.PUBLIC),
                            user_data=ec2.UserData.custom(userDataProcessed),
                            role=role
                            )

        host.instance.add_property_override("BlockDeviceMappings", [{
                "DeviceName": "/dev/xvda",
                "Ebs": {
                    "VolumeSize": "8",
                    "VolumeType": "gp3",
                    "Iops": "100",
                    "DeleteOnTermination": "true"
                }
            }
        ])

        # Print public ip of the instance
        if showPublicIp:
            CfnOutput(self, "Output",
                      value=host.instance_public_ip)
