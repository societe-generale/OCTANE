import boto3
import os
import re
import jmespath
import argparse

def aws_role_credentials(role_arn: str, role_session_name: str):
    boto_client = boto3.client(
        'sts',
        aws_access_key_id=creds['key'],
        aws_secret_access_key=creds['value'], 
    )
    response = boto_client.assume_role(RoleArn=role_arn, RoleSessionName=role_session_name)

    os.environ['AWS_ACCESS_KEY_ID']=response['Credentials']['AccessKeyId']
    os.environ['AWS_SECRET_ACCESS_KEY']=response['Credentials']['SecretAccessKey']
    os.environ['AWS_SESSION_TOKEN']=response['Credentials']['SessionToken']

def f_vpc_id(_vpc_name, _region):
    try:
        t_filter = [{'Name':'tag:Name', 'Values':[_vpc_name]}]
        vpcs = list(ec2_resource.vpcs.filter(Filters=t_filter))
        for vpc in vpcs:
            return vpc.id
    except Exception as e:
        print("No VPC id found for {}".format(_vpc_name))
        print(e.response['Error']['Code'])
        return 'none'

def f_owner_id(_stack_id):
  try:
    return re.search('(.+):([0-9]+):(.+)', _stack_id).group(2)
  except Exception as e:
    print("No owner id found for {}".format(_stack_id))
    print(e.response['Error']['Code'])
    return 'none'

def f_rtb_id(_vpc_id, _region):
  rtb_ids = []
  try:
    t_filter = [{'Name':'vpc-id', 'Values':[_vpc_id]},
      {'Name':'association.main', 'Values':['false']},]
    vpc_route_tables = ec2_resource.route_tables.filter(Filters=t_filter)
    for vpc_route_table in vpc_route_tables:
      rtb_ids.append(vpc_route_table.id)
    return rtb_ids
  except Exception as e:
    print("No VPC route table found for {}".format(_vpc_id))
    print(e.response['Error']['Code'])
    return 'none'

def f_subnet_id(_vpc_id):
  try:
    t_filter = [{'Name':'vpc-id', 'Values':[_vpc_id]},]
    subnets = ec2_client.describe_subnets(Filters=t_filter)
    return jmespath.search('Subnets[*].SubnetId', subnets)
  except Exception as e:
    print("No subnets id found for {}".format(_vpc_id))
    print(e.response['Error']['Code'])
    return ['none']

def f_create_vpc_peering_connection(_peer_owner_id, _peer_vpc_id, _vpc_id, _region):
  try:
    return ec2_client.create_vpc_peering_connection(
        DryRun = False,
        PeerOwnerId = _peer_owner_id,
        PeerVpcId = _peer_vpc_id,
        VpcId = _vpc_id,
        PeerRegion = _region
    )
  except Exception as e:
    print("Unable to  create VPC peering connection")
    print(e.response['Error']['Code'])
    return {'ResponseMetadata': {'HTTPStatusCode': 400 }}

def f_accept_vpc_peering_connection(_vpc_peering_connection_id):
  try:
    return ec2_resource.VpcPeeringConnection(_vpc_peering_connection_id).accept()
  except Exception as e:
    print("Unable to accpet VPC peering connection")
    print(e.response['Error']['Code'])
    return {'ResponseMetadata': {'HTTPStatusCode': 400 }}

def f_create_route(_route_table_ids, _destination_cidr_block, _vpc_peering_connection_id):
  for _route_table_id in _route_table_ids:
    try:
      ec2_client.create_route(
          DestinationCidrBlock = _destination_cidr_block,
          RouteTableId = _route_table_id,
          VpcPeeringConnectionId = _vpc_peering_connection_id
        )
    except Exception as e:
      if e.response['Error']['Code'] == 'RouteAlreadyExists':
        print("Route already exists")
      else:
        print("f_create_route unexpected error: %s" % e)

def f_vpc_subnet(_vpc_id):
  try:
    retour = ec2_client.describe_vpcs(VpcIds = [ _vpc_id ],)
    return jmespath.search('Vpcs[].CidrBlock', retour)
  except Exception as e:
    print("No VPC subnet found for {}".format(_vpc_id))
    print(e.response['Error']['Code'])

