scripts to get stats, reports or information from openstack
----------------------------------------------------------


- nova-ip-tenant-per-hv.sh:

  **USAGE:**
  ./nova-ip-tenant-per-hv.sh <hv ip>

  will show which vm run on the hypervisor, their ip address and the security group (which is named after the tenant)

- load-script:
  **USAGE**
  copy network information on the second,third, fourth, etc lines and run. it will spawn many as 2 iperf processes peer vm. one client one server.
  also it will run stress, script is tested on centos.

- nova-capacity-available:
  this script will retrieve hypervisor stats, apply overcommit rules and display how many vm of each size can be boot.

- most-common-flavors.py:
  it list the 10 most used flavors, across a cloud, and how many vm use them.

- nova-list-aggregates-for-hv.py
  list all the aggregates a host is in, passing `-D` it will show disabled hosts

- remaining-ip.py
  list how many ports in each status a network has and how many ip are allocated on its subnets
  if you subtract `ports` to `allocated ip` you know how many ports can be created. some of the ports mark as `DOWN` may be recycled but is a manual operation (delete if not in use)

- test-new-vlan
  this script is useful after add a new vlan to neutron, it needs thet network uuid as parameter, it will boot a small vm on each hypervisor (using the network you give) and validate that  dhcp and metadata are working, it will print **'OK'** or **'FAILED'** for each hypervisor.

  explanation of the script:
  nova boot --user-data -->  pass user-data to nova

  echo "#!/bin/sh" > $TEMP
  echo echo $name >> $TEMP
  echo echo $hv >> $TEMP
  user data, in this case, is a shell script which print the hypervisor and vm name

  user data can be only retrieved by the vm over metadata service, cloud-init does that at boot, and executes if user-data is an script

  dhcp, metadata and all vm network traffic is "inside" of a vlan, vm does not not it but all the traffic gets tagged by the hv

  if the switch port is not configured to allow that vlan tag to pass, neither dhcp, metadata or any other vm traffic will pass


attic
-----

- nova-check-all-computes:
  will boot a vm on each hypervisor

- nova-images-per-hypervisor:
  will show all images in use on each hypervisor

- \*
