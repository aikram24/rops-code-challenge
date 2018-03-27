import boto3
import os
import argparse
import time

ec2Client = boto3.client('ec2')
ec2Resource = boto3.resource('ec2')

def create_network_stack():
    network_info = {}
    vpc = ec2Resource.create_vpc(CidrBlock='192.168.0.0/16')
    # vpc.create_tags(Tags=[{"Key": "Name", "Value": "reactive"}])
    vpc.wait_until_available()
    network_info.update({'vpc_id': vpc.id})

    # create then attach internet gateway
    ig = ec2Resource.create_internet_gateway()
    vpc.attach_internet_gateway(InternetGatewayId=ig.id)
    network_info.update({"ig_id": ig.id})

    # create a route table and a public route
    route_table = vpc.create_route_table()
    route = route_table.create_route(
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=ig.id
    )
    network_info.update({"route_table_id": route_table.id})
    
    # create subnet
    subnet = ec2Resource.create_subnet(CidrBlock='192.168.1.0/24', VpcId=vpc.id)
    network_info.update({'subnet_id': subnet.id})

    # associate the route table with the subnet
    route_table.associate_with_subnet(SubnetId=subnet.id)

    # Create sec group
    sec_group = ec2Resource.create_security_group(GroupName='ReactiveOps', Description='ReactiveOps Instance SG', VpcId=vpc.id)
    sec_group.authorize_ingress(IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=80,ToPort=80)
    sec_group.authorize_ingress(IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=22,ToPort=22)
    network_info.update({'sec_group': sec_group.id})

    return network_info


def genrate_key_pair(key_name):
    keypair = ec2Client.create_key_pair(KeyName='{}'.format(key_name))
    file = open("{}.pem".format(key_name),"w") 
    file.write(keypair['KeyMaterial'])
    file.close() 

def create_instance(ami_id, key_pair, instance_type, sg_id, subnet_id):
    user_data='''
#cloud-config
repo_update: true
repo_upgrade: all

packages:
 - python-pip

runcmd:
 - mkdir /tmp/repo
 - git clone https://github.com/aikram24/rops-code-challenge.git /tmp/repo
 - bash /tmp/repo/flask_app/start.sh &
    '''
    instanceDict = ec2Resource.create_instances(
        ImageId = ami_id,
        KeyName = key_pair,
        InstanceType = instance_type,
        SecurityGroupIds = [sg_id],
        SubnetId=subnet_id,
        MinCount = 1,
        MaxCount = 1,
        UserData=user_data,        
    )
    # Wait for it to launch before assigning the elastic IP address
    instanceDict[0].wait_until_running()
    # Allocate an elastic IP
    eip = ec2Client.allocate_address(Domain='vpc')
    # Associate the elastic IP address with the instance launched above
    ec2Client.associate_address(
        InstanceId = instanceDict[0].id,
        AllocationId = eip["AllocationId"])
    return eip['PublicIp']

def main():
    parser = argparse.ArgumentParser(description='ReactiveOps Coding Challenge')
    parser.add_argument('-k', '--keyname', help='SSH Key Name', default='OpsKey', required=False)
    parser.add_argument('-a', '--ami', help='AMI ID', default='ami-ac442ac3', required=False)
    parser.add_argument('-i', '--instancetype', help='Instance Type', default='t2.small', required=False)
    args = parser.parse_args()
    
    KEY_NAME=args.keyname
    AMI_ID=args.ami
    INSTANCE_TYPE=args.instancetype
    NETWORK_INFO = create_network_stack()
    VPC_ID = NETWORK_INFO['vpc_id']
    SG_ID = NETWORK_INFO['sec_group']
    SUBNET_ID = NETWORK_INFO['subnet_id']
    genrate_key_pair(KEY_NAME)
    create_instance(AMI_ID, KEY_NAME, INSTANCE_TYPE, SG_ID, SUBNET_ID)
    # CREATE_INSTANCE = create_instance(AMI_ID, KEY_NAME, INSTANCE_TYPE, "sg-07ea0d3071dd3e1f7", "subnet-02950b620b4fa3d31")        # Test
    time.sleep(60)
    print ("Web App: http://{}".format(CREATE_INSTANCE))
    print ("SSH into Server: ssh -i \"{}.pem\" ubuntu@{}".format(KEY_NAME, CREATE_INSTANCE))