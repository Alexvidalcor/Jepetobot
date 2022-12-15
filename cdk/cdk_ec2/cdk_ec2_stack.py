# AWS libraries
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2
)

from constructs import Construct

# Custom importation
import modules.public_env as penv
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

        vpc = ec2.Vpc.from_lookup(self, penv.appName+"_VPC", vpc_id=vpcId, is_default=True)
        sg = ec2.SecurityGroup.from_security_group_id(self, penv.appName+"_SG", sgID, mutable=False)

        host = ec2.Instance(self, penv.appName + "_Ec2",
                            instance_type=ec2.InstanceType(
                                instance_type_identifier=ec2Type),
                            instance_name=instanceName+"-instance",
                            machine_image=amazonLinux,
                            vpc=vpc,
                            key_name=keyName,
                            security_group=sg,
                            vpc_subnets=ec2.SubnetSelection(
                                subnet_type=ec2.SubnetType.PUBLIC),
                            user_data=ec2.UserData.custom(userData)
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
        if penv.showPublicIp:
            CfnOutput(self, "Output",
                        value=host.instance_public_ip)
