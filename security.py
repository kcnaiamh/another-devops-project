import pulumi
import pulumi_aws as aws

def create_security_groups(vpc):
    """Create security groups for each component"""

    security_group = aws.ec2.SecurityGroup(
        resource_name='public-security-group',
        vpc_id=vpc.id,
        description="Enable SSH and VxLAN traffic",
        ingress=[
            # SSH access from anywhere
            aws.ec2.SecurityGroupIngressArgs(
                protocol='tcp',
                from_port=22,
                to_port=22,
                cidr_blocks=['103.78.226.226/32'],
            ),
            aws.ec2.SecurityGroupIngressArgs(
                protocol='tcp',
                from_port=80,
                to_port=80,
                cidr_blocks=['103.78.226.226/32'],
            ),
            aws.ec2.SecurityGroupIngressArgs(
                protocol='udp',
                from_port=4789,
                to_port=4789,
                cidr_blocks=['192.168.0.0/22'],
            ),
            aws.ec2.SecurityGroupIngressArgs(
                protocol='icmp',
                from_port=-1,
                to_port=-1,
                cidr_blocks=['192.168.0.0/22'],
            ),
        ],
        egress=[
            aws.ec2.SecurityGroupEgressArgs(
                protocol='-1',
                from_port=0,
                to_port=0,
                cidr_blocks=['0.0.0.0/0'],
            )
        ],
        tags={
            'Name': 'public-security-group'
        }
    )

    return [security_group]
