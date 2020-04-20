#!/bin/bash

/usr/local/share/openvswitch/scripts/ovs-ctl stop
rm /usr/local/etc/openvswitch/conf.db
rm /usr/local/var/log/openvswitch/ovs-vswitchd.log
/usr/local/share/openvswitch/scripts/ovs-ctl --system-id=1 start

#/usr/local/share/openvswitch/scripts/ovs-ctl --no-ovsdb-server --system-id=1 restart
ovs-vsctl add-br s1
ovs-vsctl set BRIDGE s1 other_config:datapath-id="0000000000000003"
#ovs-vsctl set-controller s1 tcp:10.0.0.2:6633

