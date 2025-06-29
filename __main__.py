import pulumi
from network import create_network_infrastructure
from security import create_security_groups
from instances import create_instances
# from utils import create_ssh_key, create_config_file

network = create_network_infrastructure()
vpc = network["vpc"]

security = create_security_groups(vpc)

instances = create_instances(
    network=network,
    security_groups=security,
)

pulumi.export('ec2 public ips', [instance.public_ip for instance in instances])
pulumi.export('ec2 private ips', [instance.private_ip for instance in instances])