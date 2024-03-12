# RE-AVD-Spine3

## Table of Contents

- [Management](#management)
  - [Management Interfaces](#management-interfaces)
  - [DNS Domain](#dns-domain)
  - [IP Name Servers](#ip-name-servers)
  - [Clock Settings](#clock-settings)
  - [NTP](#ntp)
  - [IP Client Source Interfaces](#ip-client-source-interfaces)
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
- [Spanning Tree](#spanning-tree)
  - [Spanning Tree Summary](#spanning-tree-summary)
  - [Spanning Tree Device Configuration](#spanning-tree-device-configuration)
- [Internal VLAN Allocation Policy](#internal-vlan-allocation-policy)
  - [Internal VLAN Allocation Policy Summary](#internal-vlan-allocation-policy-summary)
  - [Internal VLAN Allocation Policy Device Configuration](#internal-vlan-allocation-policy-device-configuration)
- [Interfaces](#interfaces)
  - [Interface Defaults](#interface-defaults)
  - [Ethernet Interfaces](#ethernet-interfaces)
  - [Loopback Interfaces](#loopback-interfaces)
- [Routing](#routing)
  - [Service Routing Protocols Model](#service-routing-protocols-model)
  - [IP Routing](#ip-routing)
  - [IPv6 Routing](#ipv6-routing)
  - [Static Routes](#static-routes)
  - [Router BGP](#router-bgp)
- [BFD](#bfd)
  - [Router BFD](#router-bfd)
- [Filters](#filters)
  - [Prefix-lists](#prefix-lists)
  - [Route-maps](#route-maps)
- [VRF Instances](#vrf-instances)
  - [VRF Instances Summary](#vrf-instances-summary)
  - [VRF Instances Device Configuration](#vrf-instances-device-configuration)
- [EOS CLI Device Configuration](#eos-cli-device-configuration)

## Management

### Management Interfaces

#### Management Interfaces Summary

##### IPv4

| Management Interface | Description | Type | VRF | IP Address | Gateway |
| -------------------- | ----------- | ---- | --- | ---------- | ------- |
| Management1 | oob_management | oob | MGMT | 192.168.255.13/24 | - |

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
   ip address 192.168.255.13/24
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

### IP Client Source Interfaces

| IP Client | VRF | Source Interface Name |
| --------- | --- | --------------------- |
| SSH | default | Loopback0 |

#### IP Client Source Interfaces Device Configuration

```eos
!
ip ssh client source-interface Loopback0
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

## Spanning Tree

### Spanning Tree Summary

STP mode: **none**

### Spanning Tree Device Configuration

```eos
!
spanning-tree mode none
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

*Inherited from Port-Channel Interface

##### IPv4

| Interface | Description | Type | Channel Group | IP Address | VRF |  MTU | Shutdown | ACL In | ACL Out |
| --------- | ----------- | -----| ------------- | ---------- | ----| ---- | -------- | ------ | ------- |
| Ethernet1 | P2P_LINK_TO_RE-AVD-LEAF1A_Ethernet3 | routed | - | 192.168.0.116/31 | default | 1500 | False | - | - |
| Ethernet2 | P2P_LINK_TO_RE-AVD-LEAF1B_Ethernet3 | routed | - | 192.168.0.124/31 | default | 1500 | False | - | - |
| Ethernet3 | P2P_LINK_TO_RE-AVD-LEAF2A_Ethernet3 | routed | - | 192.168.0.132/31 | default | 1500 | False | - | - |
| Ethernet4 | P2P_LINK_TO_RE-AVD-LEAF2B_Ethernet3 | routed | - | 192.168.0.140/31 | default | 1500 | False | - | - |
| Ethernet5 | P2P_LINK_TO_RE-AVD-BRDRLEAF1A_Ethernet3 | routed | - | 192.168.0.148/31 | default | 1500 | False | - | - |
| Ethernet6 | P2P_LINK_TO_RE-AVD-BRDRLEAF1B_Ethernet3 | routed | - | 192.168.0.156/31 | default | 1500 | False | - | - |

#### Ethernet Interfaces Device Configuration

```eos
!
interface Ethernet1
   description P2P_LINK_TO_RE-AVD-LEAF1A_Ethernet3
   no shutdown
   mtu 1500
   no switchport
   ip address 192.168.0.116/31
!
interface Ethernet2
   description P2P_LINK_TO_RE-AVD-LEAF1B_Ethernet3
   no shutdown
   mtu 1500
   no switchport
   ip address 192.168.0.124/31
!
interface Ethernet3
   description P2P_LINK_TO_RE-AVD-LEAF2A_Ethernet3
   no shutdown
   mtu 1500
   no switchport
   ip address 192.168.0.132/31
!
interface Ethernet4
   description P2P_LINK_TO_RE-AVD-LEAF2B_Ethernet3
   no shutdown
   mtu 1500
   no switchport
   ip address 192.168.0.140/31
!
interface Ethernet5
   description P2P_LINK_TO_RE-AVD-BRDRLEAF1A_Ethernet3
   no shutdown
   mtu 1500
   no switchport
   ip address 192.168.0.148/31
!
interface Ethernet6
   description P2P_LINK_TO_RE-AVD-BRDRLEAF1B_Ethernet3
   no shutdown
   mtu 1500
   no switchport
   ip address 192.168.0.156/31
```

### Loopback Interfaces

#### Loopback Interfaces Summary

##### IPv4

| Interface | Description | VRF | IP Address |
| --------- | ----------- | --- | ---------- |
| Loopback0 | EVPN_Overlay_Peering | default | 192.168.254.13/32 |

##### IPv6

| Interface | Description | VRF | IPv6 Address |
| --------- | ----------- | --- | ------------ |
| Loopback0 | EVPN_Overlay_Peering | default | - |

#### Loopback Interfaces Device Configuration

```eos
!
interface Loopback0
   description EVPN_Overlay_Peering
   no shutdown
   ip address 192.168.254.13/32
```

## Routing

### Service Routing Protocols Model

Multi agent routing protocol model enabled

```eos
!
service routing protocols model multi-agent
```

### IP Routing

#### IP Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | True |
| MGMT | True |

#### IP Routing Device Configuration

```eos
!
ip routing
ip routing vrf MGMT
```

### IPv6 Routing

#### IPv6 Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | False |
| MGMT | false |

### Static Routes

#### Static Routes Summary

| VRF | Destination Prefix | Next Hop IP | Exit interface | Administrative Distance | Tag | Route Name | Metric |
| --- | ------------------ | ----------- | -------------- | ----------------------- | --- | ---------- | ------ |
| MGMT | 0.0.0.0/0 | 192.168.255.1 | - | 1 | - | - | - |

#### Static Routes Device Configuration

```eos
!
ip route vrf MGMT 0.0.0.0/0 192.168.255.1
```

### Router BGP

#### Router BGP Summary

| BGP AS | Router ID |
| ------ | --------- |
| 65001 | 192.168.254.13 |

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
| Next-hop unchanged | True |
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

#### BGP Neighbors

| Neighbor | Remote AS | VRF | Shutdown | Send-community | Maximum-routes | Allowas-in | BFD | RIB Pre-Policy Retain | Route-Reflector Client | Passive | TTL Max Hops |
| -------- | --------- | --- | -------- | -------------- | -------------- | ---------- | --- | --------------------- | ---------------------- | ------- | ------------ |
| 192.168.0.117 | 65101 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 192.168.0.125 | 65101 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 192.168.0.133 | 65102 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 192.168.0.141 | 65102 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 192.168.0.149 | 65103 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 192.168.0.157 | 65103 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 192.168.254.17 | 65101 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 192.168.254.18 | 65101 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 192.168.254.19 | 65102 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 192.168.254.20 | 65102 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 192.168.254.21 | 65103 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 192.168.254.22 | 65103 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |

#### Router BGP EVPN Address Family

##### EVPN Peer Groups

| Peer Group | Activate | Encapsulation |
| ---------- | -------- | ------------- |
| EVPN-OVERLAY-PEERS | True | default |

#### Router BGP Device Configuration

```eos
!
router bgp 65001
   router-id 192.168.254.13
   maximum-paths 4 ecmp 4
   no bgp default ipv4-unicast
   distance bgp 20 200 200
   graceful-restart restart-time 300
   graceful-restart
   neighbor EVPN-OVERLAY-PEERS peer group
   neighbor EVPN-OVERLAY-PEERS next-hop-unchanged
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
   neighbor 192.168.0.117 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.0.117 remote-as 65101
   neighbor 192.168.0.117 description RE-AVD-Leaf1A_Ethernet3
   neighbor 192.168.0.125 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.0.125 remote-as 65101
   neighbor 192.168.0.125 description RE-AVD-Leaf1B_Ethernet3
   neighbor 192.168.0.133 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.0.133 remote-as 65102
   neighbor 192.168.0.133 description RE-AVD-Leaf2A_Ethernet3
   neighbor 192.168.0.141 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.0.141 remote-as 65102
   neighbor 192.168.0.141 description RE-AVD-Leaf2B_Ethernet3
   neighbor 192.168.0.149 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.0.149 remote-as 65103
   neighbor 192.168.0.149 description RE-AVD-BrdrLeaf1A_Ethernet3
   neighbor 192.168.0.157 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.0.157 remote-as 65103
   neighbor 192.168.0.157 description RE-AVD-BrdrLeaf1B_Ethernet3
   neighbor 192.168.254.17 peer group EVPN-OVERLAY-PEERS
   neighbor 192.168.254.17 remote-as 65101
   neighbor 192.168.254.17 description RE-AVD-Leaf1A
   neighbor 192.168.254.18 peer group EVPN-OVERLAY-PEERS
   neighbor 192.168.254.18 remote-as 65101
   neighbor 192.168.254.18 description RE-AVD-Leaf1B
   neighbor 192.168.254.19 peer group EVPN-OVERLAY-PEERS
   neighbor 192.168.254.19 remote-as 65102
   neighbor 192.168.254.19 description RE-AVD-Leaf2A
   neighbor 192.168.254.20 peer group EVPN-OVERLAY-PEERS
   neighbor 192.168.254.20 remote-as 65102
   neighbor 192.168.254.20 description RE-AVD-Leaf2B
   neighbor 192.168.254.21 peer group EVPN-OVERLAY-PEERS
   neighbor 192.168.254.21 remote-as 65103
   neighbor 192.168.254.21 description RE-AVD-BrdrLeaf1A
   neighbor 192.168.254.22 peer group EVPN-OVERLAY-PEERS
   neighbor 192.168.254.22 remote-as 65103
   neighbor 192.168.254.22 description RE-AVD-BrdrLeaf1B
   redistribute connected route-map RM-CONN-2-BGP
   !
   address-family evpn
      neighbor EVPN-OVERLAY-PEERS activate
   !
   address-family ipv4
      no neighbor EVPN-OVERLAY-PEERS activate
      neighbor IPv4-UNDERLAY-PEERS activate
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

## Filters

### Prefix-lists

#### Prefix-lists Summary

##### PL-LOOPBACKS-EVPN-OVERLAY

| Sequence | Action |
| -------- | ------ |
| 10 | permit 192.168.254.0/24 eq 32 |

#### Prefix-lists Device Configuration

```eos
!
ip prefix-list PL-LOOPBACKS-EVPN-OVERLAY
   seq 10 permit 192.168.254.0/24 eq 32
```

### Route-maps

#### Route-maps Summary

##### RM-CONN-2-BGP

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | permit | ip address prefix-list PL-LOOPBACKS-EVPN-OVERLAY | - | - | - |

#### Route-maps Device Configuration

```eos
!
route-map RM-CONN-2-BGP permit 10
   match ip address prefix-list PL-LOOPBACKS-EVPN-OVERLAY
```

## VRF Instances

### VRF Instances Summary

| VRF Name | IP Routing |
| -------- | ---------- |
| MGMT | enabled |

### VRF Instances Device Configuration

```eos
!
vrf instance MGMT
```

## EOS CLI Device Configuration

```eos
!
no schedule tech-support
```
