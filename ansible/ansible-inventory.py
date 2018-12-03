#!/usr/bin/env python
# coding: utf8

from __future__ import unicode_literals
import argparse
import json
import logging
import boto3
from botocore.exceptions import ProfileNotFound
import os

# Time to debug...
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

'''
-------------------------------------------------------------------------------
# http://docs.ansible.com/ansible/developing_inventory.html
-------------------------------------------------------------------------------
'''

'''
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
'''



'''
-------------------------------------------------------------------------------
# Establish a session with AWS
#
-------------------------------------------------------------------------------
'''


def _init_aws_session():
    # By default we use eu-west-1
    aws_region = os.environ.get('AWS_DEFAULT_REGION', 'eu-west-1')

    # Let's go
    try:
        session = boto3.Session(region_name=aws_region)
    except ProfileNotFound as e:
        logger.error(e)
        print(e)
        raise (SystemExit, 1)

    return session


'''
-------------------------------------------------------------------------------
#
# http://docs.ansible.com/ansible/developing_inventory.html
-------------------------------------------------------------------------------
'''
def instances_get(id=None, states=['running']):
    ''' instances_get()

    Return the list of all instances matching filters
        '''
    logger.debug("+ Looking for all running instances")

    session = _init_aws_session()  # Init a BOTO3 session
    ec2 = session.resource(u'ec2')
    fields=["id", "tags", "key_name"]

    Filters = [
        {
            'Name': 'tag:aws:cloudformation:stack-name',
            'Values': [
                '*smoke*',
            ]
        },
    ]

    if id is not None:
        logger.debug("+ Finally, looking only for %s", id)
        Filters.append({
            'Name': 'instance-id',
            'Values': [id],
        })

    if states is not None:
        logger.debug("+ I search %s instances" % states)
        Filters.append({
            'Name': 'instance-state-name',
            'Values': states,
        })

    instances = ec2.instances.filter(Filters=Filters)

    ansible_inventory = {"_meta": {"hostvars": {}}}

    for instance in instances:
        logger.debug("+Found %s" % instance.id)

        if instance.tags and instance.private_ip_address:
            instance_vars = {}

            # parse each key and reformat some
            for tag in instance.tags:
                k = tag['Key'].lower().replace(':', '_').replace('-', '_')
                key = {
                    "role": u"role",
                }.get( k, u"ec2_" + k )

                value = tag['Value'].lower()

                instance_vars[key] = value

            # Add some attributes
            for a in ['private_dns_name', 'public_dns_name', 'image_id', 'vpc_id', ]:
                if getattr(instance, a, False):
                        instance_vars[u'ec2_' + a] = getattr(instance, a)

            # Placement is an array I don't want
            if instance.placement:
                instance_vars[u'ec2_availabilityzone'] = \
                    instance.placement['AvailabilityZone']
                instance_vars[u"ec2_region"] = instance_vars["ec2_availabilityzone"][:-1]

            # Must specify full path of key file
            if instance.key_name:
                instance_vars[u"ansible_ssh_private_key_file"] = \
                    u"~/.ssh/%s.pem" % instance.key_name

            # Ansible use private_ip_address. If not there, instance can't be added
            instance_vars[u"ec2_private_ip_address"] = instance_vars[u"ansible_host"] = \
                instance.private_ip_address

            # Default user name for ansible is cloud-user
            instance_vars[u"ansible_user"] = u"cloud-user"

            # Build groups named after list values
            for g in ["ec2_service", "ec2_stage", "ec2_fonction", "role", "ec2_aws:cloudformation:stack-name"]:
                # Instance has a label/key named as g
                if instance_vars.get(g, False):
                    # If needed Create group in inventory
                    if not ansible_inventory.get(instance_vars[g]):
                        ansible_inventory[instance_vars[g]] = {'hosts': []}

                    ansible_inventory[instance_vars[g]]['hosts'].append(instance.id)

            # Add this instance to global inventory
            ansible_inventory['_meta']['hostvars'].update(
                { instance.id: instance_vars }
            )
        else:
            logger.warning("%s has no tag or no private ip (skipped)" % instance.id)

    # end for instance in instances

    return ansible_inventory


def instance_get(id=None, fields=["id", "state"]):
    ''' instance_get( instanceId)

        Return the state of the instance specified by id
        '''

    return instances_get(id=id, fields=fields)

'''
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
'''
if __name__ == '__main__':
    # Take care of the command line
    parser = argparse.ArgumentParser(
        description='Build an Ansible inventory based on AutoScaling group.'
    )

    parser.add_argument(
        '-i', '--host',
        help='Return vars for given instanceId',
        required=False,
        action='store_true',
        dest='INSTANCEID',
        default=False,
    )

    parser.add_argument(
        '-l', '--list',
        help='Build inventory for all cIAP servers running',
        required=False,
        action='store_true',
        dest='LIST',
    )

    args = parser.parse_args()

    if not args.LIST and not args.INSTANCEID:
        logger.error("You must specify an action: --list or --host.")
        parser.print_help()
        raise (SystemExit, 1)

    if args.LIST and args.INSTANCEID:
        logger.error("You can't use both --list and --host.")
        parser.print_help()
        raise (SystemExit, 1)

    if args.INSTANCEID:
        logger.info("- Looking for: %s..." % args.INSTANCEID)
        _get_host_vars(
            args.INSTANCEID,
            args.PROFILENAME,
        )

    if args.LIST:
        logger.info("- Building inventory for all filtered EC2")
        print (json.dumps(instances_get(), sort_keys=True, indent=4))