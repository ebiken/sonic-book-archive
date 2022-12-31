# Deep Dive: SRv6 on SONiC

- [SRv6 on SONiC 機能や動作環境](#srv6-on-sonic-機能や動作環境)
  - [仕様](#仕様)
  - [SRv6 関連 HLD/PR](#srv6-関連-hldpr)
  - [Known Bugs](#known-bugs)
    - [202205 Branch で H.Encaps.Red が動作しない](#202205-branch-で-hencapsred-が動作しない)
  - [制限事項](#制限事項)
  - [Tofino Profile 変更方法](#tofino-profile-変更方法)
- [SRv6 APPL\_DB Entry 設定例](#srv6-appl_db-entry-設定例)
  - [構成図](#構成図)
  - [サーバ設定](#サーバ設定)
  - [共通設定](#共通設定)
  - [Config: H.Encaps.Red](#config-hencapsred)
  - [Config: End, End.DT46](#config-end-enddt46)
  - [パケット](#パケット)
- [SAI Objects and Flow](#sai-objects-and-flow)
  - [H.Encaps.Red (SAI Objects andFlow)](#hencapsred-sai-objects-andflow)
  - [End.DT46  (SAI Objects andFlow)](#enddt46--sai-objects-andflow)
- [Logs](#logs)

## SRv6 on SONiC 機能や動作環境

### 仕様

SONiC/SAI における SRv6 は、2017年（SAI 1.2）実装されました。
しかし、その後の SRv6 標準化進展に伴う変化や、 SAI Pipeline Model の Tunnel や MPLS との整合性を確保するため、2021年に大幅に更新されました。

- SONiC [Segment Routing over IPv6 (SRv6) HLD](https://github.com/sonic-net/SONiC/blob/master/doc/srv6/srv6_hld.md)
- SAI [SAI IPv6 Segment Routing Update](https://github.com/opencomputeproject/SAI/blob/master/doc/SAI-IPv6-Segment-Routing-Update.md)

本文書の解説は、上記ドキュメントの内容を元に実装された、 `SONiC.202111` `SAI 1.9.1` もしくはそれ以降、をベースに確認した内容を記載しています。

なお、2022年末リリース予定の `SONiC.202211` では、uSID のサポートが予定されています。

- [SONiC uSID (HLD)](https://github.com/sonic-net/SONiC/blob/master/doc/srv6/SRv6_uSID.md)

### SRv6 関連 HLD/PR

SONiC 及び SAI の関連HLD/PR

- SONiC.201803 => no feature name, no HLD
  - SAI IPv6 Segment Routing Proposal for SAI 1.2.0
  - https://github.com/opencomputeproject/SAI/blob/master/doc/SAI-Proposal-IPv6_Segment_Routing-1.md
- SONiC.202111 => SRv6 support (Cntd)
  - SONiC HLD: https://github.com/sonic-net/SONiC/blob/master/doc/srv6/srv6_hld.md
    - PR: Srv6 hld #795
      - https://github.com/sonic-net/SONiC/pull/795
      - END, END.DT46, H.Encaps.Red
  - SAI IPv6 Segment Routing Update (SAI 1.9.1)
    - https://github.com/opencomputeproject/SAI/blob/master/doc/SAI-IPv6-Segment-Routing-Update.md
    - PR: Updates to SRv6 programming model and related objects/attributes #1231
      - https://github.com/opencomputeproject/SAI/pull/1231
    - PR: Added uSID related attributes which were accidentally deleted in last c… #1261
      - https://github.com/opencomputeproject/SAI/pull/1261
- SONiC.202211 => SRv6 uSID support in SONiC dataplane - uN, uA
  - SONiC HLD: https://github.com/sonic-net/SONiC/blob/master/doc/srv6/SRv6_uSID.md
    - PR: SRv6 uSID design for srv6orch #1034
    - https://github.com/sonic-net/SONiC/pull/1034
    - uSID actions: uN, uA, uDX and uDT
  - SAI PR ... no update (uSID is part of SAI 1.9.1)
  - 

### Known Bugs

#### 202205 Branch で H.Encaps.Red が動作しない

- 202205 Branch では H.Encaps.Red を設定した際に `SAI_NEXT_HOP_TYPE_SRV6_SIDLIST` を SET する際に `SAI_STATUS_INVALID_PARAMETER` となり設定できない。（Tofino ASIC の P4 Table に Entry が作成されない）
- Master Branch ではエラー発生せず、ASIC Entry が作成される。
- Tested Binary
  - SONiC-OS-master.143513-dirty-20220903.195418
  - SONiC-OS-202205.164638-dirty-20221024.204337

```
> admin@sonic:~$ tail -f /var/log/swss/swss.rec
2022-10-31.01:59:09.745213|SRV6_SID_LIST_TABLE:seg3|SET|path:2001:db8::100,2001:db8::103
2022-10-31.01:59:09.748184|ROUTE_TABLE:Vrf_srv6:10.3.0.0/24|SET|seg_src:2001:db8:ffff::3|segment:seg3

> admin@sonic:~$ tail -f /var/log/swss/sairedis.rec
2022-10-31.01:59:09.746063|c|SAI_OBJECT_TYPE_SRV6_SIDLIST:oid:0x3d000000000386|SAI_SRV6_SIDLIST_ATTR_SEGMENT_LIST=2:2001:db8::100,2001:db8::103|SAI_SRV6_SIDLIST_ATTR_TYPE=SAI_SRV6_SIDLIST_TYPE_ENCAPS_RED
2022-10-31.01:59:09.748571|c|SAI_OBJECT_TYPE_TUNNEL:oid:0x2a000000000387|SAI_TUNNEL_ATTR_TYPE=SAI_TUNNEL_TYPE_SRV6|SAI_TUNNEL_ATTR_UNDERLAY_INTERFACE=oid:0x6000000000049|SAI_TUNNEL_ATTR_ENCAP_SRC_IP=2001:db8:ffff::3
2022-10-31.01:59:09.755477|c|SAI_OBJECT_TYPE_NEXT_HOP:oid:0x4000000000388|SAI_NEXT_HOP_ATTR_TYPE=SAI_NEXT_HOP_TYPE_SRV6_SIDLIST|SAI_NEXT_HOP_ATTR_SRV6_SIDLIST_ID=oid:0x3d000000000386|SAI_NEXT_HOP_ATTR_TUNNEL_ID=oid:0x2a000000000387
2022-10-31.01:59:09.758695|E|SAI_STATUS_INVALID_PARAMETER
```

### 制限事項

- 2022年9月現在、SRv6 は Tofino を搭載したスイッチでのみ動作します。また、SRv6を有効にするには適切な Tofino Profile を選択する必要があります。
  - Tofino Profile の選択方法は [Tofino Profile 変更方法](#tofino-profile-変更方法) を参照してください。
- 2022年9月現在、SRv6 の設定は `APPL_DB` に対して直接投入する必要があります。
  - [Segment Routing over IPv6 (SRv6) HLD](https://github.com/sonic-net/SONiC/blob/master/doc/srv6/srv6_hld.md) の `3 Feature Design` には `CONFIG_DB` や FRR/fpmsyncd からのフローが記載されていますが、サポートされていません。
- [Segment Routing over IPv6 (SRv6) HLD](https://github.com/sonic-net/SONiC/blob/master/doc/srv6/srv6_hld.md) に記載されたサンプルや [sonic-swss: doc/swss-schema.md](https://github.com/sonic-net/sonic-swss/blob/master/doc/swss-schema.md#srv6_my_sid_table) に記載されたスキーマは間違いがあります。上手く動作しない場合はこれらドキュメントだけでなく、 `swss.rec` `sairedis.rec` `syslog` 等のログを参照しながら Source Code を確認しましょう。
- `APPL_DB` エントリに不正（間違い）があると、`swss` を中心としたコンテナが再起動する事が多々あります。
  - `エントリ投入後に ASIC_DB が更新されないなど動作がおかしい場合は、 `docker ps` の `STATUS` でコンテナが再起動していないか確認の上、再起動していた場合はエントリを確認しましょう。
  - 例えば `SRV6_SID_LIST_TABLE` の `path` の値に `"2001:db8::100, 2001:db8::101"` というように `,` の後にスペースが入る違いだけで再起動します。


### Tofino Profile 変更方法

> 後日 sonic-tofino.md に移動する予定

SRv6 が動作する Tofino Profile (`SDE9.10.0`)

- Tofino: `x6_profile`
- Tofino2: `y3_profile`

Tofino Profile を指定するには、以下例のように `/etc/sonic/config_db.json` の `DEVICE_METADATA["localhost"]["p4_profile"]` に profile 名を指定して再起動（`sudo reboot`）してください。

```json
> /etc/sonic/config_db.json
{
    "DEVICE_METADATA": {
        "localhost": {
            "hwsku": "montara",
            "platform": "x86_64-accton_wedge100bf_32x-r0",
            "mac": "00:90:fb:65:d6:fe",
            "hostname": "sonic",
            "type": "LeafRouter",
            "bgp_asn": "65100",
            "p4_profile": "x6_profile"
        }
    },
...snip...
}
```

## SRv6 APPL_DB Entry 設定例

以降、サンプル構成に従った設定やパケットキャプチャの例を記載します。

SONiC APPL_DB へのエントリ設定方法
- `Config: ***` に記載された json ファイルを引数として、 swss コンテナ内（`docker exec -it swss bash`）で `swssconfig <*.json>` を実行
- コンテナ内で作成したファイルはコンテナの再起動で消えてしまう場合があるので、ホストに `/etc/sonic/swss` を作成しその中に json ファイルを作成

なお、


### 構成図

```
tofino01[Ethernet0] 10.0.0.1/24 --- [ens1f0]server         10.0.0.100/24
                    2001:db8::1/64                         2001:db8::100/64
tofino01[Ethernet4] 10.0.4.1/24 --- [ens1f1@sonic04]server 10.0.4.100/24
                    2001:db8:4::1/64                       2001:db8:4::100/64
```

### サーバ設定

```
ebiken@server:~$
sudo ip addr add 10.0.0.100/24 dev ens1f0
sudo ip route add 10.0.0.0/16 via 10.0.0.1
sudo ip addr add  2001:db8::100/64 dev ens1f0
sudo ip route add 2001:db8::/32 via 2001:db8::1

sudo ip netns add sonic04
sudo ip link set ens1f1 netns sonic04
sudo ip netns exec sonic04 ip link set ens1f1 up
sudo ip netns exec sonic04 ip addr add 10.0.4.100/24 dev ens1f1
sudo ip netns exec sonic04 ip route add 10.0.0.0/16 via 10.0.4.1
sudo ip netns exec sonic04 ip addr add 2001:db8:4::100/64 dev ens1f1
sudo ip netns exec sonic04 ip route add 2001:db8::/32 via 2001:db8:4::1
```

### 共通設定

`End.DT46` を設定する場合、事前にVRFを作成する必要があります。

```sh
admin@sonic:~$
sudo config vrf add Vrf_srv6
sudo config interface vrf bind Ethernet4 Vrf_srv6

sudo config interface ip add Ethernet0 10.0.0.1/24
sudo config interface ip add Ethernet0 2001:db8::1/64
sudo config interface ip add Ethernet4 10.0.4.1/24
sudo config interface ip add Ethernet4 2001:db8:4::1/64

admin@sonic:~$ show ip int
Interface    Master    IPv4 address/mask    Admin/Oper    BGP Neighbor    Neighbor IP
-----------  --------  -------------------  ------------  --------------  -------------
Ethernet0              10.0.0.1/24          up/up         N/A             N/A
Ethernet4    Vrf_srv6  10.0.4.1/24          up/up         N/A             N/A
```


### Config: H.Encaps.Red

- config#1：Segment List に含まれるSIDが1つ。SRHは付与されない。

```json
> encaps-red-1.json
[
    {
        "SRV6_SID_LIST_TABLE:seg1": {
            "path": "2001:db8::100"
        },
        "OP": "SET"
    },
    {
        "ROUTE_TABLE:10.1.0.0/24": {
            "segment": "seg1",
            "seg_src": "2001:db8:ffff::1"
        },
        "OP": "SET"
    }
]
```

- config#2：Segment List に含まれるSIDが2つ。SRHが付与される。

```json
> encaps-red-2.json
[
    {
        "SRV6_SID_LIST_TABLE:seg2": {
            "path": "2001:db8::100,2001:db8::102"
        },
        "OP": "SET"
    },
    {
        "ROUTE_TABLE:10.2.0.0/24": {
            "segment": "seg2",
            "seg_src": "2001:db8:ffff::2"
        },
        "OP": "SET"
    }
]
```

- config#3：Segment List に含まれるSIDが2つ。SRHが付与される。 
- `Vrf_srv6` の中に設定。Encap後は default VRF で Lookupされ Ethernet0 から送信される。

```json
> encaps-red-3.json
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

- config#4: config#3 の ECMP Route を設定しようとした場合、単純に `10.3.0.0/24` への Route Entry が上書きされる。

```json
> encaps-red-4.json
[
    {
        "SRV6_SID_LIST_TABLE:seg4": {
            "path": "2001:db8::100,2001:db8::104"
        },
        "OP": "SET"
    },
    {
        "ROUTE_TABLE:Vrf_srv6:10.3.0.0/24": {
            "segment": "seg4",
            "seg_src": "2001:db8:ffff::3"
        },
        "OP": "SET"
    }
]
```
### Config: End, End.DT46

- config#1

```json
> end.json
[
    {
        "SRV6_MY_SID_TABLE:32:32:16:0:2001:db8:ffff:1:1::": {
            "action": "end"
        },
        "OP": "SET"
    }
]
```

- config#2

```json
> end-dt46.json
[
    {
        "SRV6_MY_SID_TABLE:32:32:16:0:2001:db8:ffff:1:14::": {
            "action": "end.dt46", "vrf": "Vrf_srv6"
        },
        "OP": "SET"
    }
]
```

### パケット

TODO : `ebiken@dcig170:~/sandbox/p4sonic/pytools/sendpacket$`


## SAI Objects and Flow

### H.Encaps.Red (SAI Objects andFlow)

TODO

### End.DT46  (SAI Objects andFlow)

TODO

## Logs

```
admin@sonic:~$ docker exec -it swss bash
root@sonic:/# cd /etc/sonic/swss
root@sonic:/etc/sonic/swss# ls
encaps-red-1.json  encaps-red-2.json  end-dt46.json  end.json

root@sonic:/etc/sonic/swss#
swssconfig encaps-red-1.json
swssconfig encaps-red-2.json
swssconfig end-dt46.json
swssconfig end.json

> /var/log/swss/swss.rec

2022-09-27.10:26:25.705928|SRV6_SID_LIST_TABLE:seg1|SET|path:2001:db8::100
2022-09-27.10:26:25.708294|ROUTE_TABLE:10.99.0.0/24|SET|seg_src:2001:db8:ffff::1|segment:seg1

2022-09-27.10:26:58.691719|SRV6_SID_LIST_TABLE:seg2|SET|path:2001:db8::100,2001:db8::101
2022-09-27.10:26:58.694283|ROUTE_TABLE:10.98.0.0/24|SET|seg_src:2001:db8:ffff::1|segment:seg2

2022-09-27.10:27:25.736384|SRV6_MY_SID_TABLE:32:32:16:0:2001:db8:ffff:1:14::|SET|action:end.dt46|vrf:Vrf_srv6

2022-09-27.10:28:01.894714|SRV6_MY_SID_TABLE:32:32:16:0:2001:db8:ffff:1:1::|SET|action:end

> /var/log/swss/sairedis.rec

2022-09-27.10:26:25.706612|c|SAI_OBJECT_TYPE_SRV6_SIDLIST:oid:0x3d0000000003a4|SAI_SRV6_SIDLIST_ATTR_SEGMENT_LIST=1:2001:db8::100|SAI_SRV6_SIDLIST_ATTR_TYPE=SAI_SRV6_SIDLIST_TYPE_ENCAPS_RED
2022-09-27.10:26:25.708635|c|SAI_OBJECT_TYPE_TUNNEL:oid:0x2a0000000003a5|SAI_TUNNEL_ATTR_TYPE=SAI_TUNNEL_TYPE_SRV6|SAI_TUNNEL_ATTR_UNDERLAY_INTERFACE=oid:0x600000000004b|SAI_TUNNEL_ATTR_ENCAP_SRC_IP=2001:db8:ffff::1
2022-09-27.10:26:25.714765|c|SAI_OBJECT_TYPE_NEXT_HOP:oid:0x40000000003a6|SAI_NEXT_HOP_ATTR_TYPE=SAI_NEXT_HOP_TYPE_SRV6_SIDLIST|SAI_NEXT_HOP_ATTR_SRV6_SIDLIST_ID=oid:0x3d0000000003a4|SAI_NEXT_HOP_ATTR_TUNNEL_ID=oid:0x2a0000000003a5
2022-09-27.10:26:25.722127|C|SAI_OBJECT_TYPE_ROUTE_ENTRY||{"dest":"10.99.0.0/24","switch_id":"oid:0x21000000000000","vr":"oid:0x300000000004a"}|SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID=oid:0x40000000003a6

2022-09-27.10:26:58.692285|c|SAI_OBJECT_TYPE_SRV6_SIDLIST:oid:0x3d0000000003a7|SAI_SRV6_SIDLIST_ATTR_SEGMENT_LIST=2:2001:db8::100,2001:db8::101|SAI_SRV6_SIDLIST_ATTR_TYPE=SAI_SRV6_SIDLIST_TYPE_ENCAPS_RED
2022-09-27.10:26:58.694698|c|SAI_OBJECT_TYPE_NEXT_HOP:oid:0x40000000003a8|SAI_NEXT_HOP_ATTR_TYPE=SAI_NEXT_HOP_TYPE_SRV6_SIDLIST|SAI_NEXT_HOP_ATTR_SRV6_SIDLIST_ID=oid:0x3d0000000003a7|SAI_NEXT_HOP_ATTR_TUNNEL_ID=oid:0x2a0000000003a5
2022-09-27.10:26:58.696804|C|SAI_OBJECT_TYPE_ROUTE_ENTRY||{"dest":"10.98.0.0/24","switch_id":"oid:0x21000000000000","vr":"oid:0x300000000004a"}|SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID=oid:0x40000000003a8

2022-09-27.10:27:25.736822|c|SAI_OBJECT_TYPE_MY_SID_ENTRY:{"args_len":"0","function_len":"16","locator_block_len":"32","locator_node_len":"32","sid":"2001:db8:ffff:1:14::","switch_id":"oid:0x21000000000000","vr_id":"oid:0x300000000004a"}|SAI_MY_SID_ENTRY_ATTR_VRF=oid:0x30000000003a0|SAI_MY_SID_ENTRY_ATTR_ENDPOINT_BEHAVIOR=SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_DT46|SAI_MY_SID_ENTRY_ATTR_ENDPOINT_BEHAVIOR_FLAVOR=SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_FLAVOR_PSP_AND_USD

2022-09-27.10:28:01.895012|c|SAI_OBJECT_TYPE_MY_SID_ENTRY:{"args_len":"0","function_len":"16","locator_block_len":"32","locator_node_len":"32","sid":"2001:db8:ffff:1:1::","switch_id":"oid:0x21000000000000","vr_id":"oid:0x300000000004a"}|SAI_MY_SID_ENTRY_ATTR_ENDPOINT_BEHAVIOR=SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_E|SAI_MY_SID_ENTRY_ATTR_ENDPOINT_BEHAVIOR_FLAVOR=SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_FLAVOR_PSP_AND_USD
```
