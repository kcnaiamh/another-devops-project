import os
import pulumi
import pulumi_command as command
from utils import read_file

def update_scripts(file_path, instances):
    """
    Update IP addresses in a file using Pulumi's apply() method to handle Output types
    """
    def update_file_content(ips):
        private_ips = ips  # This will be the resolved values

        with open(file_path, "r") as fd:
            content = fd.read()

        content = content.replace('VM1_PRIVATE_IP="0.0.0.0"', f'VM1_PRIVATE_IP="{private_ips[0]}"')\
                           .replace('VM2_PRIVATE_IP="0.0.0.0"', f'VM2_PRIVATE_IP="{private_ips[1]}"')\
                           .replace('VM3_PRIVATE_IP="0.0.0.0"', f'VM3_PRIVATE_IP="{private_ips[2]}"')

        with open(file_path, "w") as fd:
            fd.write(content)

        return "File updated successfully"

    # Combine all private IPs into a single Output and then apply the update
    all_private_ips = pulumi.Output.all(
        instances[0].private_ip,
        instances[1].private_ip,
        instances[2].private_ip
    )

    return all_private_ips.apply(update_file_content)
