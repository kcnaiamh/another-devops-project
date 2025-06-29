import pulumi
import pulumi_aws as aws

def create_security_groups(vpc):
    """Create security groups for each component"""

    security_group = aws.ec2.SecurityGroup(
        resource_name='cluster-security-group',
        vpc_id=vpc.id,
        description="Cluster security group",
        ingress=[
            # SSH access from anywhere
            aws.ec2.SecurityGroupIngressArgs(
                protocol='tcp',
                from_port=22,
                to_port=22,
                cidr_blocks=['0.0.0.0/0'],
            ),
            aws.ec2.SecurityGroupIngressArgs(
                protocol='-1',
                from_port=0,
                to_port=0,
                self=True,
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
            'Name': 'cluster-security-group'
        }
    )

    return [security_group]