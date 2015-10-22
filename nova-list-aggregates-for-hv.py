#!/usr/bin/env python
# this script will retrieve hypervisor stats, apply overcommit rules and
# display how many vm of each size can be boot.

import os
import keystoneclient.v2_0.client as ksclient
import novaclient.v1_1.client as novaclient
from novaclient import client
from collections import defaultdict
import json
import argparse

os_auth_url = os.environ.get('OS_AUTH_URL')
os_username = os.environ.get('OS_USERNAME')
os_password = os.environ.get('OS_PASSWORD')
os_tenant_name = os.environ.get('OS_TENANT_NAME')
os_region_name = os.environ.get('OS_REGION_NAME')

if os_auth_url is None or os_username is None or os_password is None or os_tenant_name is None:
    print "Undefined variable.  You probably need to source 'openrc' before running this program."
    exit(1)

argparser = argparse.ArgumentParser(description='list hosts on each host aggregate')
argparser.add_argument('-D', '--disabled', default=False, action='store_true', help='show disabled computes')
args = argparser.parse_args()

def is_hv_enabled(name):
    if args.disabled:
        return True
    service = nova.services.list(host=name)
    for srv in service:
        data = srv._info
        if data['status'] == 'disabled':
            return False
        if data['state'] == 'down':
            return False
        return True


nova = client.Client(2, os_username, os_password, os_tenant_name,
                     os_auth_url, region_name=os_region_name)

hypervisors = nova.hypervisors.list()

report = defaultdict(list)


aggrlist = nova.aggregates.list()
for aggr in aggrlist:
    aggrname = aggr._info['name']
    aggrhosts = aggr._info['hosts']
    for hv in aggrhosts:
        if is_hv_enabled(hv):
                report[hv].append(aggrname)
                #report[aggrname].append(hv)
                #print report[aggrname]


print json.dumps(report, sort_keys=True, indent=4)
