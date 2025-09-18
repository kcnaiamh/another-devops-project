import pulumi_aws as aws

def create_instances(network, security_groups, config):
    """Create EC2 instances for each component"""
    SSH_KEY_NAME = config["ssh_key_name"]

    fw_stop_ud = """\
ufw disable
systemctl stop ufw
"""

    instances = []
    for i in range(3):
        instance = aws.ec2.Instance(
            resource_name = f'instance-{i}',
            instance_type='t2.micro',
            ami='ami-01811d4912b4ccb26',
            subnet_id=network['public_subnets'][i].id,
            key_name=SSH_KEY_NAME,
            vpc_security_group_ids=[security_groups[0].id],
            associate_public_ip_address=True,
            user_data=fw_stop_ud,
            user_data_replace_on_change=True,
            tags={
                'Name': f'instance-{i}'
            }
        )
        instances.append(instance)

    return instances
