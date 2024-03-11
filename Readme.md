# AVD Lab Design

<p style="text-align:center;">
<img style="background-color:white;" src="./data/avd-lab.png"> </br>
</p>


## Management Interface

- Interface: Management1
- IP Network: 192.168.255.0/24

### Management IP Addresses

| Node | Management Network IP Address |
| - | - |
| RE-AVD-Spine1 | 192.168.255.11 |
| RE-AVD-Spine2 | 192.168.255.12 |
| RE-AVD-Spine3 | 192.168.255.13 |
| RE-AVD-Spine4 | 192.168.255.14 |
| RE-AVD-Leaf1A | 192.168.255.15 |
| RE-AVD-Leaf1B | 192.168.255.16 |
| RE-AVD-Leaf2A | 192.168.255.17 |
| RE-AVD-Leaf2B | 192.168.255.18 |
| RE-AVD-BrdrLeaf1A | 192.168.255.19 |
| RE-AVD-BrdrLeaf1B | 192.168.255.20 |
| RE-AVD-L2Leaf1A | 192.168.255.21 |
| RE-AVD-L2Leaf1B | 192.168.255.22 |
| RE-AVD-L2Leaf2A | 192.168.255.23 |
| RE-AVD-L2Leaf2B | 192.168.255.24 |
| Host1 | 192.168.255.25 |
| Host2 | 192.168.255.26 |
| Host3 | 192.168.255.27 |
| Server01 | 192.168.255.28 |

## Router ID (Loopback 0)

- IP Network: 192.168.254.0/24

## VTEP (Loopback1)

!!! note Does not get applied to spine switches

- IP Network: 192.168.253.0/24

## MLAG Peer IP Pool

- IP Network: 192.168.252.0/24

## MLAG Underlay Peering IP Pool

- IP Network: 192.168.251.0/24

## Uplink IP Pool

- IP Network: 192.168.0.0/23

## Virtual Router

- MAC Address: 00:1c:73:00:dc:01

<br>
<br>

---

## Tenant Networking

- MAC VRF VNI Base: 10000

## VRFs

### VRF Internet

- VRF VNI: 999
- VTEP Diagnostic Loopback: 999

#### Interfaces

- RE-AVD-BrdrLeaf1A: Ethernet7 (192.168.20.23/23)
- RE-AVD-BrdrLeaf1B: Ethernet7 (192.168.20.24/23)

### VRF App_Zone

---

- VRF VNI: 100
- VTEP Diagnostic Loopback: 100
  - VTEP Diagnostic Loopback IP Pool: 192.168.100.0/24

#### App_Zone SVIs

- Vlan110: 192.168.110.0/24
  - IP Address Virtual: 192.168.110.1
- Vlan111: 192.168.111.0/24
  - IP Address Virtual: 192.168.111.1
- Vlan112: 192.168.112.0/24
  - IP Address Virtual: 192.168.112.1

### VRF Op_Zone

---

- VRF VNI: 200
- VTEP Diagnostic Loopback: 101
  - VTEP Diagnostic Loopback IP Poool: 192.168.101.0/24

#### Op_Zone SVIs

- Vlan120: 192.168.120.0/24
  - IP Address Virtual: 192.168.120.1
- Vlan121: 192.168.121.0/24
  - IP Address Virtual: 192.168.121.1
