# RE

## Table of Contents

- [Fabric Switches and Management IP](#fabric-switches-and-management-ip)
  - [Fabric Switches with inband Management IP](#fabric-switches-with-inband-management-ip)
- [Fabric Topology](#fabric-topology)
- [Fabric IP Allocation](#fabric-ip-allocation)
  - [Fabric Point-To-Point Links](#fabric-point-to-point-links)
  - [Point-To-Point Links Node Allocation](#point-to-point-links-node-allocation)
  - [Loopback Interfaces (BGP EVPN Peering)](#loopback-interfaces-bgp-evpn-peering)
  - [Loopback0 Interfaces Node Allocation](#loopback0-interfaces-node-allocation)
  - [VTEP Loopback VXLAN Tunnel Source Interfaces (VTEPs Only)](#vtep-loopback-vxlan-tunnel-source-interfaces-vteps-only)
  - [VTEP Loopback Node allocation](#vtep-loopback-node-allocation)

## Fabric Switches and Management IP

| POD | Type | Node | Management IP | Platform | Provisioned in CloudVision | Serial Number |
| --- | ---- | ---- | ------------- | -------- | -------------------------- | ------------- |
| RE | l3leaf | RE-AVD-BrdrLeaf1A | 192.168.255.19/24 | vEOS-LAB | Provisioned | - |
| RE | l3leaf | RE-AVD-BrdrLeaf1B | 192.168.255.20/24 | vEOS-LAB | Provisioned | - |
| RE | l2leaf | RE-AVD-L2Leaf1A | 192.168.255.21/24 | vEOS-LAB | Provisioned | - |
| RE | l2leaf | RE-AVD-L2Leaf1B | 192.168.255.22/24 | vEOS-LAB | Provisioned | - |
| RE | l2leaf | RE-AVD-L2Leaf2A | 192.168.255.23/24 | vEOS-LAB | Provisioned | - |
| RE | l2leaf | RE-AVD-L2Leaf2B | 192.168.255.24/24 | vEOS-LAB | Provisioned | - |
| RE | l3leaf | RE-AVD-Leaf1A | 192.168.255.15/24 | vEOS-LAB | Provisioned | - |
| RE | l3leaf | RE-AVD-Leaf1B | 192.168.255.16/24 | vEOS-LAB | Provisioned | - |
| RE | l3leaf | RE-AVD-Leaf2A | 192.168.255.17/24 | vEOS-LAB | Provisioned | - |
| RE | l3leaf | RE-AVD-Leaf2B | 192.168.255.18/24 | vEOS-LAB | Provisioned | - |
| RE | spine | RE-AVD-Spine1 | 192.168.255.11/24 | vEOS-LAB | Provisioned | - |
| RE | spine | RE-AVD-Spine2 | 192.168.255.12/24 | vEOS-LAB | Provisioned | - |
| RE | spine | RE-AVD-Spine3 | 192.168.255.13/24 | vEOS-LAB | Provisioned | - |
| RE | spine | RE-AVD-Spine4 | 192.168.255.14/24 | vEOS-LAB | Provisioned | - |

> Provision status is based on Ansible inventory declaration and do not represent real status from CloudVision.

### Fabric Switches with inband Management IP

| POD | Type | Node | Management IP | Inband Interface |
| --- | ---- | ---- | ------------- | ---------------- |

## Fabric Topology

| Type | Node | Node Interface | Peer Type | Peer Node | Peer Interface |
| ---- | ---- | -------------- | --------- | ----------| -------------- |
| l3leaf | RE-AVD-BrdrLeaf1A | Ethernet1 | spine | RE-AVD-Spine1 | Ethernet5 |
| l3leaf | RE-AVD-BrdrLeaf1A | Ethernet2 | spine | RE-AVD-Spine2 | Ethernet5 |
| l3leaf | RE-AVD-BrdrLeaf1A | Ethernet3 | spine | RE-AVD-Spine3 | Ethernet5 |
| l3leaf | RE-AVD-BrdrLeaf1A | Ethernet4 | spine | RE-AVD-Spine4 | Ethernet5 |
| l3leaf | RE-AVD-BrdrLeaf1A | Ethernet5 | mlag_peer | RE-AVD-BrdrLeaf1B | Ethernet5 |
| l3leaf | RE-AVD-BrdrLeaf1A | Ethernet6 | mlag_peer | RE-AVD-BrdrLeaf1B | Ethernet6 |
| l3leaf | RE-AVD-BrdrLeaf1B | Ethernet1 | spine | RE-AVD-Spine1 | Ethernet6 |
| l3leaf | RE-AVD-BrdrLeaf1B | Ethernet2 | spine | RE-AVD-Spine2 | Ethernet6 |
| l3leaf | RE-AVD-BrdrLeaf1B | Ethernet3 | spine | RE-AVD-Spine3 | Ethernet6 |
| l3leaf | RE-AVD-BrdrLeaf1B | Ethernet4 | spine | RE-AVD-Spine4 | Ethernet6 |
| l2leaf | RE-AVD-L2Leaf1A | Ethernet1 | l3leaf | RE-AVD-Leaf1A | Ethernet7 |
| l2leaf | RE-AVD-L2Leaf1A | Ethernet2 | l3leaf | RE-AVD-Leaf1B | Ethernet7 |
| l2leaf | RE-AVD-L2Leaf1A | Ethernet3 | mlag_peer | RE-AVD-L2Leaf1B | Ethernet3 |
| l2leaf | RE-AVD-L2Leaf1A | Ethernet4 | mlag_peer | RE-AVD-L2Leaf1B | Ethernet4 |
| l2leaf | RE-AVD-L2Leaf1B | Ethernet1 | l3leaf | RE-AVD-Leaf1A | Ethernet8 |
| l2leaf | RE-AVD-L2Leaf1B | Ethernet2 | l3leaf | RE-AVD-Leaf1B | Ethernet8 |
| l2leaf | RE-AVD-L2Leaf2A | Ethernet1 | l3leaf | RE-AVD-Leaf2A | Ethernet7 |
| l2leaf | RE-AVD-L2Leaf2A | Ethernet2 | l3leaf | RE-AVD-Leaf2B | Ethernet7 |
| l2leaf | RE-AVD-L2Leaf2A | Ethernet3 | mlag_peer | RE-AVD-L2Leaf2B | Ethernet3 |
| l2leaf | RE-AVD-L2Leaf2A | Ethernet4 | mlag_peer | RE-AVD-L2Leaf2B | Ethernet4 |
| l2leaf | RE-AVD-L2Leaf2B | Ethernet1 | l3leaf | RE-AVD-Leaf2A | Ethernet8 |
| l2leaf | RE-AVD-L2Leaf2B | Ethernet2 | l3leaf | RE-AVD-Leaf2B | Ethernet8 |
| l3leaf | RE-AVD-Leaf1A | Ethernet1 | spine | RE-AVD-Spine1 | Ethernet1 |
| l3leaf | RE-AVD-Leaf1A | Ethernet2 | spine | RE-AVD-Spine2 | Ethernet1 |
| l3leaf | RE-AVD-Leaf1A | Ethernet3 | spine | RE-AVD-Spine3 | Ethernet1 |
| l3leaf | RE-AVD-Leaf1A | Ethernet4 | spine | RE-AVD-Spine4 | Ethernet1 |
| l3leaf | RE-AVD-Leaf1A | Ethernet5 | mlag_peer | RE-AVD-Leaf1B | Ethernet5 |
| l3leaf | RE-AVD-Leaf1A | Ethernet6 | mlag_peer | RE-AVD-Leaf1B | Ethernet6 |
| l3leaf | RE-AVD-Leaf1B | Ethernet1 | spine | RE-AVD-Spine1 | Ethernet2 |
| l3leaf | RE-AVD-Leaf1B | Ethernet2 | spine | RE-AVD-Spine2 | Ethernet2 |
| l3leaf | RE-AVD-Leaf1B | Ethernet3 | spine | RE-AVD-Spine3 | Ethernet2 |
| l3leaf | RE-AVD-Leaf1B | Ethernet4 | spine | RE-AVD-Spine4 | Ethernet2 |
| l3leaf | RE-AVD-Leaf2A | Ethernet1 | spine | RE-AVD-Spine1 | Ethernet3 |
| l3leaf | RE-AVD-Leaf2A | Ethernet2 | spine | RE-AVD-Spine2 | Ethernet3 |
| l3leaf | RE-AVD-Leaf2A | Ethernet3 | spine | RE-AVD-Spine3 | Ethernet3 |
| l3leaf | RE-AVD-Leaf2A | Ethernet4 | spine | RE-AVD-Spine4 | Ethernet3 |
| l3leaf | RE-AVD-Leaf2A | Ethernet5 | mlag_peer | RE-AVD-Leaf2B | Ethernet5 |
| l3leaf | RE-AVD-Leaf2A | Ethernet6 | mlag_peer | RE-AVD-Leaf2B | Ethernet6 |
| l3leaf | RE-AVD-Leaf2B | Ethernet1 | spine | RE-AVD-Spine1 | Ethernet4 |
| l3leaf | RE-AVD-Leaf2B | Ethernet2 | spine | RE-AVD-Spine2 | Ethernet4 |
| l3leaf | RE-AVD-Leaf2B | Ethernet3 | spine | RE-AVD-Spine3 | Ethernet4 |
| l3leaf | RE-AVD-Leaf2B | Ethernet4 | spine | RE-AVD-Spine4 | Ethernet4 |

## Fabric IP Allocation

### Fabric Point-To-Point Links

| Uplink IPv4 Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ---------------- | ------------------- | ------------------ | ------------------ |
| 192.168.0.0/23 | 512 | 48 | 9.38 % |

### Point-To-Point Links Node Allocation

| Node | Node Interface | Node IP Address | Peer Node | Peer Interface | Peer IP Address |
| ---- | -------------- | --------------- | --------- | -------------- | --------------- |
| RE-AVD-BrdrLeaf1A | Ethernet1 | 192.168.0.145/31 | RE-AVD-Spine1 | Ethernet5 | 192.168.0.144/31 |
| RE-AVD-BrdrLeaf1A | Ethernet2 | 192.168.0.147/31 | RE-AVD-Spine2 | Ethernet5 | 192.168.0.146/31 |
| RE-AVD-BrdrLeaf1A | Ethernet3 | 192.168.0.149/31 | RE-AVD-Spine3 | Ethernet5 | 192.168.0.148/31 |
| RE-AVD-BrdrLeaf1A | Ethernet4 | 192.168.0.151/31 | RE-AVD-Spine4 | Ethernet5 | 192.168.0.150/31 |
| RE-AVD-BrdrLeaf1B | Ethernet1 | 192.168.0.153/31 | RE-AVD-Spine1 | Ethernet6 | 192.168.0.152/31 |
| RE-AVD-BrdrLeaf1B | Ethernet2 | 192.168.0.155/31 | RE-AVD-Spine2 | Ethernet6 | 192.168.0.154/31 |
| RE-AVD-BrdrLeaf1B | Ethernet3 | 192.168.0.157/31 | RE-AVD-Spine3 | Ethernet6 | 192.168.0.156/31 |
| RE-AVD-BrdrLeaf1B | Ethernet4 | 192.168.0.159/31 | RE-AVD-Spine4 | Ethernet6 | 192.168.0.158/31 |
| RE-AVD-Leaf1A | Ethernet1 | 192.168.0.113/31 | RE-AVD-Spine1 | Ethernet1 | 192.168.0.112/31 |
| RE-AVD-Leaf1A | Ethernet2 | 192.168.0.115/31 | RE-AVD-Spine2 | Ethernet1 | 192.168.0.114/31 |
| RE-AVD-Leaf1A | Ethernet3 | 192.168.0.117/31 | RE-AVD-Spine3 | Ethernet1 | 192.168.0.116/31 |
| RE-AVD-Leaf1A | Ethernet4 | 192.168.0.119/31 | RE-AVD-Spine4 | Ethernet1 | 192.168.0.118/31 |
| RE-AVD-Leaf1B | Ethernet1 | 192.168.0.121/31 | RE-AVD-Spine1 | Ethernet2 | 192.168.0.120/31 |
| RE-AVD-Leaf1B | Ethernet2 | 192.168.0.123/31 | RE-AVD-Spine2 | Ethernet2 | 192.168.0.122/31 |
| RE-AVD-Leaf1B | Ethernet3 | 192.168.0.125/31 | RE-AVD-Spine3 | Ethernet2 | 192.168.0.124/31 |
| RE-AVD-Leaf1B | Ethernet4 | 192.168.0.127/31 | RE-AVD-Spine4 | Ethernet2 | 192.168.0.126/31 |
| RE-AVD-Leaf2A | Ethernet1 | 192.168.0.129/31 | RE-AVD-Spine1 | Ethernet3 | 192.168.0.128/31 |
| RE-AVD-Leaf2A | Ethernet2 | 192.168.0.131/31 | RE-AVD-Spine2 | Ethernet3 | 192.168.0.130/31 |
| RE-AVD-Leaf2A | Ethernet3 | 192.168.0.133/31 | RE-AVD-Spine3 | Ethernet3 | 192.168.0.132/31 |
| RE-AVD-Leaf2A | Ethernet4 | 192.168.0.135/31 | RE-AVD-Spine4 | Ethernet3 | 192.168.0.134/31 |
| RE-AVD-Leaf2B | Ethernet1 | 192.168.0.137/31 | RE-AVD-Spine1 | Ethernet4 | 192.168.0.136/31 |
| RE-AVD-Leaf2B | Ethernet2 | 192.168.0.139/31 | RE-AVD-Spine2 | Ethernet4 | 192.168.0.138/31 |
| RE-AVD-Leaf2B | Ethernet3 | 192.168.0.141/31 | RE-AVD-Spine3 | Ethernet4 | 192.168.0.140/31 |
| RE-AVD-Leaf2B | Ethernet4 | 192.168.0.143/31 | RE-AVD-Spine4 | Ethernet4 | 192.168.0.142/31 |

### Loopback Interfaces (BGP EVPN Peering)

| Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ------------- | ------------------- | ------------------ | ------------------ |
| 192.168.254.0/24 | 256 | 10 | 3.91 % |

### Loopback0 Interfaces Node Allocation

| POD | Node | Loopback0 |
| --- | ---- | --------- |
| RE | RE-AVD-BrdrLeaf1A | 192.168.254.21/32 |
| RE | RE-AVD-BrdrLeaf1B | 192.168.254.22/32 |
| RE | RE-AVD-Leaf1A | 192.168.254.17/32 |
| RE | RE-AVD-Leaf1B | 192.168.254.18/32 |
| RE | RE-AVD-Leaf2A | 192.168.254.19/32 |
| RE | RE-AVD-Leaf2B | 192.168.254.20/32 |
| RE | RE-AVD-Spine1 | 192.168.254.11/32 |
| RE | RE-AVD-Spine2 | 192.168.254.12/32 |
| RE | RE-AVD-Spine3 | 192.168.254.13/32 |
| RE | RE-AVD-Spine4 | 192.168.254.14/32 |

### VTEP Loopback VXLAN Tunnel Source Interfaces (VTEPs Only)

| VTEP Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| --------------------- | ------------------- | ------------------ | ------------------ |
| 192.168.253.0/24 | 256 | 6 | 2.35 % |

### VTEP Loopback Node allocation

| POD | Node | Loopback1 |
| --- | ---- | --------- |
| RE | RE-AVD-BrdrLeaf1A | 192.168.253.21/32 |
| RE | RE-AVD-BrdrLeaf1B | 192.168.253.21/32 |
| RE | RE-AVD-Leaf1A | 192.168.253.17/32 |
| RE | RE-AVD-Leaf1B | 192.168.253.17/32 |
| RE | RE-AVD-Leaf2A | 192.168.253.19/32 |
| RE | RE-AVD-Leaf2B | 192.168.253.19/32 |
