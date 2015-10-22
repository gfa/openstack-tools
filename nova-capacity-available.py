#!/usr/bin/env python
# this script will retrieve hypervisor stats, apply overcommit rules and
# display how many vm of each size can be boot.

import os
import keystoneclient.v2_0.client as ksclient
import novaclient.v1_1.client as novaclient
from novaclient import client
from collections import defaultdict
import json

os_auth_url = os.environ.get('OS_AUTH_URL')
os_username = os.environ.get('OS_USERNAME')
os_password = os.environ.get('OS_PASSWORD')
os_tenant_name = os.environ.get('OS_TENANT_NAME')
os_region_name = os.environ.get('OS_REGION_NAME')

FLAVORS = ['LCTQ.16G', 'LPJT.16G', 'LPJT.24G16core', 'LPJT.login', 'rxjj.m',
           'LPJT.24G', 'LPJT.GM2', 'XAJT.large', 'web2-vm', 'LCTQ.24G', 'rxjj.s']

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


def ram_after_overcommit(ram):
    return ram * 1.2


def cpu_after_overcommit(cpu):
    return cpu * 3


def disk_after_overcommit(disk):
    return disk * 1.3


def hv_resources(hv, vcpu, cpu, disk, disk_used, ram, ram_used):
    vcpus_available = cpu_after_overcommit(cpu) - vcpu
    disk_available = disk_after_overcommit(disk) - disk_used
    ram_available = ram_after_overcommit(ram) - ram_used
    return vcpus_available, disk_available, ram_available


def how_many_vm(hv, vcpus, disk, ram):
    for flavor in FLAVORS:
        vcpu_flavor, disk_flavor, ram_flavor = flavor_info(flavor)
        free_slots = round(
            min(vcpus_available / vcpu_flavor, ram_available / ram_flavor, disk_available / disk_flavor))
        # print "hv: %s, free slots: %d, flavor: %s" % (hv, free_slots, flavor)
        slots[hv][flavor] = free_slots
    return True


def flavor_info(flavor):
    fl = nova.flavors.find(name=flavor)
    try:
        swap = int(fl.swap / 1024)
    except:
        swap = 0
    disk_total = int(fl.disk) + int(swap) + int(fl.ephemeral)
    return fl.vcpus, disk_total, fl.ram

nova = client.Client(2, os_username, os_password, os_tenant_name,
                     os_auth_url, region_name=os_region_name)

slots = defaultdict(dict)
report = defaultdict(dict)

hypervisors = nova.hypervisors.list()
fl = []

for hv in hypervisors:
    hvname = hv.hypervisor_hostname
    if is_hv_enabled(hvname):
        vcpu = hv.vcpus_used
        cpu = hv.vcpus
        disk = hv.local_gb
        disk_used = hv.local_gb_used
        ram = hv.memory_mb
        ram_used = hv.memory_mb_used
        vcpus_available, disk_available, ram_available = hv_resources(
            hv, vcpu, cpu, disk, disk_used, ram, ram_used)
        how_many_vm(hvname, vcpus_available, disk_available, ram_available)

# list aggregates and the hv on it
aggrlist = nova.aggregates.list()
for aggr in aggrlist:
    aggrname = aggr._info['name']
    aggrhosts = aggr._info['hosts']
    for hv in aggrhosts:
        if is_hv_enabled(hv):
            for flavor in FLAVORS:
                key = 0
                key += slots[hv][flavor]
                report[aggrname][flavor] = key


print json.dumps(report, sort_keys=True, indent=4)
