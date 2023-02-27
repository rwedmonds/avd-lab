# AVD_FABRIC

# Table of Contents

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

# Fabric Switches and Management IP

| POD | Type | Node | Management IP | Platform | Provisioned in CloudVision |
| --- | ---- | ---- | ------------- | -------- | -------------------------- |
| AVD_FABRIC | l3leaf | avd-test-Leaf1A | 192.168.255.15/24 | vEOS | Provisioned |
| AVD_FABRIC | l3leaf | avd-test-Leaf1B | 192.168.255.16/24 | vEOS | Provisioned |
| AVD_FABRIC | l3leaf | avd-test-Leaf2A | 192.168.255.17/24 | vEOS | Provisioned |
| AVD_FABRIC | l3leaf | avd-test-Leaf2B | 192.168.255.18/24 | vEOS | Provisioned |
| AVD_FABRIC | spine | avd-test-Spine1 | 192.168.255.11/24 | vEOS | Provisioned |
| AVD_FABRIC | spine | avd-test-Spine2 | 192.168.255.12/24 | vEOS | Provisioned |
| AVD_FABRIC | spine | avd-test-Spine3 | 192.168.255.13/24 | vEOS | Provisioned |
| AVD_FABRIC | spine | avd-test-Spine4 | 192.168.255.14/24 | vEOS | Provisioned |

> Provision status is based on Ansible inventory declaration and do not represent real status from CloudVision.

## Fabric Switches with inband Management IP
| POD | Type | Node | Management IP | Inband Interface |
| --- | ---- | ---- | ------------- | ---------------- |

# Fabric Topology

| Type | Node | Node Interface | Peer Type | Peer Node | Peer Interface |
| ---- | ---- | -------------- | --------- | ----------| -------------- |
| l3leaf | avd-test-Leaf1A | Ethernet1 | spine | avd-test-Spine1 | Ethernet1 |
| l3leaf | avd-test-Leaf1A | Ethernet2 | spine | avd-test-Spine2 | Ethernet1 |
| l3leaf | avd-test-Leaf1A | Ethernet3 | spine | avd-test-Spine3 | Ethernet1 |
| l3leaf | avd-test-Leaf1A | Ethernet4 | spine | avd-test-Spine4 | Ethernet1 |
| l3leaf | avd-test-Leaf1A | Ethernet5 | mlag_peer | avd-test-Leaf1B | Ethernet5 |
| l3leaf | avd-test-Leaf1B | Ethernet1 | spine | avd-test-Spine1 | Ethernet2 |
| l3leaf | avd-test-Leaf1B | Ethernet2 | spine | avd-test-Spine2 | Ethernet2 |
| l3leaf | avd-test-Leaf1B | Ethernet3 | spine | avd-test-Spine3 | Ethernet2 |
| l3leaf | avd-test-Leaf1B | Ethernet4 | spine | avd-test-Spine4 | Ethernet2 |
| l3leaf | avd-test-Leaf2A | Ethernet1 | spine | avd-test-Spine1 | Ethernet3 |
| l3leaf | avd-test-Leaf2A | Ethernet2 | spine | avd-test-Spine2 | Ethernet3 |
| l3leaf | avd-test-Leaf2A | Ethernet3 | spine | avd-test-Spine3 | Ethernet3 |
| l3leaf | avd-test-Leaf2A | Ethernet4 | spine | avd-test-Spine4 | Ethernet3 |
| l3leaf | avd-test-Leaf2A | Ethernet5 | mlag_peer | avd-test-Leaf2B | Ethernet5 |
| l3leaf | avd-test-Leaf2B | Ethernet1 | spine | avd-test-Spine1 | Ethernet4 |
| l3leaf | avd-test-Leaf2B | Ethernet2 | spine | avd-test-Spine2 | Ethernet4 |
| l3leaf | avd-test-Leaf2B | Ethernet3 | spine | avd-test-Spine3 | Ethernet4 |
| l3leaf | avd-test-Leaf2B | Ethernet4 | spine | avd-test-Spine4 | Ethernet4 |

# Fabric IP Allocation

## Fabric Point-To-Point Links

| Uplink IPv4 Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ---------------- | ------------------- | ------------------ | ------------------ |
| 192.168.3.0/24 | 256 | 32 | 12.5 % |

## Point-To-Point Links Node Allocation

