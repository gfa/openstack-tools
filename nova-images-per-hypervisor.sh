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
    vm=`grep -l $hypervisor * |tr '\n' ' '`
    grep image ${vm} |awk -F \| '{print $3}'|sort | uniq
    echo "\n"
    echo "\n"
done
