#!/bin/bash
set -e

IP=`/bin/echo $1 | sed 's/\./-/g'`

HV=`nova service-list | egrep $IP\\\\.  |head -1 | awk '{print $6}'`

for vm in `nova hypervisor-servers $HV |grep instance |awk '{print $2}'` ; do nova show $vm |grep  -e security_groups -e network ;echo '' ; done