| Node | Node Interface | Node IP Address | Peer Node | Peer Interface | Peer IP Address |
| ---- | -------------- | --------------- | --------- | -------------- | --------------- |
| avd-test-Leaf1A | Ethernet1 | 192.168.3.9/31 | avd-test-Spine1 | Ethernet1 | 192.168.3.8/31 |
| avd-test-Leaf1A | Ethernet2 | 192.168.3.11/31 | avd-test-Spine2 | Ethernet1 | 192.168.3.10/31 |
| avd-test-Leaf1A | Ethernet3 | 192.168.3.13/31 | avd-test-Spine3 | Ethernet1 | 192.168.3.12/31 |
| avd-test-Leaf1A | Ethernet4 | 192.168.3.15/31 | avd-test-Spine4 | Ethernet1 | 192.168.3.14/31 |
| avd-test-Leaf1B | Ethernet1 | 192.168.3.25/31 | avd-test-Spine1 | Ethernet2 | 192.168.3.24/31 |
| avd-test-Leaf1B | Ethernet2 | 192.168.3.27/31 | avd-test-Spine2 | Ethernet2 | 192.168.3.26/31 |
| avd-test-Leaf1B | Ethernet3 | 192.168.3.29/31 | avd-test-Spine3 | Ethernet2 | 192.168.3.28/31 |
| avd-test-Leaf1B | Ethernet4 | 192.168.3.31/31 | avd-test-Spine4 | Ethernet2 | 192.168.3.30/31 |
| avd-test-Leaf2A | Ethernet1 | 192.168.3.41/31 | avd-test-Spine1 | Ethernet3 | 192.168.3.40/31 |
| avd-test-Leaf2A | Ethernet2 | 192.168.3.43/31 | avd-test-Spine2 | Ethernet3 | 192.168.3.42/31 |
| avd-test-Leaf2A | Ethernet3 | 192.168.3.45/31 | avd-test-Spine3 | Ethernet3 | 192.168.3.44/31 |
| avd-test-Leaf2A | Ethernet4 | 192.168.3.47/31 | avd-test-Spine4 | Ethernet3 | 192.168.3.46/31 |
| avd-test-Leaf2B | Ethernet1 | 192.168.3.57/31 | avd-test-Spine1 | Ethernet4 | 192.168.3.56/31 |
| avd-test-Leaf2B | Ethernet2 | 192.168.3.59/31 | avd-test-Spine2 | Ethernet4 | 192.168.3.58/31 |
| avd-test-Leaf2B | Ethernet3 | 192.168.3.61/31 | avd-test-Spine3 | Ethernet4 | 192.168.3.60/31 |
| avd-test-Leaf2B | Ethernet4 | 192.168.3.63/31 | avd-test-Spine4 | Ethernet4 | 192.168.3.62/31 |

## Loopback Interfaces (BGP EVPN Peering)

| Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ------------- | ------------------- | ------------------ | ------------------ |
| 192.168.0.0/24 | 256 | 4 | 1.57 % |
| 192.168.100.0/24 | 256 | 4 | 1.57 % |

## Loopback0 Interfaces Node Allocation

| POD | Node | Loopback0 |
| --- | ---- | --------- |
| AVD_FABRIC | avd-test-Leaf1A | 192.168.0.1/32 |
| AVD_FABRIC | avd-test-Leaf1B | 192.168.0.2/32 |
| AVD_FABRIC | avd-test-Leaf2A | 192.168.0.3/32 |
| AVD_FABRIC | avd-test-Leaf2B | 192.168.0.4/32 |
| AVD_FABRIC | avd-test-Spine1 | 192.168.100.1/32 |
| AVD_FABRIC | avd-test-Spine2 | 192.168.100.2/32 |
| AVD_FABRIC | avd-test-Spine3 | 192.168.100.3/32 |
| AVD_FABRIC | avd-test-Spine4 | 192.168.100.4/32 |

## VTEP Loopback VXLAN Tunnel Source Interfaces (VTEPs Only)

| VTEP Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| --------------------- | ------------------- | ------------------ | ------------------ |
| 192.168.1.0/24 | 256 | 4 | 1.57 % |

## VTEP Loopback Node allocation

| POD | Node | Loopback1 |
| --- | ---- | --------- |
| AVD_FABRIC | avd-test-Leaf1A | 192.168.1.1/32 |
| AVD_FABRIC | avd-test-Leaf1B | 192.168.1.1/32 |
| AVD_FABRIC | avd-test-Leaf2A | 192.168.1.3/32 |
| AVD_FABRIC | avd-test-Leaf2B | 192.168.1.3/32 |
