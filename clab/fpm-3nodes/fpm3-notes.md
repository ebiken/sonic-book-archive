

## nl messages druing startup (no multipath route set)

```
$ docker logs clab-fpm-3nodes-fpm-logger  -f
[NEXTHOP]id 16 via fe80::a8c1:abff:fe82:b419 dev net1 proto zebra
[NEXTHOP]id 18 via fe80::a8c1:abff:fe1b:f1ca dev net0 proto zebra
[NEXTHOP]id 7 dev eth0 proto zebra
[NEXTHOP]id 8 dev eth0 proto zebra
[NEXTHOP]id 9 dev net1 proto zebra
[NEXTHOP]id 10 dev net0 proto zebra
[NEXTHOP]id 11 via 172.20.20.1 dev eth0 proto zebra
[NEXTHOP]id 12 via 2001:172:20:20::1 dev eth0 proto zebra
[NEXTHOP]id 14 via fe80::a8c1:abff:fe1b:f1ca dev net0 proto zebra
[ROUTE]0.0.0.0/0 nhid 11 proto kernel metric 20
[ROUTE]172.20.20.0/24 nhid 7 proto kernel metric 20
[ROUTE]::/0 nhid 16 proto kernel metric 20
[ROUTE]2001:172:20:20::/64 nhid 8 proto kernel metric 20
[ROUTE]fe80::/64 nhid 8 proto kernel metric 20
```

## Config

### router1

```
bash-5.1# vtysh -c "show run"
Building configuration...

Current configuration:
!
frr version 8.4_git
frr defaults traditional
hostname router1
no ipv6 forwarding
fpm address 127.0.0.1
!
router bgp 65001
 bgp router-id 10.0.0.1
 no bgp ebgp-requires-policy
 neighbor PEERS peer-group
 neighbor PEERS remote-as external
 neighbor PEERS capability extended-nexthop
 neighbor net0 interface peer-group PEERS
 neighbor net1 interface peer-group PEERS
exit
!
end
```