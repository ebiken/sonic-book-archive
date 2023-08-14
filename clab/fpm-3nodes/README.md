# lab with 3 nodes

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