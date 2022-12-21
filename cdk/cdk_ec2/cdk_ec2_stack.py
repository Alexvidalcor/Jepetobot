# AWS libraries
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
    aws_iam as iam
)

from constructs import Construct

# Custom importation
from modules.cdk_support import *

# User data imported
with open("./user_data/install_docker.sh") as f:
    userData = f.read()
userDataProcessed = userData.replace("REPLACEREGION", awsRegion)

# AMI used
amazonLinux = ec2.MachineImage.latest_amazon_linux(
    cpu_type=ec2.AmazonLinuxCpuType.X86_64,
    edition=ec2.AmazonLinuxEdition.STANDARD,
    generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
)

# EC2 configuration
class Ec2Stack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc.from_lookup(
            self, appName+"_VPC", vpc_id=vpcId, is_default=True)
        sg = ec2.SecurityGroup.from_security_group_id(
            self, appName+"_SG", sgID, mutable=False)

        # Instance Role and S3 managed Policy
        role = iam.Role(self, appName + "_Ec2_Role",
                        assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"))

        host = ec2.Instance(self, appName + "_Ec2",
                            instance_type=ec2.InstanceType(
                                instance_type_identifier=ec2Type),
                            instance_name=instanceName+"-instance",
                            machine_image=amazonLinux,
                            vpc=vpc,
                            key_name=keyName,
                            security_group=sg,
                            vpc_subnets=ec2.SubnetSelection(
                                subnet_type=ec2.SubnetType.PUBLIC),
                            user_data=ec2.UserData.custom(userDataProcessed),
                            role=role
                            )

        host.instance.add_property_override("BlockDeviceMappings", [{
            "DeviceName": "/dev/xvda",
            "Ebs": {
                "VolumeSize": "10",
                "VolumeType": "io1",
                "Iops": "150",
                "DeleteOnTermination": "true"
            }
        }, {
            "DeviceName": "/dev/sdb",
            "Ebs": {
                "VolumeSize": "10",
                "VolumeType": "gp2"
            }
        }
        ])

        # Print public ip of the instance
        if showPublicIp:
            CfnOutput(self, "Output",
                      value=host.instance_public_ip)
