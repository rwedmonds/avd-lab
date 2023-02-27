# avd-test-Leaf2B
# Table of Contents

- [Management](#management)
  - [Management Interfaces](#management-interfaces)
  - [DNS Domain](#dns-domain)
  - [Name Servers](#name-servers)
  - [Management API HTTP](#management-api-http)
- [Authentication](#authentication)
  - [Local Users](#local-users)
- [Monitoring](#monitoring)
  - [TerminAttr Daemon](#terminattr-daemon)
- [MLAG](#mlag)
  - [MLAG Summary](#mlag-summary)
  - [MLAG Device Configuration](#mlag-device-configuration)
- [Spanning Tree](#spanning-tree)
  - [Spanning Tree Summary](#spanning-tree-summary)
  - [Spanning Tree Device Configuration](#spanning-tree-device-configuration)
- [Internal VLAN Allocation Policy](#internal-vlan-allocation-policy)
  - [Internal VLAN Allocation Policy Summary](#internal-vlan-allocation-policy-summary)
  - [Internal VLAN Allocation Policy Configuration](#internal-vlan-allocation-policy-configuration)
- [VLANs](#vlans)
  - [VLANs Summary](#vlans-summary)
  - [VLANs Device Configuration](#vlans-device-configuration)
- [Interfaces](#interfaces)
  - [Ethernet Interfaces](#ethernet-interfaces)
  - [Port-Channel Interfaces](#port-channel-interfaces)
  - [Loopback Interfaces](#loopback-interfaces)
  - [VLAN Interfaces](#vlan-interfaces)
  - [VXLAN Interface](#vxlan-interface)
- [Routing](#routing)
  - [Service Routing Protocols Model](#service-routing-protocols-model)
  - [Virtual Router MAC Address](#virtual-router-mac-address)
  - [IP Routing](#ip-routing)
  - [IPv6 Routing](#ipv6-routing)
  - [Static Routes](#static-routes)
  - [Router BGP](#router-bgp)
- [BFD](#bfd)
  - [Router BFD](#router-bfd)
- [Multicast](#multicast)
  - [IP IGMP Snooping](#ip-igmp-snooping)
- [Filters](#filters)
  - [Prefix-lists](#prefix-lists)
  - [Route-maps](#route-maps)
- [ACL](#acl)
- [VRF Instances](#vrf-instances)
  - [VRF Instances Summary](#vrf-instances-summary)
  - [VRF Instances Device Configuration](#vrf-instances-device-configuration)
- [Virtual Source NAT](#virtual-source-nat)
  - [Virtual Source NAT Summary](#virtual-source-nat-summary)
  - [Virtual Source NAT Configuration](#virtual-source-nat-configuration)
- [Quality Of Service](#quality-of-service)

# Management

## Management Interfaces

### Management Interfaces Summary

#### IPv4

| Management Interface | description | Type | VRF | IP Address | Gateway |
| -------------------- | ----------- | ---- | --- | ---------- | ------- |
| Management1 | oob_management | oob | MGMT | 192.168.255.18/24 | 192.168.255.1 |

#### IPv6

| Management Interface | description | Type | VRF | IPv6 Address | IPv6 Gateway |
| -------------------- | ----------- | ---- | --- | ------------ | ------------ |
| Management1 | oob_management | oob | MGMT | -  | - |

### Management Interfaces Device Configuration

```eos
!
interface Management1
   description oob_management
   no shutdown
   vrf MGMT
   ip address 192.168.255.18/24
```

## DNS Domain

### DNS domain: slacker.eve

### DNS Domain Device Configuration

```eos
dns domain slacker.eve
!
```

## Name Servers

### Name Servers Summary

| Name Server | Source VRF |
| ----------- | ---------- |
| 192.168.2.1 | MGMT |
| 192.168.255.1 | MGMT |

### Name Servers Device Configuration

```eos
ip name-server vrf MGMT 192.168.2.1
ip name-server vrf MGMT 192.168.255.1
```

## Management API HTTP

### Management API HTTP Summary

| HTTP | HTTPS | Default Services |
| ---- | ----- | ---------------- |
| False | True | - |

### Management API VRF Access

| VRF Name | IPv4 ACL | IPv6 ACL |
| -------- | -------- | -------- |
| MGMT | - | - |

### Management API HTTP Configuration

```eos
!
management api http-commands
   protocol https
   no shutdown
   !
   vrf MGMT
      no shutdown
```

# Authentication

## Local Users

### Local Users Summary

| User | Privilege | Role |
| ---- | --------- | ---- |
| admin | 15 | network-admin |
| cvpadmin | 15 | network-admin |

### Local Users Device Configuration

```eos
!
username admin privilege 15 role network-admin secret sha512 $6$2YPH6yCQ.xAFxuUh$t0uUeTzX1VLj2xu4il.//BIzI46CNswZNdD..vs2N.jRim65PPA8BqrSoft.2h5duvcQ27XULKnwmEp6aRZHT.
username cvpadmin privilege 15 role network-admin secret sha512 $6$wh5/7CrF9CTrG0nk$RWaK9mq0OvSe1yRnDE6bkYNa6SRHte8Pt3pGa0fxTN0uKuF2TddOGOrkzdwsRul5DTYi1Sr7UYYXkbEuQClXl0
```

# Monitoring

## TerminAttr Daemon

### TerminAttr Daemon Summary

| CV Compression | CloudVision Servers | VRF | Authentication | Smash Excludes | Ingest Exclude | Bypass AAA |
| -------------- | ------------------- | --- | -------------- | -------------- | -------------- | ---------- |
| gzip | 192.168.2.137:9910 | MGMT | key, | ale,flexCounter,hardware,kni,pulse,strata | /Sysdb/cell/1/agent,/Sysdb/cell/2/agent | False |

### TerminAttr Daemon Device Configuration

```eos
!
daemon TerminAttr
   exec /usr/bin/TerminAttr -cvaddr=192.168.2.137:9910 -cvauth=key, -cvvrf=MGMT -smashexcludes=ale,flexCounter,hardware,kni,pulse,strata -ingestexclude=/Sysdb/cell/1/agent,/Sysdb/cell/2/agent -taillogs
   no shutdown
```

# MLAG

## MLAG Summary

| Domain-id | Local-interface | Peer-address | Peer-link |
| --------- | --------------- | ------------ | --------- |
| pod1 | Vlan4094 | 192.168.255.4 | Port-Channel5 |

Dual primary detection is disabled.

## MLAG Device Configuration

```eos
!
mlag configuration
   domain-id pod1
   local-interface Vlan4094
   peer-address 192.168.255.4
   peer-link Port-Channel5
   reload-delay mlag 300
   reload-delay non-mlag 330
```

# Spanning Tree

## Spanning Tree Summary

STP mode: **mstp**

### MSTP Instance and Priority

| Instance(s) | Priority |
| -------- | -------- |
| 0 | 16384 |

### Global Spanning-Tree Settings

- Spanning Tree disabled for VLANs: **4093-4094**

## Spanning Tree Device Configuration

```eos
!
spanning-tree mode mstp
no spanning-tree vlan-id 4093-4094
spanning-tree mst 0 priority 16384
```

# Internal VLAN Allocation Policy

## Internal VLAN Allocation Policy Summary

| Policy Allocation | Range Beginning | Range Ending |
| ------------------| --------------- | ------------ |
| ascending | 1006 | 1199 |

## Internal VLAN Allocation Policy Configuration

```eos
!
vlan internal order ascending range 1006 1199
```

# VLANs

## VLANs Summary

| VLAN ID | Name | Trunk Groups |
| ------- | ---- | ------------ |
| 3000 | MLAG_iBGP_prod | LEAF_PEER_L3 |
| 3001 | MLAG_iBGP_pdmz | LEAF_PEER_L3 |
| 3002 | MLAG_iBGP_nonprod | LEAF_PEER_L3 |
| 3003 | MLAG_iBGP_npdmz | LEAF_PEER_L3 |
| 3300 | DMZ_Non_Prod_VLAN | - |
| 4093 | LEAF_PEER_L3 | LEAF_PEER_L3 |
| 4094 | MLAG_PEER | MLAG |

## VLANs Device Configuration

```eos
!
vlan 3000
   name MLAG_iBGP_prod
   trunk group LEAF_PEER_L3
!
vlan 3001
   name MLAG_iBGP_pdmz
   trunk group LEAF_PEER_L3
!
vlan 3002
   name MLAG_iBGP_nonprod
   trunk group LEAF_PEER_L3
!
vlan 3003
   name MLAG_iBGP_npdmz
   trunk group LEAF_PEER_L3
!
vlan 3300
   name DMZ_Non_Prod_VLAN
!
vlan 4093
   name LEAF_PEER_L3
   trunk group LEAF_PEER_L3
!
vlan 4094
   name MLAG_PEER
   trunk group MLAG
```

# Interfaces

## Ethernet Interfaces

### Ethernet Interfaces Summary

#### L2

| Interface | Description | Mode | VLANs | Native VLAN | Trunk Group | Channel-Group |
| --------- | ----------- | ---- | ----- | ----------- | ----------- | ------------- |
| Ethernet5 | MLAG_PEER_avd-test-Leaf2A_Ethernet5 | *trunk | *2-4094 | *- | *['LEAF_PEER_L3', 'MLAG'] | 5 |
| Ethernet7 | ntx02_ntx01_to_leaf2b | *access | *602 | *- | *- | 7 |

*Inherited from Port-Channel Interface

#### IPv4

| Interface | Description | Type | Channel Group | IP Address | VRF |  MTU | Shutdown | ACL In | ACL Out |
| --------- | ----------- | -----| ------------- | ---------- | ----| ---- | -------- | ------ | ------- |
| Ethernet1 | P2P_LINK_TO_AVD-TEST-SPINE1_Ethernet4 | routed | - | 192.168.3.57/31 | default | 9214 | false | - | - |
| Ethernet2 | P2P_LINK_TO_AVD-TEST-SPINE2_Ethernet4 | routed | - | 192.168.3.59/31 | default | 9214 | false | - | - |
| Ethernet3 | P2P_LINK_TO_AVD-TEST-SPINE3_Ethernet4 | routed | - | 192.168.3.61/31 | default | 9214 | false | - | - |
| Ethernet4 | P2P_LINK_TO_AVD-TEST-SPINE4_Ethernet4 | routed | - | 192.168.3.63/31 | default | 9214 | false | - | - |

### Ethernet Interfaces Device Configuration

```eos
!
interface Ethernet1
   description P2P_LINK_TO_AVD-TEST-SPINE1_Ethernet4
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.3.57/31
!
interface Ethernet2
   description P2P_LINK_TO_AVD-TEST-SPINE2_Ethernet4
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.3.59/31
!
interface Ethernet3
   description P2P_LINK_TO_AVD-TEST-SPINE3_Ethernet4
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.3.61/31
!
interface Ethernet4
   description P2P_LINK_TO_AVD-TEST-SPINE4_Ethernet4
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.3.63/31
!
interface Ethernet5
   description MLAG_PEER_avd-test-Leaf2A_Ethernet5
   no shutdown
   channel-group 5 mode active
!
interface Ethernet7
   description ntx02_ntx01_to_leaf2b
   no shutdown
   channel-group 7 mode active
```

## Port-Channel Interfaces

### Port-Channel Interfaces Summary

#### L2

| Interface | Description | Type | Mode | VLANs | Native VLAN | Trunk Group | LACP Fallback Timeout | LACP Fallback Mode | MLAG ID | EVPN ESI |
| --------- | ----------- | ---- | ---- | ----- | ----------- | ------------| --------------------- | ------------------ | ------- | -------- |
| Port-Channel5 | MLAG_PEER_avd-test-Leaf2A_Po5 | switched | trunk | 2-4094 | - | ['LEAF_PEER_L3', 'MLAG'] | - | - | - | - |
| Port-Channel7 | ntx02_ntx01_to_leaf2b | switched | access | 602 | - | - | - | - | 7 | - |

### Port-Channel Interfaces Device Configuration

```eos
!
interface Port-Channel5
   description MLAG_PEER_avd-test-Leaf2A_Po5
   no shutdown
   switchport
   switchport trunk allowed vlan 2-4094
   switchport mode trunk
   switchport trunk group LEAF_PEER_L3
   switchport trunk group MLAG
!
interface Port-Channel7
   description ntx02_ntx01_to_leaf2b
   no shutdown
   switchport
   switchport access vlan 602
   mlag 7
```

## Loopback Interfaces

### Loopback Interfaces Summary

#### IPv4

| Interface | Description | VRF | IP Address |
| --------- | ----------- | --- | ---------- |
| Loopback0 | EVPN_Overlay_Peering | default | 192.168.0.4/32 |
| Loopback1 | VTEP_VXLAN_Tunnel_Source | default | 192.168.1.3/32 |
| Loopback100 | prod_VTEP_DIAGNOSTICS | prod | 10.1.255.4/32 |
| Loopback300 | nonprod_VTEP_DIAGNOSTICS | nonprod | 10.3.255.4/32 |
| Loopback400 | pdmz_VTEP_DIAGNOSTICS | pdmz | 10.4.255.4/32 |
| Loopback500 | npdmz_VTEP_DIAGNOSTICS | npdmz | 10.5.255.4/32 |

#### IPv6

| Interface | Description | VRF | IPv6 Address |
| --------- | ----------- | --- | ------------ |
| Loopback0 | EVPN_Overlay_Peering | default | - |
| Loopback1 | VTEP_VXLAN_Tunnel_Source | default | - |
| Loopback100 | prod_VTEP_DIAGNOSTICS | prod | - |
| Loopback300 | nonprod_VTEP_DIAGNOSTICS | nonprod | - |
| Loopback400 | pdmz_VTEP_DIAGNOSTICS | pdmz | - |
| Loopback500 | npdmz_VTEP_DIAGNOSTICS | npdmz | - |


### Loopback Interfaces Device Configuration

```eos
!
interface Loopback0
   description EVPN_Overlay_Peering
   no shutdown
   ip address 192.168.0.4/32
!
interface Loopback1
   description VTEP_VXLAN_Tunnel_Source
   no shutdown
   ip address 192.168.1.3/32
!
interface Loopback100
   description prod_VTEP_DIAGNOSTICS
   no shutdown
   vrf prod
   ip address 10.1.255.4/32
!
interface Loopback300
   description nonprod_VTEP_DIAGNOSTICS
   no shutdown
   vrf nonprod
   ip address 10.3.255.4/32
!
interface Loopback400
   description pdmz_VTEP_DIAGNOSTICS
   no shutdown
   vrf pdmz
   ip address 10.4.255.4/32
!
interface Loopback500
   description npdmz_VTEP_DIAGNOSTICS
   no shutdown
   vrf npdmz
   ip address 10.5.255.4/32
```

## VLAN Interfaces

### VLAN Interfaces Summary

| Interface | Description | VRF |  MTU | Shutdown |
| --------- | ----------- | --- | ---- | -------- |
| Vlan3000 | MLAG_PEER_L3_iBGP: vrf prod | prod | 9214 | false |
| Vlan3001 | MLAG_PEER_L3_iBGP: vrf pdmz | pdmz | 9214 | false |
| Vlan3002 | MLAG_PEER_L3_iBGP: vrf nonprod | nonprod | 9214 | false |
| Vlan3003 | MLAG_PEER_L3_iBGP: vrf npdmz | npdmz | 9214 | false |
| Vlan3300 | DMZ_Non_Prod_VLAN | prod | - | false |
| Vlan4093 | MLAG_PEER_L3_PEERING | default | 9214 | false |
| Vlan4094 | MLAG_PEER | default | 9214 | false |

#### IPv4

| Interface | VRF | IP Address | IP Address Virtual | IP Router Virtual Address | VRRP | ACL In | ACL Out |
| --------- | --- | ---------- | ------------------ | ------------------------- | ---- | ------ | ------- |
| Vlan3000 |  prod  |  192.168.254.5/31  |  -  |  -  |  -  |  -  |  -  |
| Vlan3001 |  pdmz  |  192.168.254.5/31  |  -  |  -  |  -  |  -  |  -  |
| Vlan3002 |  nonprod  |  192.168.254.5/31  |  -  |  -  |  -  |  -  |  -  |
| Vlan3003 |  npdmz  |  192.168.254.5/31  |  -  |  -  |  -  |  -  |  -  |
| Vlan3300 |  prod  |  -  |  10.5.0.1/24  |  -  |  -  |  -  |  -  |
| Vlan4093 |  default  |  192.168.254.5/31  |  -  |  -  |  -  |  -  |  -  |
| Vlan4094 |  default  |  192.168.255.5/31  |  -  |  -  |  -  |  -  |  -  |

### VLAN Interfaces Device Configuration

```eos
!
interface Vlan3000
   description MLAG_PEER_L3_iBGP: vrf prod
   no shutdown
   mtu 9214
   vrf prod
   ip address 192.168.254.5/31
!
interface Vlan3001
   description MLAG_PEER_L3_iBGP: vrf pdmz
   no shutdown
   mtu 9214
   vrf pdmz
   ip address 192.168.254.5/31
!
interface Vlan3002
   description MLAG_PEER_L3_iBGP: vrf nonprod
   no shutdown
   mtu 9214
   vrf nonprod
   ip address 192.168.254.5/31
!
interface Vlan3003
   description MLAG_PEER_L3_iBGP: vrf npdmz
   no shutdown
   mtu 9214
   vrf npdmz
   ip address 192.168.254.5/31
!
interface Vlan3300
   description DMZ_Non_Prod_VLAN
   no shutdown
   vrf prod
   ip address virtual 10.5.0.1/24
!
interface Vlan4093
   description MLAG_PEER_L3_PEERING
   no shutdown
   mtu 9214
   ip address 192.168.254.5/31
!
interface Vlan4094
   description MLAG_PEER
   no shutdown
   mtu 9214
   no autostate
   ip address 192.168.255.5/31
```

## VXLAN Interface

### VXLAN Interface Summary

| Setting | Value |
| ------- | ----- |
| Source Interface | Loopback1 |
| UDP port | 4789 |
| EVPN MLAG Shared Router MAC | mlag-system-id |

#### VLAN to VNI, Flood List and Multicast Group Mappings

| VLAN | VNI | Flood List | Multicast Group |
| ---- | --- | ---------- | --------------- |
| 3300 | 23300 | - | - |

#### VRF to VNI and Multicast Group Mappings

| VRF | VNI | Multicast Group |
| ---- | --- | --------------- |
| nonprod | 3 | - |
| npdmz | 4 | - |
| pdmz | 2 | - |
| prod | 1 | - |

### VXLAN Interface Device Configuration

```eos
!
interface Vxlan1
   description avd-test-Leaf2B_VTEP
   vxlan source-interface Loopback1
   vxlan virtual-router encapsulation mac-address mlag-system-id
   vxlan udp-port 4789
   vxlan vlan 3300 vni 23300
   vxlan vrf nonprod vni 3
   vxlan vrf npdmz vni 4
   vxlan vrf pdmz vni 2
   vxlan vrf prod vni 1
```

# Routing
## Service Routing Protocols Model

Multi agent routing protocol model enabled

```eos
!
service routing protocols model multi-agent
```

## Virtual Router MAC Address

### Virtual Router MAC Address Summary

#### Virtual Router MAC Address: 00:1c:73:00:dc:01

### Virtual Router MAC Address Configuration

```eos
!
ip virtual-router mac-address 00:1c:73:00:dc:01
```

## IP Routing

### IP Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | true |
| MGMT | false |
| nonprod | true |
| npdmz | true |
| pdmz | true |
| prod | true |

### IP Routing Device Configuration

```eos
!
ip routing
no ip routing vrf MGMT
ip routing vrf nonprod
ip routing vrf npdmz
ip routing vrf pdmz
ip routing vrf prod
```
## IPv6 Routing

### IPv6 Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | false |
| MGMT | false |
| nonprod | false |
| npdmz | false |
| pdmz | false |
| prod | false |

## Static Routes

### Static Routes Summary

| VRF | Destination Prefix | Next Hop IP             | Exit interface      | Administrative Distance       | Tag               | Route Name                    | Metric         |
| --- | ------------------ | ----------------------- | ------------------- | ----------------------------- | ----------------- | ----------------------------- | -------------- |
| MGMT | 0.0.0.0/0 | 192.168.255.1 | - | 1 | - | - | - |

### Static Routes Device Configuration

```eos
!
ip route vrf MGMT 0.0.0.0/0 192.168.255.1
```

## Router BGP

### Router BGP Summary

| BGP AS | Router ID |
| ------ | --------- |
| 65002|  192.168.0.4 |

| BGP Tuning |
| ---------- |
| maximum-paths 4 ecmp 4 |

### Router BGP Peer Groups

#### EVPN-OVERLAY-PEERS

| Settings | Value |
| -------- | ----- |
| Address Family | evpn |
| Source | Loopback0 |
| BFD | True |
| Ebgp multihop | 3 |
| Send community | all |
| Maximum routes | 0 (no limit) |

#### IPv4-UNDERLAY-PEERS

| Settings | Value |
| -------- | ----- |
| Address Family | ipv4 |
| Send community | all |
| Maximum routes | 12000 |

#### MLAG-IPv4-UNDERLAY-PEER

| Settings | Value |
| -------- | ----- |
| Address Family | ipv4 |
| Remote AS | 65002 |
| Next-hop self | True |
| Send community | all |
| Maximum routes | 12000 |

### BGP Neighbors

| Neighbor | Remote AS | VRF | Shutdown | Send-community | Maximum-routes | Allowas-in | BFD | RIB Pre-Policy Retain |
| -------- | --------- | --- | -------- | -------------- | -------------- | ---------- | --- | --------------------- |
| 192.168.3.48 | 65100 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - |
| 192.168.3.50 | 65100 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - |
| 192.168.3.52 | 65100 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - |
| 192.168.3.54 | 65100 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - |
| 192.168.3.56 | 65100 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - |
| 192.168.3.58 | 65100 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - |
| 192.168.3.60 | 65100 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - |
| 192.168.3.62 | 65100 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - |
| 192.168.100.1 | 65100 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - |
| 192.168.100.2 | 65100 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - |
| 192.168.100.3 | 65100 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - |
| 192.168.100.4 | 65100 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - |
| 192.168.254.4 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | default | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - |
| 192.168.254.4 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | nonprod | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - |
| 192.168.254.4 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | npdmz | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - |
| 192.168.254.4 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | pdmz | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - |
| 192.168.254.4 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | prod | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - |

### Router BGP EVPN Address Family

#### EVPN Peer Groups

| Peer Group | Activate |
| ---------- | -------- |
| EVPN-OVERLAY-PEERS | True |

### Router BGP VLAN Aware Bundles

| VLAN Aware Bundle | Route-Distinguisher | Both Route-Target | Import Route Target | Export Route-Target | Redistribute | VLANs |
| ----------------- | ------------------- | ----------------- | ------------------- | ------------------- | ------------ | ----- |
| nonprod | 192.168.0.4:3 | 3:3 | - | - | learned | 3300 |
| npdmz | 192.168.0.4:4 | 4:4 | - | - | learned | 3300 |
| pdmz | 192.168.0.4:2 | 2:2 | - | - | learned | 3300 |
| prod | 192.168.0.4:1 | 1:1 | - | - | learned | 3300 |

### Router BGP VRFs

| VRF | Route-Distinguisher | Redistribute |
| --- | ------------------- | ------------ |
| nonprod | 192.168.0.4:3 | connected |
| npdmz | 192.168.0.4:4 | connected |
| pdmz | 192.168.0.4:2 | connected |
| prod | 192.168.0.4:1 | connected |

### Router BGP Device Configuration

```eos
!
router bgp 65002
   router-id 192.168.0.4
   maximum-paths 4 ecmp 4
   neighbor EVPN-OVERLAY-PEERS peer group
   neighbor EVPN-OVERLAY-PEERS update-source Loopback0
   neighbor EVPN-OVERLAY-PEERS bfd
   neighbor EVPN-OVERLAY-PEERS ebgp-multihop 3
   neighbor EVPN-OVERLAY-PEERS password 7 AQQvKeimxJu+uGQ/yYvv9w==
   neighbor EVPN-OVERLAY-PEERS send-community
   neighbor EVPN-OVERLAY-PEERS maximum-routes 0
   neighbor IPv4-UNDERLAY-PEERS peer group
   neighbor IPv4-UNDERLAY-PEERS password 7 AQQvKeimxJu+uGQ/yYvv9w==
   neighbor IPv4-UNDERLAY-PEERS send-community
   neighbor IPv4-UNDERLAY-PEERS maximum-routes 12000
   neighbor MLAG-IPv4-UNDERLAY-PEER peer group
   neighbor MLAG-IPv4-UNDERLAY-PEER remote-as 65002
   neighbor MLAG-IPv4-UNDERLAY-PEER next-hop-self
   neighbor MLAG-IPv4-UNDERLAY-PEER description avd-test-Leaf2A
   neighbor MLAG-IPv4-UNDERLAY-PEER password 7 AQQvKeimxJu+uGQ/yYvv9w==
   neighbor MLAG-IPv4-UNDERLAY-PEER send-community
   neighbor MLAG-IPv4-UNDERLAY-PEER maximum-routes 12000
   neighbor MLAG-IPv4-UNDERLAY-PEER route-map RM-MLAG-PEER-IN in
   neighbor 192.168.3.48 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.3.48 remote-as 65100
   neighbor 192.168.3.48 description avd-test-Spine1_Ethernet4
   neighbor 192.168.3.50 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.3.50 remote-as 65100
   neighbor 192.168.3.50 description avd-test-Spine2_Ethernet4
   neighbor 192.168.3.52 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.3.52 remote-as 65100
   neighbor 192.168.3.52 description avd-test-Spine3_Ethernet4
   neighbor 192.168.3.54 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.3.54 remote-as 65100
   neighbor 192.168.3.54 description avd-test-Spine4_Ethernet4
   neighbor 192.168.3.56 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.3.56 remote-as 65100
   neighbor 192.168.3.56 description avd-test-Spine1_Ethernet4
   neighbor 192.168.3.58 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.3.58 remote-as 65100
   neighbor 192.168.3.58 description avd-test-Spine2_Ethernet4
   neighbor 192.168.3.60 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.3.60 remote-as 65100
   neighbor 192.168.3.60 description avd-test-Spine3_Ethernet4
   neighbor 192.168.3.62 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.3.62 remote-as 65100
   neighbor 192.168.3.62 description avd-test-Spine4_Ethernet4
   neighbor 192.168.100.1 peer group EVPN-OVERLAY-PEERS
   neighbor 192.168.100.1 remote-as 65100
   neighbor 192.168.100.1 description avd-test-Spine1
   neighbor 192.168.100.2 peer group EVPN-OVERLAY-PEERS
   neighbor 192.168.100.2 remote-as 65100
   neighbor 192.168.100.2 description avd-test-Spine2
   neighbor 192.168.100.3 peer group EVPN-OVERLAY-PEERS
   neighbor 192.168.100.3 remote-as 65100
   neighbor 192.168.100.3 description avd-test-Spine3
   neighbor 192.168.100.4 peer group EVPN-OVERLAY-PEERS
   neighbor 192.168.100.4 remote-as 65100
   neighbor 192.168.100.4 description avd-test-Spine4
   neighbor 192.168.254.4 peer group MLAG-IPv4-UNDERLAY-PEER
   neighbor 192.168.254.4 description avd-test-Leaf2A
   redistribute connected route-map RM-CONN-2-BGP
   !
   vlan-aware-bundle nonprod
      rd 192.168.0.4:3
      route-target both 3:3
      redistribute learned
      vlan 3300
   !
   vlan-aware-bundle npdmz
      rd 192.168.0.4:4
      route-target both 4:4
      redistribute learned
      vlan 3300
   !
   vlan-aware-bundle pdmz
      rd 192.168.0.4:2
      route-target both 2:2
      redistribute learned
      vlan 3300
   !
   vlan-aware-bundle prod
      rd 192.168.0.4:1
      route-target both 1:1
      redistribute learned
      vlan 3300
   !
   address-family evpn
      neighbor EVPN-OVERLAY-PEERS activate
   !
   address-family ipv4
      no neighbor EVPN-OVERLAY-PEERS activate
      neighbor IPv4-UNDERLAY-PEERS activate
      neighbor MLAG-IPv4-UNDERLAY-PEER activate
   !
   vrf nonprod
      rd 192.168.0.4:3
      route-target import evpn 3:3
      route-target export evpn 3:3
      router-id 192.168.0.4
      neighbor 192.168.254.4 peer group MLAG-IPv4-UNDERLAY-PEER
      redistribute connected
   !
   vrf npdmz
      rd 192.168.0.4:4
      route-target import evpn 4:4
      route-target export evpn 4:4
      router-id 192.168.0.4
      neighbor 192.168.254.4 peer group MLAG-IPv4-UNDERLAY-PEER
      redistribute connected
   !
   vrf pdmz
      rd 192.168.0.4:2
      route-target import evpn 2:2
      route-target export evpn 2:2
      router-id 192.168.0.4
      neighbor 192.168.254.4 peer group MLAG-IPv4-UNDERLAY-PEER
      redistribute connected
   !
   vrf prod
      rd 192.168.0.4:1
      route-target import evpn 1:1
      route-target export evpn 1:1
      router-id 192.168.0.4
      neighbor 192.168.254.4 peer group MLAG-IPv4-UNDERLAY-PEER
      redistribute connected
```

# BFD

## Router BFD

### Router BFD Multihop Summary

| Interval | Minimum RX | Multiplier |
| -------- | ---------- | ---------- |
| 300 | 300 | 3 |

### Router BFD Device Configuration

```eos
!
router bfd
   multihop interval 300 min-rx 300 multiplier 3
```

# Multicast

## IP IGMP Snooping

### IP IGMP Snooping Summary

| IGMP Snooping | Fast Leave | Interface Restart Query | Proxy | Restart Query Interval | Robustness Variable |
| ------------- | ---------- | ----------------------- | ----- | ---------------------- | ------------------- |
| Enabled | - | - | - | - | - |

### IP IGMP Snooping Device Configuration

```eos
```

# Filters

## Prefix-lists

### Prefix-lists Summary

#### PL-LOOPBACKS-EVPN-OVERLAY

| Sequence | Action |
| -------- | ------ |
| 10 | permit 192.168.0.0/24 eq 32 |
| 20 | permit 192.168.1.0/24 eq 32 |

### Prefix-lists Device Configuration

```eos
!
ip prefix-list PL-LOOPBACKS-EVPN-OVERLAY
   seq 10 permit 192.168.0.0/24 eq 32
   seq 20 permit 192.168.1.0/24 eq 32
```

## Route-maps

### Route-maps Summary

#### RM-CONN-2-BGP

| Sequence | Type | Match and/or Set |
| -------- | ---- | ---------------- |
| 10 | permit | match ip address prefix-list PL-LOOPBACKS-EVPN-OVERLAY |

#### RM-MLAG-PEER-IN

| Sequence | Type | Match and/or Set |
| -------- | ---- | ---------------- |
| 10 | permit | set origin incomplete |

### Route-maps Device Configuration

```eos
!
route-map RM-CONN-2-BGP permit 10
   match ip address prefix-list PL-LOOPBACKS-EVPN-OVERLAY
!
route-map RM-MLAG-PEER-IN permit 10
   description Make routes learned over MLAG Peer-link less preferred on spines to ensure optimal routing
   set origin incomplete
```

# ACL

# VRF Instances

## VRF Instances Summary

| VRF Name | IP Routing |
| -------- | ---------- |
| MGMT | disabled |
| nonprod | enabled |
| npdmz | enabled |
| pdmz | enabled |
| prod | enabled |

## VRF Instances Device Configuration

```eos
!
vrf instance MGMT
!
vrf instance nonprod
!
vrf instance npdmz
!
vrf instance pdmz
!
vrf instance prod
```

# Virtual Source NAT

## Virtual Source NAT Summary

| Source NAT VRF | Source NAT IP Address |
| -------------- | --------------------- |
| nonprod | 10.3.255.4 |
| npdmz | 10.5.255.4 |
| pdmz | 10.4.255.4 |
| prod | 10.1.255.4 |

## Virtual Source NAT Configuration

```eos
!
ip address virtual source-nat vrf nonprod address 10.3.255.4
ip address virtual source-nat vrf npdmz address 10.5.255.4
ip address virtual source-nat vrf pdmz address 10.4.255.4
ip address virtual source-nat vrf prod address 10.1.255.4
```

# Quality Of Service
