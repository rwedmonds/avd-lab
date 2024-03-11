# RE-AVD-BrdrLeaf1A

## Table of Contents

- [Management](#management)
  - [Management Interfaces](#management-interfaces)
  - [DNS Domain](#dns-domain)
  - [IP Name Servers](#ip-name-servers)
  - [Clock Settings](#clock-settings)
  - [NTP](#ntp)
  - [Management API HTTP](#management-api-http)
- [Authentication](#authentication)
  - [Local Users](#local-users)
  - [Enable Password](#enable-password)
  - [RADIUS Server](#radius-server)
  - [IP RADIUS Source Interfaces](#ip-radius-source-interfaces)
  - [AAA Server Groups](#aaa-server-groups)
  - [AAA Authentication](#aaa-authentication)
  - [AAA Authorization](#aaa-authorization)
  - [AAA Accounting](#aaa-accounting)
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
  - [Internal VLAN Allocation Policy Device Configuration](#internal-vlan-allocation-policy-device-configuration)
- [VLANs](#vlans)
  - [VLANs Summary](#vlans-summary)
  - [VLANs Device Configuration](#vlans-device-configuration)
- [Interfaces](#interfaces)
  - [Interface Defaults](#interface-defaults)
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
  - [Router General](#router-general)
  - [Router BGP](#router-bgp)
- [BFD](#bfd)
  - [Router BFD](#router-bfd)
- [Multicast](#multicast)
  - [IP IGMP Snooping](#ip-igmp-snooping)
- [Filters](#filters)
  - [Prefix-lists](#prefix-lists)
  - [Route-maps](#route-maps)
- [VRF Instances](#vrf-instances)
  - [VRF Instances Summary](#vrf-instances-summary)
  - [VRF Instances Device Configuration](#vrf-instances-device-configuration)
- [Virtual Source NAT](#virtual-source-nat)
  - [Virtual Source NAT Summary](#virtual-source-nat-summary)
  - [Virtual Source NAT Configuration](#virtual-source-nat-configuration)
- [EOS CLI Device Configuration](#eos-cli-device-configuration)

## Management

### Management Interfaces

#### Management Interfaces Summary

##### IPv4

| Management Interface | Description | Type | VRF | IP Address | Gateway |
| -------------------- | ----------- | ---- | --- | ---------- | ------- |
| Management1 | oob_management | oob | MGMT | 192.168.255.19/24 | - |

##### IPv6

| Management Interface | Description | Type | VRF | IPv6 Address | IPv6 Gateway |
| -------------------- | ----------- | ---- | --- | ------------ | ------------ |
| Management1 | oob_management | oob | MGMT | - | - |

#### Management Interfaces Device Configuration

```eos
!
interface Management1
   description oob_management
   no shutdown
   vrf MGMT
   ip address 192.168.255.19/24
```

### DNS Domain

DNS domain: slacker.net

#### DNS Domain Device Configuration

```eos
dns domain slacker.net
!
```

### IP Name Servers

#### IP Name Servers Summary

| Name Server | VRF | Priority |
| ----------- | --- | -------- |
| 192.168.255.1 | MGMT | - |

#### IP Name Servers Device Configuration

```eos
ip name-server vrf MGMT 192.168.255.1
```

### Clock Settings

#### Clock Timezone Settings

Clock Timezone is set to **US/Central**.

#### Clock Device Configuration

```eos
!
clock timezone US/Central
```

### NTP

#### NTP Summary

##### NTP Local Interface

| Interface | VRF |
| --------- | --- |
| Management1 | MGMT |

##### NTP Servers

| Server | VRF | Preferred | Burst | iBurst | Version | Min Poll | Max Poll | Local-interface | Key |
| ------ | --- | --------- | ----- | ------ | ------- | -------- | -------- | --------------- | --- |
| 0.fr.pool.ntp.org | MGMT | True | - | - | - | - | - | - | - |
| 1.fr.pool.ntp.org | MGMT | - | - | - | - | - | - | - | - |

#### NTP Device Configuration

```eos
!
ntp local-interface vrf MGMT Management1
ntp server vrf MGMT 0.fr.pool.ntp.org prefer
ntp server vrf MGMT 1.fr.pool.ntp.org
```

### Management API HTTP

#### Management API HTTP Summary

| HTTP | HTTPS | Default Services |
| ---- | ----- | ---------------- |
| False | True | - |

#### Management API VRF Access

| VRF Name | IPv4 ACL | IPv6 ACL |
| -------- | -------- | -------- |
| MGMT | - | - |

#### Management API HTTP Device Configuration

```eos
!
management api http-commands
   protocol https
   no shutdown
   !
   vrf MGMT
      no shutdown
```

## Authentication

### Local Users

#### Local Users Summary

| User | Privilege | Role | Disabled | Shell |
| ---- | --------- | ---- | -------- | ----- |
| admin | 15 | network-admin | False | - |
| ansible | 15 | network-admin | False | - |
| cvpadmin | 15 | network-admin | False | - |
| robert | 15 | network-admin | False | - |

#### Local Users Device Configuration

```eos
!
username admin privilege 15 role network-admin secret sha512 <removed>
username ansible privilege 15 role network-admin secret sha512 <removed>
username cvpadmin privilege 15 role network-admin secret sha512 <removed>
username robert privilege 15 role network-admin nopassword
username robert ssh-key ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIA/FAQMSaka0eojd51yDc+Uf59FvJdewt2SJp1mU4yf2 redmonds@redmonds
```

### Enable Password

sha512 encrypted enable password is configured

#### Enable Password Device Configuration

```eos
!
enable password sha512 <removed>
!
```

### RADIUS Server

#### RADIUS Server Hosts

| VRF | RADIUS Servers | Timeout | Retransmit |
| --- | -------------- | ------- | ---------- |
| MGMT | jumpbox.slacker.net | - | - |

#### RADIUS Server Device Configuration

```eos
!
radius-server host jumpbox.slacker.net vrf MGMT key 7 <removed>
```

### IP RADIUS Source Interfaces

#### IP RADIUS Source Interfaces

| VRF | Source Interface Name |
| --- | --------------- |
| MGMT | Management1 |

#### IP SOURCE Source Interfaces Device Configuration

```eos
!
ip radius vrf MGMT source-interface Management1
```

### AAA Server Groups

#### AAA Server Groups Summary

| Server Group Name | Type  | VRF | IP address |
| ------------------| ----- | --- | ---------- |
| FreeRadius | radius | MGMT | jumpbox.slacker.net |

#### AAA Server Groups Device Configuration

```eos
!
aaa group server radius FreeRadius
   server jumpbox.slacker.net vrf MGMT
```

### AAA Authentication

#### AAA Authentication Summary

| Type | Sub-type | User Stores |
| ---- | -------- | ---------- |
| Login | default | group FreeRadius local |

#### AAA Authentication Device Configuration

```eos
aaa authentication login default group FreeRadius local
aaa authentication enable default none
!
```

### AAA Authorization

#### AAA Authorization Summary

| Type | User Stores |
| ---- | ----------- |
| Exec | local group FreeRadius |

Authorization for configuration commands is disabled.

#### AAA Authorization Device Configuration

```eos
aaa authorization exec default local group FreeRadius
no aaa authorization config-commands
!
```

### AAA Accounting

#### AAA Accounting Summary

| Type | Commands | Record type | Group | Logging |
| ---- | -------- | ----------- | ----- | ------- |
| Commands - Console | 5,15 | stop-only | FreeRadius | True |
| Exec - Default | - | start-stop | FreeRadius | - |
| System - Default | - | start-stop | FreeRadius | - |
| Commands - Default | 5 | stop-only | FreeRadius | True |
| Commands - Default | 15 | stop-only | FreeRadius | True |

#### AAA Accounting Device Configuration

```eos
aaa accounting commands 5,15 console stop-only group FreeRadius logging
aaa accounting exec default start-stop group FreeRadius
aaa accounting system default start-stop group FreeRadius
aaa accounting commands 5 default stop-only group FreeRadius logging
aaa accounting commands 15 default stop-only group FreeRadius logging
```

## Monitoring

### TerminAttr Daemon

#### TerminAttr Daemon Summary

| CV Compression | CloudVision Servers | VRF | Authentication | Smash Excludes | Ingest Exclude | Bypass AAA |
| -------------- | ------------------- | --- | -------------- | -------------- | -------------- | ---------- |
| gzip | apiserver.arista.io:443 | MGMT | token-secure,/tmp/cv-onboarding-token | ale,flexCounter,hardware,kni,pulse,strata | /Sysdb/cell/1/agent,/Sysdb/cell/2/agent | True |

#### TerminAttr Daemon Device Configuration

```eos
!
daemon TerminAttr
   exec /usr/bin/TerminAttr -cvaddr=apiserver.arista.io:443 -cvauth=token-secure,/tmp/cv-onboarding-token -cvvrf=MGMT -disableaaa -smashexcludes=ale,flexCounter,hardware,kni,pulse,strata -ingestexclude=/Sysdb/cell/1/agent,/Sysdb/cell/2/agent -taillogs
   no shutdown
```

## MLAG

### MLAG Summary

| Domain-id | Local-interface | Peer-address | Peer-link |
| --------- | --------------- | ------------ | --------- |
| RE-AVD-BrdrLeaf1 | Vlan4094 | 192.168.252.37 | Port-Channel5 |

Dual primary detection is disabled.

### MLAG Device Configuration

```eos
!
mlag configuration
   domain-id RE-AVD-BrdrLeaf1
   local-interface Vlan4094
   peer-address 192.168.252.37
   peer-link Port-Channel5
   reload-delay mlag 300
   reload-delay non-mlag 330
```

## Spanning Tree

### Spanning Tree Summary

STP mode: **mstp**

#### MSTP Instance and Priority

| Instance(s) | Priority |
| -------- | -------- |
| 0 | 16384 |

#### Global Spanning-Tree Settings

- Spanning Tree disabled for VLANs: **4093-4094**

### Spanning Tree Device Configuration

```eos
!
spanning-tree mode mstp
no spanning-tree vlan-id 4093-4094
spanning-tree mst 0 priority 16384
```

## Internal VLAN Allocation Policy

### Internal VLAN Allocation Policy Summary

| Policy Allocation | Range Beginning | Range Ending |
| ------------------| --------------- | ------------ |
| ascending | 1006 | 1199 |

### Internal VLAN Allocation Policy Device Configuration

```eos
!
vlan internal order ascending range 1006 1199
```

## VLANs

### VLANs Summary

| VLAN ID | Name | Trunk Groups |
| ------- | ---- | ------------ |
| 110 | App_Zone_110 | - |
| 111 | App_Zone_111 | - |
| 112 | App_Zone_112 | - |
| 120 | Op_Zone_120 | - |
| 121 | Op_Zone_121 | - |
| 3099 | MLAG_iBGP_App_Zone | LEAF_PEER_L3 |
| 3199 | MLAG_iBGP_Op_Zone | LEAF_PEER_L3 |
| 3998 | MLAG_iBGP_Internet | LEAF_PEER_L3 |
| 4093 | LEAF_PEER_L3 | LEAF_PEER_L3 |
| 4094 | MLAG_PEER | MLAG |

### VLANs Device Configuration

```eos
!
vlan 110
   name App_Zone_110
!
vlan 111
   name App_Zone_111
!
vlan 112
   name App_Zone_112
!
vlan 120
   name Op_Zone_120
!
vlan 121
   name Op_Zone_121
!
vlan 3099
   name MLAG_iBGP_App_Zone
   trunk group LEAF_PEER_L3
!
vlan 3199
   name MLAG_iBGP_Op_Zone
   trunk group LEAF_PEER_L3
!
vlan 3998
   name MLAG_iBGP_Internet
   trunk group LEAF_PEER_L3
!
vlan 4093
   name LEAF_PEER_L3
   trunk group LEAF_PEER_L3
!
vlan 4094
   name MLAG_PEER
   trunk group MLAG
```

## Interfaces

### Interface Defaults

#### Interface Defaults Summary

- Default Ethernet Interface Shutdown: True

#### Interface Defaults Device Configuration

```eos
!
interface defaults
   ethernet
      shutdown
```

### Ethernet Interfaces

#### Ethernet Interfaces Summary

##### L2

| Interface | Description | Mode | VLANs | Native VLAN | Trunk Group | Channel-Group |
| --------- | ----------- | ---- | ----- | ----------- | ----------- | ------------- |
| Ethernet5 | MLAG_PEER_RE-AVD-BrdrLeaf1B_Ethernet5 | *trunk | *- | *- | *['LEAF_PEER_L3', 'MLAG'] | 5 |
| Ethernet6 | MLAG_PEER_RE-AVD-BrdrLeaf1B_Ethernet6 | *trunk | *- | *- | *['LEAF_PEER_L3', 'MLAG'] | 5 |

*Inherited from Port-Channel Interface

##### IPv4

| Interface | Description | Type | Channel Group | IP Address | VRF |  MTU | Shutdown | ACL In | ACL Out |
| --------- | ----------- | -----| ------------- | ---------- | ----| ---- | -------- | ------ | ------- |
| Ethernet1 | P2P_LINK_TO_RE-AVD-SPINE1_Ethernet5 | routed | - | 192.168.0.145/31 | default | 1500 | False | - | - |
| Ethernet2 | P2P_LINK_TO_RE-AVD-SPINE2_Ethernet5 | routed | - | 192.168.0.147/31 | default | 1500 | False | - | - |
| Ethernet3 | P2P_LINK_TO_RE-AVD-SPINE3_Ethernet5 | routed | - | 192.168.0.149/31 | default | 1500 | False | - | - |
| Ethernet4 | P2P_LINK_TO_RE-AVD-SPINE4_Ethernet5 | routed | - | 192.168.0.151/31 | default | 1500 | False | - | - |
| Ethernet7 | Internet Connection | routed | - | 192.168.20.23/23 | Internet | - | False | - | - |

#### Ethernet Interfaces Device Configuration

```eos
!
interface Ethernet1
   description P2P_LINK_TO_RE-AVD-SPINE1_Ethernet5
   no shutdown
   mtu 1500
   no switchport
   ip address 192.168.0.145/31
!
interface Ethernet2
   description P2P_LINK_TO_RE-AVD-SPINE2_Ethernet5
   no shutdown
   mtu 1500
   no switchport
   ip address 192.168.0.147/31
!
interface Ethernet3
   description P2P_LINK_TO_RE-AVD-SPINE3_Ethernet5
   no shutdown
   mtu 1500
   no switchport
   ip address 192.168.0.149/31
!
interface Ethernet4
   description P2P_LINK_TO_RE-AVD-SPINE4_Ethernet5
   no shutdown
   mtu 1500
   no switchport
   ip address 192.168.0.151/31
!
interface Ethernet5
   description MLAG_PEER_RE-AVD-BrdrLeaf1B_Ethernet5
   no shutdown
   channel-group 5 mode active
!
interface Ethernet6
   description MLAG_PEER_RE-AVD-BrdrLeaf1B_Ethernet6
   no shutdown
   channel-group 5 mode active
!
interface Ethernet7
   description Internet Connection
   no shutdown
   no switchport
   vrf Internet
   ip address 192.168.20.23/23
```

### Port-Channel Interfaces

#### Port-Channel Interfaces Summary

##### L2

| Interface | Description | Type | Mode | VLANs | Native VLAN | Trunk Group | LACP Fallback Timeout | LACP Fallback Mode | MLAG ID | EVPN ESI |
| --------- | ----------- | ---- | ---- | ----- | ----------- | ------------| --------------------- | ------------------ | ------- | -------- |
| Port-Channel5 | MLAG_PEER_RE-AVD-BrdrLeaf1B_Po5 | switched | trunk | - | - | ['LEAF_PEER_L3', 'MLAG'] | - | - | - | - |

#### Port-Channel Interfaces Device Configuration

```eos
!
interface Port-Channel5
   description MLAG_PEER_RE-AVD-BrdrLeaf1B_Po5
   no shutdown
   switchport
   switchport mode trunk
   switchport trunk group LEAF_PEER_L3
   switchport trunk group MLAG
```

### Loopback Interfaces

#### Loopback Interfaces Summary

##### IPv4

| Interface | Description | VRF | IP Address |
| --------- | ----------- | --- | ---------- |
| Loopback0 | EVPN_Overlay_Peering | default | 192.168.254.21/32 |
| Loopback1 | VTEP_VXLAN_Tunnel_Source | default | 192.168.253.21/32 |
| Loopback100 | App_Zone_VTEP_DIAGNOSTICS | App_Zone | 192.168.100.21/32 |
| Loopback101 | Op_Zone_VTEP_DIAGNOSTICS | Op_Zone | 192.168.101.21/32 |

##### IPv6

| Interface | Description | VRF | IPv6 Address |
| --------- | ----------- | --- | ------------ |
| Loopback0 | EVPN_Overlay_Peering | default | - |
| Loopback1 | VTEP_VXLAN_Tunnel_Source | default | - |
| Loopback100 | App_Zone_VTEP_DIAGNOSTICS | App_Zone | - |
| Loopback101 | Op_Zone_VTEP_DIAGNOSTICS | Op_Zone | - |

#### Loopback Interfaces Device Configuration

```eos
!
interface Loopback0
   description EVPN_Overlay_Peering
   no shutdown
   ip address 192.168.254.21/32
!
interface Loopback1
   description VTEP_VXLAN_Tunnel_Source
   no shutdown
   ip address 192.168.253.21/32
!
interface Loopback100
   description App_Zone_VTEP_DIAGNOSTICS
   no shutdown
   vrf App_Zone
   ip address 192.168.100.21/32
!
interface Loopback101
   description Op_Zone_VTEP_DIAGNOSTICS
   no shutdown
   vrf Op_Zone
   ip address 192.168.101.21/32
```

### VLAN Interfaces

#### VLAN Interfaces Summary

| Interface | Description | VRF |  MTU | Shutdown |
| --------- | ----------- | --- | ---- | -------- |
| Vlan110 | App_Zone_110 | App_Zone | - | False |
| Vlan111 | App_Zone_111 | App_Zone | - | False |
| Vlan112 | App_Zone_112 | App_Zone | - | False |
| Vlan120 | Op_Zone_120 | Op_Zone | - | False |
| Vlan121 | Op_Zone_121 | Op_Zone | - | False |
| Vlan3099 | MLAG_PEER_L3_iBGP: vrf App_Zone | App_Zone | 1500 | False |
| Vlan3199 | MLAG_PEER_L3_iBGP: vrf Op_Zone | Op_Zone | 1500 | False |
| Vlan3998 | MLAG_PEER_L3_iBGP: vrf Internet | Internet | 1500 | False |
| Vlan4093 | MLAG_PEER_L3_PEERING | default | 1500 | False |
| Vlan4094 | MLAG_PEER | default | 1500 | False |

##### IPv4

| Interface | VRF | IP Address | IP Address Virtual | IP Router Virtual Address | VRRP | ACL In | ACL Out |
| --------- | --- | ---------- | ------------------ | ------------------------- | ---- | ------ | ------- |
| Vlan110 |  App_Zone  |  -  |  192.168.110.1/24  |  -  |  -  |  -  |  -  |
| Vlan111 |  App_Zone  |  -  |  192.168.111.1/24  |  -  |  -  |  -  |  -  |
| Vlan112 |  App_Zone  |  -  |  192.168.112.1/24  |  -  |  -  |  -  |  -  |
| Vlan120 |  Op_Zone  |  -  |  192.168.120.1/24  |  -  |  -  |  -  |  -  |
| Vlan121 |  Op_Zone  |  -  |  192.168.121.1/24  |  -  |  -  |  -  |  -  |
| Vlan3099 |  App_Zone  |  192.168.251.36/31  |  -  |  -  |  -  |  -  |  -  |
| Vlan3199 |  Op_Zone  |  192.168.251.36/31  |  -  |  -  |  -  |  -  |  -  |
| Vlan3998 |  Internet  |  192.168.251.36/31  |  -  |  -  |  -  |  -  |  -  |
| Vlan4093 |  default  |  192.168.251.36/31  |  -  |  -  |  -  |  -  |  -  |
| Vlan4094 |  default  |  192.168.252.36/31  |  -  |  -  |  -  |  -  |  -  |

#### VLAN Interfaces Device Configuration

```eos
!
interface Vlan110
   description App_Zone_110
   no shutdown
   vrf App_Zone
   ip address virtual 192.168.110.1/24
!
interface Vlan111
   description App_Zone_111
   no shutdown
   vrf App_Zone
   ip address virtual 192.168.111.1/24
!
interface Vlan112
   description App_Zone_112
   no shutdown
   vrf App_Zone
   ip address virtual 192.168.112.1/24
!
interface Vlan120
   description Op_Zone_120
   no shutdown
   vrf Op_Zone
   ip address virtual 192.168.120.1/24
!
interface Vlan121
   description Op_Zone_121
   no shutdown
   vrf Op_Zone
   ip address virtual 192.168.121.1/24
!
interface Vlan3099
   description MLAG_PEER_L3_iBGP: vrf App_Zone
   no shutdown
   mtu 1500
   vrf App_Zone
   ip address 192.168.251.36/31
!
interface Vlan3199
   description MLAG_PEER_L3_iBGP: vrf Op_Zone
   no shutdown
   mtu 1500
   vrf Op_Zone
   ip address 192.168.251.36/31
!
interface Vlan3998
   description MLAG_PEER_L3_iBGP: vrf Internet
   no shutdown
   mtu 1500
   vrf Internet
   ip address 192.168.251.36/31
!
interface Vlan4093
   description MLAG_PEER_L3_PEERING
   no shutdown
   mtu 1500
   ip address 192.168.251.36/31
!
interface Vlan4094
   description MLAG_PEER
   no shutdown
   mtu 1500
   no autostate
   ip address 192.168.252.36/31
```

### VXLAN Interface

#### VXLAN Interface Summary

| Setting | Value |
| ------- | ----- |
| Source Interface | Loopback1 |
| UDP port | 4789 |
| EVPN MLAG Shared Router MAC | mlag-system-id |

##### VLAN to VNI, Flood List and Multicast Group Mappings

| VLAN | VNI | Flood List | Multicast Group |
| ---- | --- | ---------- | --------------- |
| 110 | 20110 | - | - |
| 111 | 20111 | - | - |
| 112 | 20112 | - | - |
| 120 | 20120 | - | - |
| 121 | 20121 | - | - |

##### VRF to VNI and Multicast Group Mappings

| VRF | VNI | Multicast Group |
| ---- | --- | --------------- |
| App_Zone | 100 | - |
| Internet | 999 | - |
| Op_Zone | 200 | - |

#### VXLAN Interface Device Configuration

```eos
!
interface Vxlan1
   description RE-AVD-BrdrLeaf1A_VTEP
   vxlan source-interface Loopback1
   vxlan virtual-router encapsulation mac-address mlag-system-id
   vxlan udp-port 4789
   vxlan vlan 110 vni 20110
   vxlan vlan 111 vni 20111
   vxlan vlan 112 vni 20112
   vxlan vlan 120 vni 20120
   vxlan vlan 121 vni 20121
   vxlan vrf App_Zone vni 100
   vxlan vrf Internet vni 999
   vxlan vrf Op_Zone vni 200
```

## Routing

### Service Routing Protocols Model

Multi agent routing protocol model enabled

```eos
!
service routing protocols model multi-agent
```

### Virtual Router MAC Address

#### Virtual Router MAC Address Summary

Virtual Router MAC Address: 00:1c:73:00:dc:01

#### Virtual Router MAC Address Device Configuration

```eos
!
ip virtual-router mac-address 00:1c:73:00:dc:01
```

### IP Routing

#### IP Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | True |
| App_Zone | True |
| Internet | True |
| MGMT | True |
| Op_Zone | True |

#### IP Routing Device Configuration

```eos
!
ip routing
ip routing vrf App_Zone
ip routing vrf Internet
ip routing vrf MGMT
ip routing vrf Op_Zone
```

### IPv6 Routing

#### IPv6 Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | False |
| App_Zone | false |
| Internet | false |
| MGMT | false |
| Op_Zone | false |

### Static Routes

#### Static Routes Summary

| VRF | Destination Prefix | Next Hop IP | Exit interface | Administrative Distance | Tag | Route Name | Metric |
| --- | ------------------ | ----------- | -------------- | ----------------------- | --- | ---------- | ------ |
| Internet | 0.0.0.0/0 | 192.168.20.1 | - | 1 | - | - | - |
| MGMT | 0.0.0.0/0 | 192.168.255.1 | - | 1 | - | - | - |

#### Static Routes Device Configuration

```eos
!
ip route vrf Internet 0.0.0.0/0 192.168.20.1
ip route vrf MGMT 0.0.0.0/0 192.168.255.1
```

### Router General

#### VRF Route leaking

| VRF | Source VRF | Route Map Policy |
|-----|------------|------------------|
| Internet | App_Zone | RM-LEAK-VRFS |
| Internet | Op_Zone | RM-LEAK-VRFS |
| App_Zone | Internet | RM-LEAK-DEFAULT |
| Op_Zone | Internet | RM-LEAK-DEFAULT |

#### Router General Device Configuration

```eos
!
router general
   vrf App_Zone
      leak routes source-vrf Internet subscribe-policy RM-LEAK-DEFAULT
      exit
   !
   vrf Internet
      leak routes source-vrf App_Zone subscribe-policy RM-LEAK-VRFS
      leak routes source-vrf Op_Zone subscribe-policy RM-LEAK-VRFS
      exit
   !
   vrf Op_Zone
      leak routes source-vrf Internet subscribe-policy RM-LEAK-DEFAULT
      exit
   !
   exit
```

### Router BGP

#### Router BGP Summary

| BGP AS | Router ID |
| ------ | --------- |
| 65103 | 192.168.254.21 |

| BGP Tuning |
| ---------- |
| distance bgp 20 200 200 |
| graceful-restart restart-time 300 |
| graceful-restart |
| no bgp default ipv4-unicast |
| maximum-paths 4 ecmp 4 |

#### Router BGP Peer Groups

##### EVPN-OVERLAY-PEERS

| Settings | Value |
| -------- | ----- |
| Address Family | evpn |
| Source | Loopback0 |
| BFD | True |
| Ebgp multihop | 3 |
| Send community | all |
| Maximum routes | 0 (no limit) |

##### IPv4-UNDERLAY-PEERS

| Settings | Value |
| -------- | ----- |
| Address Family | ipv4 |
| Send community | all |
| Maximum routes | 12000 |

##### MLAG-IPv4-UNDERLAY-PEER

| Settings | Value |
| -------- | ----- |
| Address Family | ipv4 |
| Remote AS | 65103 |
| Next-hop self | True |
| Send community | all |
| Maximum routes | 12000 |

#### BGP Neighbors

| Neighbor | Remote AS | VRF | Shutdown | Send-community | Maximum-routes | Allowas-in | BFD | RIB Pre-Policy Retain | Route-Reflector Client | Passive | TTL Max Hops |
| -------- | --------- | --- | -------- | -------------- | -------------- | ---------- | --- | --------------------- | ---------------------- | ------- | ------------ |
| 192.168.0.144 | 65001 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 192.168.0.146 | 65001 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 192.168.0.148 | 65001 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 192.168.0.150 | 65001 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 192.168.251.37 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | default | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - | - | - | - |
| 192.168.254.11 | 65001 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 192.168.254.12 | 65001 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 192.168.254.13 | 65001 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 192.168.254.14 | 65001 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 192.168.251.37 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | App_Zone | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - | - | - |
| 192.168.251.37 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Internet | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - | - | - |
| 192.168.251.37 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Op_Zone | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - | - | - |

#### Router BGP EVPN Address Family

##### EVPN Peer Groups

| Peer Group | Activate | Encapsulation |
| ---------- | -------- | ------------- |
| EVPN-OVERLAY-PEERS | True | default |

#### Router BGP VLAN Aware Bundles

| VLAN Aware Bundle | Route-Distinguisher | Both Route-Target | Import Route Target | Export Route-Target | Redistribute | VLANs |
| ----------------- | ------------------- | ----------------- | ------------------- | ------------------- | ------------ | ----- |
| App_Zone | 192.168.254.21:100 | 100:100 | - | - | learned | 110-112 |
| Op_Zone | 192.168.254.21:200 | 200:200 | - | - | learned | 120-121 |

#### Router BGP VRFs

| VRF | Route-Distinguisher | Redistribute |
| --- | ------------------- | ------------ |
| App_Zone | 192.168.254.21:100 | connected<br>static |
| Internet | 192.168.254.21:999 | connected<br>static |
| Op_Zone | 192.168.254.21:200 | connected<br>static |

#### Router BGP Device Configuration

```eos
!
router bgp 65103
   router-id 192.168.254.21
   maximum-paths 4 ecmp 4
   no bgp default ipv4-unicast
   distance bgp 20 200 200
   graceful-restart restart-time 300
   graceful-restart
   neighbor EVPN-OVERLAY-PEERS peer group
   neighbor EVPN-OVERLAY-PEERS update-source Loopback0
   neighbor EVPN-OVERLAY-PEERS bfd
   neighbor EVPN-OVERLAY-PEERS ebgp-multihop 3
   neighbor EVPN-OVERLAY-PEERS password 7 <removed>
   neighbor EVPN-OVERLAY-PEERS send-community
   neighbor EVPN-OVERLAY-PEERS maximum-routes 0
   neighbor IPv4-UNDERLAY-PEERS peer group
   neighbor IPv4-UNDERLAY-PEERS password 7 <removed>
   neighbor IPv4-UNDERLAY-PEERS send-community
   neighbor IPv4-UNDERLAY-PEERS maximum-routes 12000
   neighbor MLAG-IPv4-UNDERLAY-PEER peer group
   neighbor MLAG-IPv4-UNDERLAY-PEER remote-as 65103
   neighbor MLAG-IPv4-UNDERLAY-PEER next-hop-self
   neighbor MLAG-IPv4-UNDERLAY-PEER description RE-AVD-BrdrLeaf1B
   neighbor MLAG-IPv4-UNDERLAY-PEER password 7 <removed>
   neighbor MLAG-IPv4-UNDERLAY-PEER send-community
   neighbor MLAG-IPv4-UNDERLAY-PEER maximum-routes 12000
   neighbor MLAG-IPv4-UNDERLAY-PEER route-map RM-MLAG-PEER-IN in
   neighbor 192.168.0.144 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.0.144 remote-as 65001
   neighbor 192.168.0.144 description RE-AVD-Spine1_Ethernet5
   neighbor 192.168.0.146 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.0.146 remote-as 65001
   neighbor 192.168.0.146 description RE-AVD-Spine2_Ethernet5
   neighbor 192.168.0.148 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.0.148 remote-as 65001
   neighbor 192.168.0.148 description RE-AVD-Spine3_Ethernet5
   neighbor 192.168.0.150 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.0.150 remote-as 65001
   neighbor 192.168.0.150 description RE-AVD-Spine4_Ethernet5
   neighbor 192.168.251.37 peer group MLAG-IPv4-UNDERLAY-PEER
   neighbor 192.168.251.37 description RE-AVD-BrdrLeaf1B
   neighbor 192.168.254.11 peer group EVPN-OVERLAY-PEERS
   neighbor 192.168.254.11 remote-as 65001
   neighbor 192.168.254.11 description RE-AVD-Spine1
   neighbor 192.168.254.12 peer group EVPN-OVERLAY-PEERS
   neighbor 192.168.254.12 remote-as 65001
   neighbor 192.168.254.12 description RE-AVD-Spine2
   neighbor 192.168.254.13 peer group EVPN-OVERLAY-PEERS
   neighbor 192.168.254.13 remote-as 65001
   neighbor 192.168.254.13 description RE-AVD-Spine3
   neighbor 192.168.254.14 peer group EVPN-OVERLAY-PEERS
   neighbor 192.168.254.14 remote-as 65001
   neighbor 192.168.254.14 description RE-AVD-Spine4
   redistribute connected route-map RM-CONN-2-BGP
   !
   vlan-aware-bundle App_Zone
      rd 192.168.254.21:100
      route-target both 100:100
      redistribute learned
      vlan 110-112
   !
   vlan-aware-bundle Op_Zone
      rd 192.168.254.21:200
      route-target both 200:200
      redistribute learned
      vlan 120-121
   !
   address-family evpn
      neighbor EVPN-OVERLAY-PEERS activate
   !
   address-family ipv4
      no neighbor EVPN-OVERLAY-PEERS activate
      neighbor IPv4-UNDERLAY-PEERS activate
      neighbor MLAG-IPv4-UNDERLAY-PEER activate
   !
   vrf App_Zone
      rd 192.168.254.21:100
      route-target import evpn 100:100
      route-target export evpn 100:100
      router-id 192.168.254.21
      neighbor 192.168.251.37 peer group MLAG-IPv4-UNDERLAY-PEER
      redistribute connected
      redistribute static include leaked route-map RM-LEAK-DEFAULT
   !
   vrf Internet
      rd 192.168.254.21:999
      route-target import evpn 999:999
      route-target export evpn 999:999
      router-id 192.168.254.21
      neighbor 192.168.251.37 peer group MLAG-IPv4-UNDERLAY-PEER
      redistribute connected
      redistribute static
   !
   vrf Op_Zone
      rd 192.168.254.21:200
      route-target import evpn 200:200
      route-target export evpn 200:200
      router-id 192.168.254.21
      neighbor 192.168.251.37 peer group MLAG-IPv4-UNDERLAY-PEER
      redistribute connected
      redistribute static include leaked route-map RM-LEAK-DEFAULT
```

## BFD

### Router BFD

#### Router BFD Multihop Summary

| Interval | Minimum RX | Multiplier |
| -------- | ---------- | ---------- |
| 1200 | 1200 | 3 |

#### Router BFD Device Configuration

```eos
!
router bfd
   multihop interval 1200 min-rx 1200 multiplier 3
```

## Multicast

### IP IGMP Snooping

#### IP IGMP Snooping Summary

| IGMP Snooping | Fast Leave | Interface Restart Query | Proxy | Restart Query Interval | Robustness Variable |
| ------------- | ---------- | ----------------------- | ----- | ---------------------- | ------------------- |
| Enabled | - | - | - | - | - |

#### IP IGMP Snooping Device Configuration

```eos
```

## Filters

### Prefix-lists

#### Prefix-lists Summary

##### PL-LEAK-APP-ZONE

| Sequence | Action |
| -------- | ------ |
| 10 | permit 192.168.110.0/24 le 32 |
| 20 | permit 192.168.111.0/24 le 32 |
| 30 | permit 192.168.112.0/24 le 32 |
| 40 | permit 192.168.100.0/24 eq 32 |

##### PL-LEAK-DEFAULT

| Sequence | Action |
| -------- | ------ |
| 10 | permit 0.0.0.0/0 |

##### PL-LEAK-OP-ZONE

| Sequence | Action |
| -------- | ------ |
| 10 | permit 192.168.120.0/24 le 32 |
| 20 | permit 192.168.121.0/24 le 32 |
| 30 | permit 192.168.200.0/24 eq 32 |

##### PL-LOOPBACKS-EVPN-OVERLAY

| Sequence | Action |
| -------- | ------ |
| 10 | permit 192.168.254.0/24 eq 32 |
| 20 | permit 192.168.253.0/24 eq 32 |

#### Prefix-lists Device Configuration

```eos
!
ip prefix-list PL-LEAK-APP-ZONE
   seq 10 permit 192.168.110.0/24 le 32
   seq 20 permit 192.168.111.0/24 le 32
   seq 30 permit 192.168.112.0/24 le 32
   seq 40 permit 192.168.100.0/24 eq 32
!
ip prefix-list PL-LEAK-DEFAULT
   seq 10 permit 0.0.0.0/0
!
ip prefix-list PL-LEAK-OP-ZONE
   seq 10 permit 192.168.120.0/24 le 32
   seq 20 permit 192.168.121.0/24 le 32
   seq 30 permit 192.168.200.0/24 eq 32
!
ip prefix-list PL-LOOPBACKS-EVPN-OVERLAY
   seq 10 permit 192.168.254.0/24 eq 32
   seq 20 permit 192.168.253.0/24 eq 32
```

### Route-maps

#### Route-maps Summary

##### RM-CONN-2-BGP

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | permit | ip address prefix-list PL-LOOPBACKS-EVPN-OVERLAY | - | - | - |

##### RM-LEAK-DEFAULT

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | permit | ip address prefix-list PL-LEAK-DEFAULT | - | - | - |

##### RM-LEAK-VRFS

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | permit | ip address prefix-list PL-LEAK-APP-ZONE | - | - | - |
| 20 | permit | ip address prefix-list PL-LEAK-OP-ZONE | - | - | - |

##### RM-MLAG-PEER-IN

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | permit | - | origin incomplete | - | - |

#### Route-maps Device Configuration

```eos
!
route-map RM-CONN-2-BGP permit 10
   match ip address prefix-list PL-LOOPBACKS-EVPN-OVERLAY
!
route-map RM-LEAK-DEFAULT permit 10
   match ip address prefix-list PL-LEAK-DEFAULT
!
route-map RM-LEAK-VRFS permit 10
   match ip address prefix-list PL-LEAK-APP-ZONE
!
route-map RM-LEAK-VRFS permit 20
   match ip address prefix-list PL-LEAK-OP-ZONE
!
route-map RM-MLAG-PEER-IN permit 10
   description Make routes learned over MLAG Peer-link less preferred on spines to ensure optimal routing
   set origin incomplete
```

## VRF Instances

### VRF Instances Summary

| VRF Name | IP Routing |
| -------- | ---------- |
| App_Zone | enabled |
| Internet | enabled |
| MGMT | enabled |
| Op_Zone | enabled |

### VRF Instances Device Configuration

```eos
!
vrf instance App_Zone
!
vrf instance Internet
!
vrf instance MGMT
!
vrf instance Op_Zone
```

## Virtual Source NAT

### Virtual Source NAT Summary

| Source NAT VRF | Source NAT IP Address |
| -------------- | --------------------- |
| App_Zone | 192.168.100.21 |
| Op_Zone | 192.168.101.21 |

### Virtual Source NAT Configuration

```eos
!
ip address virtual source-nat vrf App_Zone address 192.168.100.21
ip address virtual source-nat vrf Op_Zone address 192.168.101.21
```

## EOS CLI Device Configuration

```eos
!
no schedule tech-support
```
