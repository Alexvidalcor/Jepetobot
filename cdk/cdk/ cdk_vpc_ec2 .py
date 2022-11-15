from aws_cdk import CfnOutput, Stack
import aws_cdk.aws_ec2 as ec2
from constructs import Construct

instance_name = "name_instance",
vpc_id = "MY-VPC-ID"  # Import an Exist VPC
ec2_type = "t2.micro"
key_name = "id_rsa"
sg = "sg"


# linux_ami = ec2.GenericLinuxImage({
#     "eu-west-1": "ami-0ee415e1b8b71305f"
# })

tags: {
    group: 'group',
    name: 'name'
  }


amazon_linux = ec2.MachineImage.latest_amazon_linux(
    cpu_type=ec2.AmazonLinuxCpuType.X86_64,
    edition=ec2.AmazonLinuxEdition.STANDARD,
    generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
    storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
)


with open("./user_data/install_docker.sh") as f:
    user_data = f.read()


class CdkVpcEc2Stack(Stack):

    def __init__(self, scope: Construct, id: str) -> None:

        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=vpc_id)

        host = ec2.Instance(self, "myEC2",
                            instance_type=ec2.InstanceType(
                                instance_type_identifier=ec2_type),
                            instance_name=instance_name,
                            machine_image=linux_ami,
                            vpc=vpc,
                            key_name=key_name,
                            security_group=sg,
                            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                            user_data=ec2.UserData.custom(user_data)
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
