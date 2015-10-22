#!/usr/bin/python

import os
import keystoneclient.v2_0.client as ksclient
import novaclient.v1_1.client as novaclient
import paramiko

os_auth_url = os.environ.get('OS_AUTH_URL')
os_username = os.environ.get('OS_USERNAME')
os_password = os.environ.get('OS_PASSWORD')
os_tenant_name = os.environ.get('OS_TENANT_NAME')
os_region_name = os.environ.get('OS_REGION_NAME')

if os_auth_url is None or os_username is None or os_password is None or os_tenant_name is None:
    print "Undefined variable.  You probably need to source 'openrc' before running this program."
    exit(1)

def is_hv_enabled(name):
    service = nova.services.list(host=name)
    for srv in service:
      data = srv._info
      if data['status'] == 'disabled':
        return False
      if data['state'] == 'down':
        return False
      return True

def get_real_disk(host):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, 9022)
        stdin, stdout, stderr = ssh.exec_command('/bin/df -m /data | tail -1')
        for line in stdout.readlines():
            device, size, used, available, percent, mountpoint = line.split()
    except:
        used = 0
    return float(used)

from novaclient import client
nova = client.Client(2, os_username, os_password, os_tenant_name, os_auth_url, region_name=os_region_name)

hypervisors = nova.hypervisors.list()

for hv in hypervisors:
    disk = hv._info['local_gb_used']
    name = hv._info['hypervisor_hostname']
    host_ip = hv._info['host_ip']
    if is_hv_enabled(name):
        real_disk = get_real_disk(host_ip)
        real_disk = round(real_disk / 1024, 2)
        float(disk)
        percentage = real_disk * 100 / disk
        print 'nova used disk: %d GiB, real use disk: %d GiB, hv name: %s, ip: %s, usage: %d' % (disk, real_disk, name, host_ip, percentage), '%'
