# Next Hop on SONiC

> Detailed description should be documented under [/doc](/doc/)

- [Next Hop Group in APPL\_DB: NEXT\_HOP\_GROUP\_TABLE](#next-hop-group-in-appl_db-next_hop_group_table)
  - [Add Next Hop Group to APPL\_DB](#add-next-hop-group-to-appl_db)
  - [Remove entry from APPL\_DB NEXTHOP\_GROUP\_TABLE](#remove-entry-from-appl_db-nexthop_group_table)
  - [Add ROUTE entry with Next Hop Group](#add-route-entry-with-next-hop-group)
  - [memo](#memo)

Next Hop Groups can be configured in two ways.

- configure two or more nexthop to same prefix
  - CLI available:
    -  `admin@sonic:~$ sudo config route add prefix 10.99.0.0/24 nexthop 10.0.0.100`
    -  `admin@sonic:~$ sudo config route add prefix 10.99.0.0/24 nexthop 10.0.0.101`
- create Next Hop Group Object in APPL_DB `NEXT_HOP_GROUP_TABLE`
  - CLI NOT available
  - described in: [HLD: Routing and Next Hop Table Enhancement](https://github.com/sonic-net/SONiC/blob/master/doc/ip/next_hop_group_hld.md)


## Next Hop Group in APPL_DB: NEXT_HOP_GROUP_TABLE

### Add Next Hop Group to APPL_DB

Python Script to add entry to APPL_DB NEXTHOP_GROUP_TABLE

```
admin@sonic:~/script$ cat nhg_push_appldb.py
#!/usr/bin/python3

from swsscommon import swsscommon

db = swsscommon.DBConnector("APPL_DB", 0, True)
table = swsscommon.ProducerStateTable(db, "NEXTHOP_GROUP_TABLE")

key = "nhg1"
fieldValues = {"nexthop": "10.0.0.100,10.0.0.101", "ifname": "Ethernet0,Ethernet0"}
fvs = swsscommon.FieldValuePairs(list(fieldValues.items()))
table.set(key, fvs)
```

Log: Console

```
> Run after reboot (no Next Hop Group Entry)
admin@sonic:~$ sonic-db-cli ASIC_DB keys \* | grep NEXT
admin@sonic:~$ sonic-db-cli APPL_DB keys \* | grep NEXT
admin@sonic:~$
admin@sonic:~$ cd script/
admin@sonic:~/script$ ./nhg_push_appldb.py
admin@sonic:~/script$ sonic-db-cli APPL_DB keys \* | grep NEXT
NEXTHOP_GROUP_TABLE:nhg1
admin@sonic:~/script$ sonic-db-cli APPL_DB HGETALL NEXTHOP_GROUP_TABLE:nhg1
{'nexthop': '10.0.0.100,10.0.0.101', 'ifname': 'Ethernet0,Ethernet0'}

admin@sonic:~/script$ sonic-db-cli ASIC_DB keys \* | grep NEXT
ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER:oid:0x2d0000000003a9
ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP_GROUP:oid:0x50000000003a8
ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER:oid:0x2d0000000003aa
ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP:oid:0x40000000003a7
ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP:oid:0x40000000003a5

admin@sonic:~/script$ sonic-db-cli ASIC_DB HGETALL ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP_GROUP:oid:0x50000000003a8
{'SAI_NEXT_HOP_GROUP_ATTR_TYPE': 'SAI_NEXT_HOP_GROUP_TYPE_DYNAMIC_UNORDERED_ECMP'}
admin@sonic:~/script$ sonic-db-cli ASIC_DB HGETALL ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER:oid:0x2d0000000003a9
{'SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_GROUP_ID': 'oid:0x50000000003a8', 'SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_ID': 'oid:0x40000000003a5'}
admin@sonic:~/script$ sonic-db-cli ASIC_DB HGETALL ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER:oid:0x2d0000000003aa
{'SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_GROUP_ID': 'oid:0x50000000003a8', 'SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_ID': 'oid:0x40000000003a7'}
admin@sonic:~/script$ sonic-db-cli ASIC_DB HGETALL ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP:oid:0x40000000003a5
{'SAI_NEXT_HOP_ATTR_TYPE': 'SAI_NEXT_HOP_TYPE_IP', 'SAI_NEXT_HOP_ATTR_IP': '10.0.0.100', 'SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID': 'oid:0x60000000003a1'}
admin@sonic:~/script$ sonic-db-cli ASIC_DB HGETALL ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP:oid:0x40000000003a7
{'SAI_NEXT_HOP_ATTR_TYPE': 'SAI_NEXT_HOP_TYPE_IP', 'SAI_NEXT_HOP_ATTR_IP': '10.0.0.101', 'SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID': 'oid:0x60000000003a1'}
```

Log: swss.rec / sairedis.rec

> TODO: SAI_OBJECT_TYPE_NEXT_HOP_GROUP is created(c) and removed(r) two times before last one is created

```
> admin@sonic:/var/log/swss$ tail -f swss.rec
2022-11-23.03:51:31.427065|NEXTHOP_GROUP_TABLE:nhg1|SET|nexthop:10.0.0.100,10.0.0.101|ifname:Ethernet0,Ethernet0
2022-11-23.03:51:31.439272|NEIGH_TABLE:Ethernet0:10.0.0.100|SET|neigh:0c:42:a1:46:64:a2|family:IPv4
2022-11-23.03:51:31.448339|NEIGH_TABLE:Ethernet0:10.0.0.101|SET|neigh:0c:42:a1:46:64:a2|family:IPv4

> admin@sonic:/var/log/swss$ tail -f sairedis.rec
2022-11-23.03:51:31.427527|c|SAI_OBJECT_TYPE_NEXT_HOP_GROUP:oid:0x50000000003a3|SAI_NEXT_HOP_GROUP_ATTR_TYPE=SAI_NEXT_HOP_GROUP_TYPE_DYNAMIC_UNORDERED_ECMP
2022-11-23.03:51:31.432960|r|SAI_OBJECT_TYPE_NEXT_HOP_GROUP:oid:0x50000000003a3
2022-11-23.03:51:31.435818|c|SAI_OBJECT_TYPE_NEXT_HOP_GROUP:oid:0x50000000003a4|SAI_NEXT_HOP_GROUP_ATTR_TYPE=SAI_NEXT_HOP_GROUP_TYPE_DYNAMIC_UNORDERED_ECMP
2022-11-23.03:51:31.437392|r|SAI_OBJECT_TYPE_NEXT_HOP_GROUP:oid:0x50000000003a4
2022-11-23.03:51:31.439566|c|SAI_OBJECT_TYPE_NEIGHBOR_ENTRY:{"ip":"10.0.0.100","rif":"oid:0x60000000003a1","switch_id":"oid:0x21000000000000"}|SAI_NEIGHBOR_ENTRY_ATTR_DST_MAC_ADDRESS=0C:42:A1:46:64:A2
2022-11-23.03:51:31.441707|c|SAI_OBJECT_TYPE_NEXT_HOP:oid:0x40000000003a5|SAI_NEXT_HOP_ATTR_TYPE=SAI_NEXT_HOP_TYPE_IP|SAI_NEXT_HOP_ATTR_IP=10.0.0.100|SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID=oid:0x60000000003a1
2022-11-23.03:51:31.443844|c|SAI_OBJECT_TYPE_NEXT_HOP_GROUP:oid:0x50000000003a6|SAI_NEXT_HOP_GROUP_ATTR_TYPE=SAI_NEXT_HOP_GROUP_TYPE_DYNAMIC_UNORDERED_ECMP
2022-11-23.03:51:31.445600|r|SAI_OBJECT_TYPE_NEXT_HOP_GROUP:oid:0x50000000003a6
2022-11-23.03:51:31.448575|c|SAI_OBJECT_TYPE_NEIGHBOR_ENTRY:{"ip":"10.0.0.101","rif":"oid:0x60000000003a1","switch_id":"oid:0x21000000000000"}|SAI_NEIGHBOR_ENTRY_ATTR_DST_MAC_ADDRESS=0C:42:A1:46:64:A2
2022-11-23.03:51:31.451010|c|SAI_OBJECT_TYPE_NEXT_HOP:oid:0x40000000003a7|SAI_NEXT_HOP_ATTR_TYPE=SAI_NEXT_HOP_TYPE_IP|SAI_NEXT_HOP_ATTR_IP=10.0.0.101|SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID=oid:0x60000000003a1
2022-11-23.03:51:31.452526|c|SAI_OBJECT_TYPE_NEXT_HOP_GROUP:oid:0x50000000003a8|SAI_NEXT_HOP_GROUP_ATTR_TYPE=SAI_NEXT_HOP_GROUP_TYPE_DYNAMIC_UNORDERED_ECMP
2022-11-23.03:51:31.454082|C|SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER
||oid:0x2d0000000003a9|SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_GROUP_ID=oid:0x50000000003a8|SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_ID=oid:0x40000000003a5
||oid:0x2d0000000003aa|SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_GROUP_ID=oid:0x50000000003a8|SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_ID=oid:0x40000000003a7
```

### Remove entry from APPL_DB NEXTHOP_GROUP_TABLE

> TODO: ASIC_DB entry would not be deleted on SONiC-OS-master.143513-dirty-20220903.195418

```
admin@sonic:~/script$ sonic-db-cli APPL_DB del HGETALL NEXTHOP_GROUP_TABLE:nhg1
1

> No log logged in swss.rec / sairedis.rec
admin@sonic:~/script$ sonic-db-cli APPL_DB keys \* | grep NEXT
admin@sonic:~/script$
admin@sonic:~/script$ sonic-db-cli ASIC_DB keys \* | grep NEXT
ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER:oid:0x2d0000000003a9
ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP_GROUP:oid:0x50000000003a8
ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER:oid:0x2d0000000003aa
ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP:oid:0x40000000003a7
ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP:oid:0x40000000003a5

admin@sonic:~/script$ sudo sonic-installer list
Current: SONiC-OS-master.143513-dirty-20220903.195418
```

### Add ROUTE entry with Next Hop Group

Python Script to add entry to APPL_DB NEXTHOP_GROUP_TABLE

> prerequisit is you have already created entry in NEXT_HOP_GROUP_TABLE with key `nhg1`

```
admin@sonic:~/script$ cat nhg-route_push_appldb.py
#!/usr/bin/python3
from swsscommon import swsscommon

db = swsscommon.DBConnector("APPL_DB", 0, True)

pstable = swsscommon.ProducerStateTable(db, "ROUTE_TABLE")
key = "10.88.0.0/24"
fieldValues = {"nexthop_group": "nhg1"}
fvs = swsscommon.FieldValuePairs(list(fieldValues.items()))
pstable.set(key, fvs)

admin@sonic:~/script$ ./nhg-route_push_appldb.py
```

Log: Console

```
admin@sonic:~/script$ sonic-db-cli APPL_DB HGETALL ROUTE_TABLE:10.88.0.0/24
{'nexthop_group': 'nhg1'}

admin@sonic:~/script$ sonic-db-cli APPL_DB keys \* | grep NEXT
NEXTHOP_GROUP_TABLE:nhg1
admin@sonic:~/script$ sonic-db-cli ASIC_DB keys \* | grep NEXT
ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP_GROUP:oid:0x50000000003a8
ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP:oid:0x40000000003a7
ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER:oid:0x2d0000000003a9
ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER:oid:0x2d0000000003aa
ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP:oid:0x40000000003a5
```

Add 2nd ROUTE entry

```
admin@sonic:~/script$ cat nhg-route99_push_appldb.py
#!/usr/bin/python3
from swsscommon import swsscommon

db = swsscommon.DBConnector("APPL_DB", 0, True)

pstable = swsscommon.ProducerStateTable(db, "ROUTE_TABLE")
key = "10.99.0.0/24"
fieldValues = {"nexthop_group": "nhg1"}
fvs = swsscommon.FieldValuePairs(list(fieldValues.items()))
pstable.set(key, fvs)

admin@sonic:~/script$ ./nhg-route99_push_appldb.py
```

Log: Console

```
admin@sonic:~/script$ sonic-db-cli APPL_DB HGETALL ROUTE_TABLE:10.99.0.0/24
{'nexthop_group': 'nhg1'}
admin@sonic:~/script$ sonic-db-cli APPL_DB HGETALL ROUTE_TABLE:10.88.0.0/24
{'nexthop_group': 'nhg1'}
admin@sonic:~/script$ sonic-db-cli APPL_DB keys \* | grep NEXT
NEXTHOP_GROUP_TABLE:nhg1
admin@sonic:~/script$ sonic-db-cli APPL_DB HGETALL NEXTHOP_GROUP_TABLE:nhg1
{'nexthop': '10.0.0.100,10.0.0.101', 'ifname': 'Ethernet0,Ethernet0'}

admin@sonic:~/script$ sonic-db-cli ASIC_DB keys \* | grep ROUTE
...snip...
ASIC_STATE:SAI_OBJECT_TYPE_ROUTE_ENTRY:{"dest":"10.88.0.0/24","switch_id":"oid:0x21000000000000","vr":"oid:0x300000000004a"}
ASIC_STATE:SAI_OBJECT_TYPE_ROUTE_ENTRY:{"dest":"10.99.0.0/24","switch_id":"oid:0x21000000000000","vr":"oid:0x300000000004a"}

admin@sonic:~/script$ sonic-db-cli ASIC_DB HGETALL 'ASIC_STATE:SAI_OBJECT_TYPE_ROUTE_ENTRY:{"dest":"10.88.0.0/24","switch_id":"oid:
0x21000000000000","vr":"oid:0x300000000004a"}'
{'SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID': 'oid:0x50000000003a8'}
admin@sonic:~/script$ sonic-db-cli ASIC_DB HGETALL 'ASIC_STATE:SAI_OBJECT_TYPE_ROUTE_ENTRY:{"dest":"10.99.0.0/24","switch_id":"oid:
0x21000000000000","vr":"oid:0x300000000004a"}'
{'SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID': 'oid:0x50000000003a8'}

admin@sonic:~/script$ sonic-db-cli ASIC_DB keys \* | grep NEXT
ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP_GROUP:oid:0x50000000003a8
ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP:oid:0x40000000003a7
ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER:oid:0x2d0000000003a9
ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER:oid:0x2d0000000003aa
ASIC_STATE:SAI_OBJECT_TYPE_NEXT_HOP:oid:0x40000000003a5
```


### memo

From [HLD: Routing and Next Hop Table Enhancement](https://github.com/sonic-net/SONiC/blob/master/doc/ip/next_hop_group_hld.md)

```
create next hop group
add next hop group member for each next hop
sai_id = sai ID of the next hop group
```

- next hop group 内の next hop が１つでも next hop group を作成する
  - HLDには1つの場合は next hop group を作成しないと記載されているが、HLD側の document bug
  - https://github.com/sonic-net/SONiC/issues/1100
- orchagent が APPL_DB から読み取ったあと、ASIC_DB に 1. next hop group の追加 2. next hop group member の追加 の順でエントリを作成する
  - the next hop group orchagent will add a next hop group to ASIC_DB and then add a next hop group member to ASIC_DB for every member of that group that is available to be used. Changes to the membership of the group will result in next hop group members being added to or removed from ASIC_DB.
- next hop group orchagent が APPL_DB の oid と SAI id の対応を管理している
  - The next hop group orchagent will then maintain an association between the identifer of the group from APP_DB and the SAI identifier assigned to the next hop group
