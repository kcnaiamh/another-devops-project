import pulumi
import pulumi_aws as aws
import pulumi_tls as tls
import os
import secrets
import string

def read_file(file_path: str) -> str:
    """Read and return the contents of a file"""
    with open(f'./{file_path}', 'r') as fd:
        return fd.read()

def gen_password(n: int) -> str:
    """Generate a secure random password of length n"""
    # Character pools
    uppercase = secrets.choice(string.ascii_uppercase)
    lowercase = secrets.choice(string.ascii_lowercase)
    digit = secrets.choice(string.digits)

    # Fill the rest of the password length
    all_chars = string.ascii_letters + string.digits
    remaining_chars = [secrets.choice(all_chars) for _ in range(n - 3)]

    # Combine and shuffle to randomize order
    password_list = [uppercase, lowercase, digit] + remaining_chars
    secrets.SystemRandom().shuffle(password_list)  # Secure shuffle

    return ''.join(password_list)

def create_ssh_key(key_name):
    """Create an SSH key pair"""

    # Generate a private key (only if Pulumi actually needs it)
    ssh_key = tls.PrivateKey(
        "generated-key",
        algorithm="RSA",
        rsa_bits=4096,
    )

    # Declare the AWS KeyPair as a managed Pulumi resource
    aws_key = aws.ec2.KeyPair(
        key_name,
        key_name=key_name,
        public_key=ssh_key.public_key_openssh
    )

    # Save private key locally
    private_key_path = os.path.join(os.path.expanduser("~"), '.ssh', f'{key_name}.id_rsa')

    def write_private_key(private_key_pem):
        os.makedirs(os.path.dirname(private_key_path), exist_ok=True)
        with open(private_key_path, "w") as private_key_file:
            private_key_file.write(private_key_pem)
        os.chmod(private_key_path, 0o600)

    ssh_key.private_key_pem.apply(write_private_key)

    return aws_key

def create_config_file(instances, ssh_key_name):
    """Create SSH config file for connecting to instances"""
    def write_config(all_ips):
        config_content = f'''\
Host host1
    HostName {all_ips[0]}
    User ubuntu
    IdentityFile ~/.ssh/{ssh_key_name}.id_rsa
    ControlMaster auto
    ControlPath ~/.ssh/master-%r@%h:%p
    ControlPersist 10m

Host host2
    HostName {all_ips[1]}
    User ubuntu
    IdentityFile ~/.ssh/{ssh_key_name}.id_rsa
    ControlMaster auto
    ControlPath ~/.ssh/master-%r@%h:%p
    ControlPersist 10m

Host host3
    HostName {all_ips[2]}
    User ubuntu
    IdentityFile ~/.ssh/{ssh_key_name}.id_rsa
    ControlMaster auto
    ControlPath ~/.ssh/master-%r@%h:%p
    ControlPersist 10m
'''
        config_path = os.path.join(os.path.expanduser("~"), '.ssh', 'config')
        with open(config_path, "w") as config_file:
            config_file.write(config_content)

    pulumi.Output.all(
        instances[0].public_ip,
        instances[1].public_ip,
        instances[2].public_ip,
    ).apply(write_config)
