#!/usr/bin/env python

import os
import sys
import logging
import argparse
import json
from collections import Counter
from neutronclient.neutron import client


os_auth_url = os.environ.get('OS_AUTH_URL')
os_username = os.environ.get('OS_USERNAME')
os_password = os.environ.get('OS_PASSWORD')
os_tenant_name = os.environ.get('OS_TENANT_NAME')
os_region_name = os.environ.get('OS_REGION_NAME')

if os_auth_url is None or os_username is None or os_password is None or os_tenant_name is None:
    print "Undefined variable.  You probably need to source 'openrc' before running this program."
    exit(1)

argparser = argparse.ArgumentParser(description='list remaining ip on a network')
argparser.add_argument('-n', '--network_id', nargs=1, default=None, help='network to examine')
args = argparser.parse_args()

if args.network_id:
    NET_ID = args.network_id[0]
else:
    print "i need a network id"
    print sys.argv[0] + " -h to check the help"
    sys.exit(1)


neutron = client.Client('2.0',username=os_username, password=os_password, tenant_name=os_tenant_name, auth_url=os_auth_url, insecure=True, region_name=os_region_name)
#logging.basicConfig(level=logging.DEBUG)
#neutron = client.Client('2.0', endpoint_url=OS_URL, token=OS_TOKEN)
neutron.format = 'json'
#network = {'name': 'mynetwork', 'admin_state_up': True}
#neutron.create_network({'network':network})
#networks = neutron.list_networks(name='mynetwork')
#print networks
#network_id = networks['networks'][0]['id']
##neutron.delete_network(network_id)

# http://stackoverflow.com/questions/5619685/conversion-from-ip-string-to-integer-and-backward-in-python
def IP2Int(ip):
    o = map(int, ip.split('.'))
    res = (16777216 * o[0]) + (65536 * o[1]) + (256 * o[2]) + o[3]
    return res

ports = neutron.list_ports(network_id=NET_ID)

ports_dict = json.dumps(ports)
ports_dict = json.loads(ports_dict)
total_ports = len(ports_dict['ports'])
count = int(total_ports)
cnt_ports = Counter()
while ( count > 0 ):
        count = count -1
        port_status = ports_dict['ports'][count]['status']
        cnt_ports[port_status] += 1


#print cnt_ports

cnt_ips = 0

subnets = neutron.show_network(NET_ID,fields='subnets')
for subnet_id in subnets['network']['subnets']:
        allocation_pools = neutron.show_subnet(subnet_id, fields='allocation_pools')
        count = int(len(allocation_pools['subnet']['allocation_pools']))
        while ( count > 0 ):
                count = count -1
                start = allocation_pools['subnet']['allocation_pools'][count]['start']
                end = allocation_pools['subnet']['allocation_pools'][count]['end']
                start = IP2Int(start)
                end = IP2Int(end)
                total = end - start
                cnt_ips = cnt_ips + total


print cnt_ports
print "all allocated ip: %s" % int(cnt_ips)
