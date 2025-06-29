sudo apt update
sudo apt install -y docker.io

VM1_PRIVATE_IP="192.168.1.65"
VM2_PRIVATE_IP="192.168.2.14"
VM3_PRIVATE_IP="192.168.3.117"

network_id=$(sudo docker network create --subnet 10.10.0.0/16 br-vxlan)
short_id=${network_id:0:12}
BRIDGE_NAME="br-${short_id}"

sudo ip link add vxlan-03 type vxlan id 103 remote ${VM3_PRIVATE_IP} dstport 4789 dev enX0
sudo ip link set vxlan-03 up
sudo ip link set vxlan-03 master ${BRIDGE_NAME}

sudo ip link add vxlan-02 type vxlan id 102 remote ${VM2_PRIVATE_IP} dstport 4789 dev enX0
sudo ip link set vxlan-02 up
sudo ip link set vxlan-02 master ${BRIDGE_NAME}