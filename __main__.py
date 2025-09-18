import pulumi
from network import create_network_infrastructure
from security import create_security_groups
from instances import create_instances
from utils import create_ssh_key, create_config_file
from configure import update_scripts

# Configuration
config = pulumi.Config()
SSH_KEY_NAME = config.require("sshKeyName")

# Create infrastructure components
aws_key = create_ssh_key(SSH_KEY_NAME)

network = create_network_infrastructure()  # returns vpc, public_subnets[]
vpc = network["vpc"]

security = create_security_groups(vpc)

instances = create_instances(
    network=network,
    security_groups=security,
    config={
        "ssh_key_name": SSH_KEY_NAME,
    }
)

create_config_file(instances, SSH_KEY_NAME)

pulumi.export('ec2 public ips', [instance.public_ip for instance in instances])
pulumi.export('ec2 private ips', [instance.private_ip for instance in instances])


for i in range(1, 4):
    update_scripts(f"./scripts/setup-vxlan-host-{i}.sh", instances)


# configure_ec2s_with_cloud_init_check(SSH_KEY_NAME, instances)
