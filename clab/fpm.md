# Fpm monitoring using containerlab

TODO:
- Document to Zenn in Japanese with graph diagram
  - simple multipath route add/del
- Think more test procedure for NHG increase decrease.
  - e.g. how to reduce members for a specific route?

## lab for nhg testing

Start / Stop commands:

```
cd fpm-nhg

sudo clab deploy -t topo.yaml

sudo clab destroy -t topo.yaml
```

add / del address to lo

```
docker exec -it clab-fpm-nhg-r5 ip addr add 10.99.0.0/32 dev lo
docker exec -it clab-fpm-nhg-r5 ip addr add 10.99.0.1/32 dev lo
docker exec -it clab-fpm-nhg-r5 ip addr add 10.99.0.2/32 dev lo

docker exec -it clab-fpm-nhg-r5 ip addr del 10.99.0.0/32 dev lo
docker exec -it clab-fpm-nhg-r5 ip addr del 10.99.0.1/32 dev lo
docker exec -it clab-fpm-nhg-r5 ip addr del 10.99.0.2/32 dev lo
```

```
[NEXTHOP]id 26 via 192.168.12.2 dev eth12 proto zebra
[NEXTHOP]id 27 via 192.168.13.3 dev eth13 proto zebra
[NEXTHOP]id 28 via 192.168.14.4 dev eth14 proto zebra
[NEXTHOP]id 25 group 26/27/28 proto zebra
[ROUTE]10.99.0.0 nhid 25 proto bgp metric 20

[ROUTE]10.99.0.1 nhid 25 proto bgp metric 20

[ROUTE]10.99.0.2 nhid 25 proto bgp metric 20

[ROUTE]Deleted none 10.99.0.0 proto bgp metric 20

[ROUTE]Deleted none 10.99.0.1 proto bgp metric 20

[ROUTE]Deleted none 10.99.0.2 proto bgp metric 20
```
## lab with 3 nodes

```
[fpm-logger]
     |
 [router1]net0---net0[router2]
          net1---net0[router3]
```

start

```
sudo containerlab deploy --topo fpm-3nodes.yaml

# clab inspect --name fpm-3nodes
+---+----------------------------+--------------+----------------------------------+-------+---------+----------------+----------------------+
| # |            Name            | Container ID |              Image               | Kind  |  State  |  IPv4 Address  |     IPv6 Address     |
+---+----------------------------+--------------+----------------------------------+-------+---------+----------------+----------------------+
| 1 | clab-fpm-3nodes-fpm-logger | ca38e97a14da | yutarohayakawa/fpm-logger:latest | linux | running | N/A            | N/A                  |
| 2 | clab-fpm-3nodes-router1    | 177e0dfce2e2 | frrouting/frr:latest             | linux | running | 172.20.20.6/24 | 2001:172:20:20::6/64 |
| 3 | clab-fpm-3nodes-router2    | f8d0b65221a3 | frrouting/frr:latest             | linux | running | 172.20.20.5/24 | 2001:172:20:20::5/64 |
| 4 | clab-fpm-3nodes-router3    | abd6a255194c | frrouting/frr:latest             | linux | running | 172.20.20.4/24 | 2001:172:20:20::4/64 |
+---+----------------------------+--------------+----------------------------------+-------+---------+----------------+----------------------+
```

stop

```
sudo containerlab destroy --topo fpm-3nodes.yaml
```

## see graph

1. Allow access to port 50080 `$ sudo ufw allow 50080/tcp`
2. run http server serving graph
    ```
    # clab graph -t fpm-3nodes.yaml
    INFO[0000] Parsing & checking topology file: fpm-3nodes.yaml
    INFO[0000] Serving static files from directory: /etc/containerlab/templates/graph/nextui/static
    INFO[0000] Serving topology graph on http://0.0.0.0:50080
    ```
3. access from browser `http://<host-ip>:50080/`

![clab-graph-fpm-3nodes](./clab-fpm-3nodes-01.png)
