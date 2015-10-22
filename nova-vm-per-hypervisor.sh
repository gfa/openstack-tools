#!/bin/sh
set -e
HYPERVISORES=`nova hypervisor-list | grep ip | awk '{print $4}' | tr '\n' ' '`
INSTANCES=`nova list --all-tenants |grep '|' |grep -v ID | awk '{print $2}' | tr '\n' ' '`
TEMPDIR=`mktemp -d`


cd $TEMPDIR
for instance in ${INSTANCES}
do
    nova show $instance > $instance
done

for hypervisor in ${HYPERVISORES}
do
    echo $hypervisor
    vms=`grep -l $hypervisor * |tr '\n' ' '`
    for vm in ${vms}
    do 
        nova show $vm |grep ' name' | awk '{print $4}'
    done
    echo "\n"
    echo "\n"
done
