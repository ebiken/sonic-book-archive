# Redis DB (redisdb)

Redis DB (redisdb) 周辺でデバッグ等をする際に必要な情報を記載

> Redis Database の概要は [SONiCを学ぶための前提知識 > RedisDB](prerequisites.md#redis-db) を参照

- [SONiC で使用されている DB の種類](#sonic-で使用されている-db-の種類)
- [エントリのフォーマット](#エントリのフォーマット)
  - [ASIC_TEMPERATURE_INFO_TABLE_NAME](#asic_temperature_info_table_name)
- [redisdb への読み書き](#redisdb-への読み書き)
  - [APPL_DB への書き込み：swssconfig](#appl_db-への書き込みswssconfig)
  - [TODO: redis-cli を利用した読み書き](#todo-redis-cli-を利用した読み書き)
  - [TODO: python を利用した読み書き](#todo-python-を利用した読み書き)
- [出力サンプル](#出力サンプル)
  - [redis-cli 出力サンプル](#redis-cli-出力サンプル)
  - [sonic-db-cli 出力サンプル](#sonic-db-cli-出力サンプル)

## SONiC で使用されている DB の種類

redisdb に含まれるデータベースは、 `dbid` で識別されます。
また、SONiC ではそれぞれのDBに名前がついています。
SONiCのDB名と `dbid` の対応は以下場所で確認できます。

- [GitHub: sonic-swss-common/common/schema.h](https://github.com/sonic-net/sonic-swss-common/blob/master/common/schema.h)
- SONiC Host: `/var/run/redis/sonic-db/database_config.json`

`sonic-db-cli` ではDB名で指定できますが、デバッグ時など redisdb を直接操作する際には以下表を元に dbid を指定してください。

| redis dbid | sonic db name      |
| :--------: | :----------------- |
|     0      | APPL_DB            |
|     1      | ASIC_DB            |
|     2      | COUNTERS_DB        |
|     3      | LOGLEVEL_DB        |
|     4      | CONFIG_DB          |
|     5      | PFC_WD_DB          |
|     5      | FLEX_COUNTER_DB    |
|     6      | STATE_DB           |
|     7      | SNMP_OVERLAY_DB    |
|     8      | RESTAPI_DB         |
|     9      | GB_ASIC_DB         |
|     10     | GB_COUNTERS_DB     |
|     11     | GB_FLEX_COUNTER_DB |
|     12     | CHASSIS_APP_DB     |
|     13     | CHASSIS_STATE_DB   |
|     14     | APPL_STATE_DB      |

## エントリのフォーマット

[GitHub: sonic-swss-common/common/schema.h](https://github.com/sonic-net/sonic-swss-common/blob/master/common/schema.h) に記載されるように、各DB毎にテーブルが定義されています。

この "テーブル" は redisdb としては Key の一部になっており、key = `<TABLE_NAME>:<object_name1>[:<object_name2> ...]` というフォーマットとなります。

なお、 `ASIC_DB` に含まれる `<TABLE_NAME>` は `ASIC_STATE` のみであるため定義はありません。（`ASIC_TEMPERATURE_INFO_TABLE_NAME` については後述の [ASIC_TEMPERATURE_INFO_TABLE_NAME](#asic_temperature_info_table_name) を参照）

`<TABLE_NAME>` と `<object_name>` の間のセパレータは `:` または `|` が使用されます。
各DBで利用しているセパレータは `database_config.json` に定義されています。

例：[sonic-swss-common /common/database_config.json](https://github.com/sonic-net/sonic-swss-common/blob/master/common/database_config.json) から抜粋

```json
    "DATABASES" : {
        "APPL_DB" : {
            "id" : 0,
            "separator": ":",
            "instance" : "redis"
        },
        "ASIC_DB" : {
            "id" : 1,
            "separator": ":",
            "instance" : "redis"
        },
...
        "CONFIG_DB" : {
            "id" : 4,
            "separator": "|",
            "instance" : "redis"
        },
...
        "STATE_DB" : {
            "id" : 6,
            "separator": "|",
            "instance" : "redis"
        },
```

### ASIC_TEMPERATURE_INFO_TABLE_NAME

[GitHub: sonic-swss-common/common/schema.h](https://github.com/sonic-net/sonic-swss-common/blob/master/common/schema.h) には、以下の通り `ASIC DATABASE` というコメントの下に `ASIC_TEMPERATURE_INFO_TABLE_NAME` が含まれますが、これはソースコードを参照すると `ASIC_DB` ではなく `STATE_DB` に保存されているようです。

参考：[ASIC thermal monitoring High Level Design](https://github.com/sonic-net/SONiC/blob/master/doc/asic_thermal_monitoring_hld.md)

```c++
// https://github.com/sonic-net/sonic-swss-common/blob/master/common/schema.h

/***** ASIC DATABASE *****/
#define ASIC_TEMPERATURE_INFO_TABLE_NAME    "ASIC_TEMPERATURE_INFO"

// https://github.com/sonic-net/sonic-swss/blob/master/orchagent/switchorch.cpp

SwitchOrch::SwitchOrch(DBConnector *db, vector<TableConnector>& connectors, TableConnector switchTable):
        Orch(connectors),
        m_switchTable(switchTable.first, switchTable.second),
        m_db(db),
        m_stateDb(new DBConnector(STATE_DB, DBConnector::DEFAULT_UNIXSOCKET, 0)),
        m_asicSensorsTable(new Table(m_stateDb.get(), ASIC_TEMPERATURE_INFO_TABLE_NAME)),
    //                     ^^^^^^^^^ m_stateDb => STATE_DB ^^^^^
```

## redisdb への読み書き

### APPL_DB への書き込み：swssconfig

swss container 内で swssconfig コマンドを利用して、APPL_DB へ JSON で記述したエントリを投入する事が可能です。
以下にSRv6設定をサンプルとして記載します。

```
> Enter swss container

admin@sonic:~$ docker exec -it swss bash

> Create files (Copy&Paste JSON sample)

root@sonic:/# vi end-dt46.json
root@sonic:/# vi encaps-red-3.json

> Insert Entries using command: swssconfig

root@sonic:/# swssconfig end-dt46.json
root@sonic:/# swssconfig encaps-red-3.json
```

`docker cp` でファイルをコピーしてホスト上で実行する事も可能です。

```
$ cat ~/srv6.json
docker cp srv6.json swss:.
docker exec -it swss swssconfig srv6.json
```

APPL_DB JSON サンプル

- End.DT46 : end-dt46.json

```json
[
  {
    "SRV6_MY_SID_TABLE:32:32:16:0:2001:db8:ffff:1:14::": {
      "action": "end.dt46", "vrf": "Vrf_srv6"
    },
    "OP": "SET"
  }
]

```

- H.Encaps.Red : encaps-red-3.json

```json
[
  {
    "SRV6_SID_LIST_TABLE:seg3": {
      "path": "2001:db8::100,2001:db8::103"
    },
    "OP": "SET"
  },
  {
    "ROUTE_TABLE:Vrf_srv6:10.3.0.0/24": {
      "segment": "seg3",
      "seg_src": "2001:db8:ffff::3"
    },
    "OP": "SET"
  }
]
```

### TODO: redis-cli を利用した読み書き

### TODO: python を利用した読み書き


## 出力サンプル

### redis-cli 出力サンプル

Redis Database has IDs: `sonic:/var/run/redis/sonic-db/database_config.json`

Check DB ID which is keyspace.

```shell
admin@sonic:~$redis-cli
127.0.0.1:6379> INFO keyspace
# Keyspace
db0:keys=56,expires=0,avg_ttl=0
db1:keys=916,expires=0,avg_ttl=0
db2:keys=1924,expires=0,avg_ttl=0
db3:keys=67,expires=0,avg_ttl=0
db4:keys=123,expires=0,avg_ttl=0
db5:keys=980,expires=0,avg_ttl=0
db6:keys=485,expires=0,avg_ttl=0
db11:keys=1,expires=0,avg_ttl=0

- 0 : APPL_DB
- 1 : ASIC_DB
- 2 : COUNTERS_DB
- 3 : LOGLEVEL_DB
- 4 : CONFIG_DB
- 5 : PFC_WD_DB
- 5 : FLEX_COUNTER_DB
- 6 : STATE_DB
- 11 : GB_FLEX_COUNTER_DB
```

select keyspace (DB ID)

```shell
> ASIC_DB
127.0.0.1:6379> select 1
127.0.0.1:6379[1]> keys *
  1) "ASIC_STATE:SAI_OBJECT_TYPE_QUEUE:oid:0x1500000000034b"
  2) "ASIC_STATE:SAI_OBJECT_TYPE_SCHEDULER_GROUP:oid:0x17000000000091"
  3) "ASIC_STATE:SAI_OBJECT_TYPE_INGRESS_PRIORITY_GROUP:oid:0x1a000000000132"

> CONFIG_DB
127.0.0.1:6379> select 4
127.0.0.1:6379[4]> keys *
  1) "FLEX_COUNTER_TABLE|BUFFER_POOL_WATERMARK"
  2) "FEATURE|database"
  3) "FEATURE|mux"
...snip...
121) "PORT|Ethernet116"
122) "PORT|Ethernet68"
123) "PORT|Ethernet56"
```

show value for a key

```shell
127.0.0.1:6379[4]> HGETALL "PORT|Ethernet56"
 1) "admin_status"
 2) "up"
 3) "alias"
 4) "Ethernet56"
 5) "autoneg"
 6) "off"
 7) "fec"
 8) "rs"
 9) "index"
10) "15"
11) "lanes"
12) "56,57,58,59"
13) "mtu"
14) "9100"
15) "speed"
16) "100000"
```

### sonic-db-cli 出力サンプル

TBD