def f_retrieve_security_groups(_vpc_id, _stack_name):
  try:
    t_filter = [{'Name':'vpc-id', 'Values':[_vpc_id]}, {'Name':'group-name', 'Values':[_stack_name + '-SGADM-*']},]
    return ec2_resource.security_groups.filter(Filters=t_filter)
  except Exception as e:
    print("No security groups found for {}, {}".format(_vpc_id, _stack_name))
    print(e.response['Error']['Code'])

# Argument parser
parser = argparse.ArgumentParser(description="Make VPC peering connection between two VPC")
parser.add_argument("-r", "--region", help="Set AWS region, default to eu-west-1", default="eu-west-1")
parser.add_argument("-a", "--awsprofile", help="Set AWS profile (example: dev)", required=False)
parser.add_argument("-p", "--peerstackname", help="Set peer stack name (example: octanetst)", required=True)
parser.add_argument("-q", "--stackname", help="Set stack name (example: admin-octanetst)", required=True)
parser.add_argument("-v", "--peervpcname", help="Set peer VPC name (example: VPC_OCTANE_TST)", required=True)
parser.add_argument("-w", "--vpcname", help="Set VPC name (example: VPC_ADMIN-OCTANE_TST)", required=True)
args = parser.parse_args()

# Set common variables
default_region = args.region
try:
    os.environ['AWS_PROFILE'] = args.awsprofile
except Exception as e:
    aws_role_credentials('arn:aws:iam::1234567890:role/role-name', 'role-name')

os.environ['AWS_DEFAULT_REGION'] = default_region


# Set common resources
ec2_resource = boto3.resource('ec2', region_name=default_region)
ec2_client = boto3.client('ec2')
cloudformation = boto3.resource('cloudformation')

# Peer informations
peer_stack_name = args.peerstackname
peer_vpc_name = args.peervpcname
peer_stack = cloudformation.Stack(peer_stack_name)
peer_stack_id = peer_stack.stack_id
peer_vpc_id = f_vpc_id(peer_vpc_name, default_region)
peer_owner_id = f_owner_id(peer_stack_id)
peer_vpc_rtb_id = f_rtb_id(peer_vpc_id, default_region)

# Own informations
stack_name = args.stackname
vpc_name = args.vpcname
vpc_id = f_vpc_id(vpc_name, default_region)
vpc_rtb_id = f_rtb_id(vpc_id, default_region)
vpc_peering_tag_name = args.peervpcname + "_" + args.vpcname

def vpc_peering():
  retour = f_create_vpc_peering_connection(peer_owner_id, peer_vpc_id, vpc_id, default_region)
  if jmespath.search('ResponseMetadata.HTTPStatusCode', retour) == 200:
    vpc_peering_connection_id = jmespath.search('VpcPeeringConnection.VpcPeeringConnectionId', retour)
    retour = f_accept_vpc_peering_connection(vpc_peering_connection_id)
    if jmespath.search('ResponseMetadata.HTTPStatusCode', retour) == 200:
      retour = ec2_resource.create_tags(
        DryRun = False,
        Resources=[ vpc_peering_connection_id, ],
        Tags=[ { 'Key': 'Name', 'Value': vpc_peering_tag_name }, ]
        )
      vpc_cidr = f_vpc_subnet(vpc_id)
      peer_vpc_cidr = f_vpc_subnet(peer_vpc_id)
      f_create_route(vpc_rtb_id, peer_vpc_cidr[0], vpc_peering_connection_id)
      f_create_route(peer_vpc_rtb_id, vpc_cidr[0], vpc_peering_connection_id)
      security_groups = f_retrieve_security_groups(peer_vpc_id, peer_stack_name)
      for security_group in security_groups:
        t_security_group = ec2_resource.SecurityGroup(security_group.id)
        try:
          response = t_security_group.authorize_ingress(
              GroupId= security_group.id,
              IpPermissions=[
                {
                  'FromPort': 22,
                  'ToPort': 22,
                  'IpProtocol': 'tcp',
                  'IpRanges': [ {
                      'CidrIp': vpc_cidr[0],
                      'Description': 'grant admin'
                    },
                  ],
                },
              ],
          )
        except Exception as e:
          if e.response['Error']['Code'] == 'InvalidPermission.Duplicate':
             print("Rule already exists")
          else:
             print("Unexpected error: %s" % e)
             return 1
    else:
      print("Error when accepting VPC Peering connection")
      return 1
    return 0
  else:
    print("Error when creating VPC peering connection")
    return 1



vpc_peering()