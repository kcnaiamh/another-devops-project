import pulumi
import pulumi_aws as aws

def create_network_infrastructure():
    """Create VPC, subnets, gateways and route tables"""

    VPC_CIDR = '192.168.0.0/16'
    PUBLIC_SUBNET_CIDRS = ['192.168.1.0/24', '192.168.2.0/24', '192.168.3.0/24']
    AZ_NAMES = aws.get_availability_zones(state="available")


    # Create VPC
    vpc = aws.ec2.Vpc(
        resource_name='poc-vpc',
        cidr_block=VPC_CIDR,
        enable_dns_support=True,
        enable_dns_hostnames=True,
        tags={'Name': 'poc-vpc'}
    )

    # Create internet gateway
    internet_gateway = aws.ec2.InternetGateway(
        resource_name='poc-igw',
        vpc_id=vpc.id,
        tags={'Name': 'poc-igw'}
    )

    # Create public subnet
    public_subnets = []
    for i in range(3):
        subnet = aws.ec2.Subnet(
            resource_name=f'poc-public-subnet-{i}',
            vpc_id=vpc.id,
            cidr_block=PUBLIC_SUBNET_CIDRS[i],
            map_public_ip_on_launch=True,
            availability_zone=AZ_NAMES.names[i],
            tags={'Name': f'poc-public-subnet-{i}'}
        )
        public_subnets.append(subnet)

    # Create route tables
    public_route_table = aws.ec2.RouteTable(
        resource_name='poc-public-rt',
        vpc_id=vpc.id,
        routes=[
            aws.ec2.RouteTableRouteArgs(
                cidr_block='0.0.0.0/0',
                gateway_id=internet_gateway.id
            )
        ],
        tags={'Name': 'poc-public-rt'}
    )


    # Associate route tables with subnets
    public_route_table_associations = []
    for i in range(3):
        association = aws.ec2.RouteTableAssociation(
            resource_name=f'public-rt-association-{i}',
            subnet_id=public_subnets[i].id,
            route_table_id=public_route_table.id
        )
        public_route_table_associations.append(association)


    return {
        "vpc": vpc,
        "public_subnets": public_subnets,
    }