#!/usr/bin/python

import os
import novaclient.v1_1.client as novaclient
from collections import Counter

os_auth_url = os.environ.get('OS_AUTH_URL')
os_username = os.environ.get('OS_USERNAME')
os_password = os.environ.get('OS_PASSWORD')
os_tenant_name = os.environ.get('OS_TENANT_NAME')
os_region_name = os.environ.get('OS_REGION_NAME')

if os_auth_url is None or os_username is None or os_password is None or os_tenant_name is None:
    print "Undefined variable.  You probably need to source 'openrc' before running this program."
    exit(1)

from novaclient import client
nova = client.Client(2, os_username, os_password, os_tenant_name, os_auth_url, region_name=os_region_name)

vmlist = nova.servers.list(search_opts={'all_tenants': 1})

cnt = Counter()

for vm in vmlist:
    vminfo = vm._info.copy()
    vm_flavor = vminfo['flavor']['id']
    cnt[vm_flavor] += 1



print "10 most common flavors"
print cnt.most_common(10)
