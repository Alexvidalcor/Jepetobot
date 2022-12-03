# AWS libraries
from aws_cdk import CfnOutput, Stack
from constructs import Construct

#Python libraries
import os

# Variables from Github Secrets
instanceName = os.environ["AWS_NAME_INSTANCE"],
vpcId = os.environ["AWS_VPC_ID"]  # Import an Exist VPC
ec2Type = "t2.micro"
keyName = os.environ["AWS_KEY"]
sg = os.environ["AWS_SG"]


# AMI used
amazonLinux= ec2.MachineImage.latest_amazon_linux(
    cpu_type=ec2.AmazonLinuxCpuType.X86_64,
    edition=ec2.AmazonLinuxEdition.STANDARD,
    generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2022,
    storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
)

# User data imported
with open("./user_data/install_docker.sh") as f:
    userData = f.read()


# EC2 configuration
class aws_ec2(Stack):

    def __init__(self, scope: Construct, id: str) -> None:

        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=vpcId)

        host = ec2.Instance(self, "myEC2",
                            instance_type=ec2.InstanceType(
                                instance_type_identifier=ec2Type),
                            instance_name=instanceName,
                            machine_image=amazonLinux,
                            vpc=vpc,
                            key_name=keyName,
                            security_group=sg,
                            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
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

        CfnOutput(self, "Output",
                  value=host.instance_public_ip)
