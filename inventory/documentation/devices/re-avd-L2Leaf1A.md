# RE-AVD-L2Leaf1A

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
  - [VLAN Interfaces](#vlan-interfaces)
- [Routing](#routing)
  - [Service Routing Protocols Model](#service-routing-protocols-model)
  - [IP Routing](#ip-routing)
  - [IPv6 Routing](#ipv6-routing)
  - [Static Routes](#static-routes)
- [Multicast](#multicast)
  - [IP IGMP Snooping](#ip-igmp-snooping)
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
| Management1 | oob_management | oob | MGMT | 192.168.255.21/24 | - |

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
   ip address 192.168.255.21/24
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

## MLAG

### MLAG Summary

| Domain-id | Local-interface | Peer-address | Peer-link |
| --------- | --------------- | ------------ | --------- |
| RE-AVD-L2Leaf1 | Vlan4094 | 192.168.252.41 | Port-Channel3 |

Dual primary detection is disabled.

### MLAG Device Configuration

```eos
!
mlag configuration
   domain-id RE-AVD-L2Leaf1
   local-interface Vlan4094
   peer-address 192.168.252.41
   peer-link Port-Channel3
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

- Spanning Tree disabled for VLANs: **4094**

### Spanning Tree Device Configuration

```eos
!
spanning-tree mode mstp
no spanning-tree vlan-id 4094
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
| Ethernet1 | RE-AVD-LEAF1A_Ethernet7 | *trunk | *110-112,120-121 | *- | *- | 1 |
| Ethernet2 | RE-AVD-LEAF1B_Ethernet7 | *trunk | *110-112,120-121 | *- | *- | 1 |
| Ethernet3 | MLAG_PEER_RE-AVD-L2Leaf1B_Ethernet3 | *trunk | *- | *- | *['MLAG'] | 3 |
| Ethernet4 | MLAG_PEER_RE-AVD-L2Leaf1B_Ethernet4 | *trunk | *- | *- | *['MLAG'] | 3 |
| Ethernet5 | Host1_Ethernet1 | *access | *110 | *- | *- | 5 |
| Ethernet6 |  Host3_ens3 | access | 120 | - | - | - |

*Inherited from Port-Channel Interface

#### Ethernet Interfaces Device Configuration

```eos
!
interface Ethernet1
   description RE-AVD-LEAF1A_Ethernet7
   no shutdown
   channel-group 1 mode on
!
interface Ethernet2
   description RE-AVD-LEAF1B_Ethernet7
   no shutdown
   channel-group 1 mode on
!
interface Ethernet3
   description MLAG_PEER_RE-AVD-L2Leaf1B_Ethernet3
   no shutdown
   channel-group 3 mode active
!
interface Ethernet4
   description MLAG_PEER_RE-AVD-L2Leaf1B_Ethernet4
   no shutdown
   channel-group 3 mode active
!
interface Ethernet5
   description Host1_Ethernet1
   no shutdown
   channel-group 5 mode on
!
interface Ethernet6
   description Host3_ens3
   no shutdown
   switchport access vlan 120
   switchport mode access
   switchport
```

### Port-Channel Interfaces

#### Port-Channel Interfaces Summary

##### L2

| Interface | Description | Type | Mode | VLANs | Native VLAN | Trunk Group | LACP Fallback Timeout | LACP Fallback Mode | MLAG ID | EVPN ESI |
| --------- | ----------- | ---- | ---- | ----- | ----------- | ------------| --------------------- | ------------------ | ------- | -------- |
| Port-Channel1 | RE-AVD-LEAF1_Po7 | switched | trunk | 110-112,120-121 | - | - | - | - | 1 | - |
| Port-Channel3 | MLAG_PEER_RE-AVD-L2Leaf1B_Po3 | switched | trunk | - | - | ['MLAG'] | - | - | - | - |
| Port-Channel5 | Host1 | switched | access | 110 | - | - | - | - | 5 | - |

#### Port-Channel Interfaces Device Configuration

```eos
!
interface Port-Channel1
   description RE-AVD-LEAF1_Po7
   no shutdown
   switchport
   switchport trunk allowed vlan 110-112,120-121
   switchport mode trunk
   mlag 1
!
interface Port-Channel3
   description MLAG_PEER_RE-AVD-L2Leaf1B_Po3
   no shutdown
   switchport
   switchport mode trunk
   switchport trunk group MLAG
!
interface Port-Channel5
   description Host1
   no shutdown
   switchport
   switchport access vlan 110
   mlag 5
```

### VLAN Interfaces

#### VLAN Interfaces Summary

| Interface | Description | VRF |  MTU | Shutdown |
| --------- | ----------- | --- | ---- | -------- |
| Vlan4094 | MLAG_PEER | default | 1500 | False |

##### IPv4

| Interface | VRF | IP Address | IP Address Virtual | IP Router Virtual Address | VRRP | ACL In | ACL Out |
| --------- | --- | ---------- | ------------------ | ------------------------- | ---- | ------ | ------- |
| Vlan4094 |  default  |  192.168.252.40/31  |  -  |  -  |  -  |  -  |  -  |

#### VLAN Interfaces Device Configuration

```eos
!
interface Vlan4094
   description MLAG_PEER
   no shutdown
   mtu 1500
   no autostate
   ip address 192.168.252.40/31
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
| default | False |
| MGMT | True |

#### IP Routing Device Configuration

```eos
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

## Multicast

### IP IGMP Snooping

#### IP IGMP Snooping Summary

| IGMP Snooping | Fast Leave | Interface Restart Query | Proxy | Restart Query Interval | Robustness Variable |
| ------------- | ---------- | ----------------------- | ----- | ---------------------- | ------------------- |
| Enabled | - | - | - | - | - |

#### IP IGMP Snooping Device Configuration

```eos
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
