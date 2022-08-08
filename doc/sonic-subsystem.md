# 各サブシステムやモジュールの役割

> TODO: 各モジュールの役割を、「どのようなデータをどこから受信し、どのように変換しどこに送信（格納）するか」という視点で整理する。

SONiCのサブシステム（コンテナ）及びモジュール（コンテナ内で動作するプログラム）について整理します。
なお、CLI / sonic-cfggen はコンテナではなくホストOS上で動作しますが、サブシステムのひとつとして取り上げます。


- [SONiCモジュール早見表（Google Sheet）](https://docs.google.com/spreadsheets/d/1y6wvmaf2lNlvuFa4NUT0QDLK0qFjpBQqxqKOEBCPkA4/)
  - [sonic-buildimage /dockers](https://github.com/sonic-net/sonic-buildimage/tree/master/dockers) のうち主要なものだけを記載。順次必要なコンテナを追加する）

目次
- [起動するサブシステム（コンテナ）とモジュールの確認方法](#起動するサブシステムコンテナとモジュールの確認方法)
- [CLI / sonic-cfggen](#cli--sonic-cfggen)
- [database](#database)
  - [redis-server](#redis-server)
- [syncd](#syncd)
  - [syncd](#syncd-1)
- [swss (Switch State Service)](#swss-switch-state-service)
  - [orchagent](#orchagent)
  - [portsyncd](#portsyncd)
  - [neighsyncd](#neighsyncd)
  - [fdbsyncd](#fdbsyncd)
  - [gearsyncd](#gearsyncd)
  - [coppmgrd](#coppmgrd)
  - [vlanmgrd](#vlanmgrd)
  - [intfmgrd](#intfmgrd)
  - [portmgrd](#portmgrd)
  - [buffermgrd](#buffermgrd)
  - [vrfmgrd](#vrfmgrd)
  - [nbrmgrd](#nbrmgrd)
  - [vxlanmgrd](#vxlanmgrd)
  - [tunnelmgrd](#tunnelmgrd)
- [teamd](#teamd)
  - [teammgrd](#teammgrd)
  - [tlm_teamd](#tlm_teamd)
  - [teamsyncd](#teamsyncd)
- [snmp](#snmp)
  - [snmpd](#snmpd)
  - [snmp-subagent (sonic_ax_impl)](#snmp-subagent-sonic_ax_impl)
- [mgmt-framework (SONiC Management Framework)](#mgmt-framework-sonic-management-framework)
  - [rest-server](#rest-server)
- [telemetry](#telemetry)
  - [telemetry](#telemetry-1)
  - [dialout](#dialout)
- [pmon (Platform Monitoring)](#pmon-platform-monitoring)
  - [pmon の各種モジュールの起動制御](#pmon-の各種モジュールの起動制御)
  - [`Wedge100BF-32` で起動している pmon 関連モジュール（サンプル）](#wedge100bf-32-で起動している-pmon-関連モジュールサンプル)
- [lldp](#lldp)
  - [lldpd](#lldpd)
  - [lldp_syncd](#lldp_syncd)
  - [lldpmgrd](#lldpmgrd)
- [radv (Router Advertiser)](#radv-router-advertiser)
- [bgp (docker-fpm-frr)](#bgp-docker-fpm-frr)
  - [起動するモジュールの違いとシーケンス](#起動するモジュールの違いとシーケンス)
  - [fpmsyncd](#fpmsyncd)
  - [bgpmon](#bgpmon)
  - [zebra](#zebra)
  - [staticd](#staticd)
  - [bgpd](#bgpd)
  - [bgpcfgd](#bgpcfgd)


## 起動するサブシステム（コンテナ）とモジュールの確認方法

SONiCで起動しているサブシステム（コンテナ）やモジュール（プロセス・デーモン）を確認するには、SONiC 上で `docker ps` や `docker exec -it <container_name> ps a` 等のコマンドを実行する事で確認できます。
しかし、起動するサブシステムはビルド設定や起動時の設定に依存するため、上記コマンドで確認できるもの以外も起動する可能性があります。

SONiCに含まれるサブシステム（コンテナ）は [sonic-buildimage /dockers](https://github.com/sonic-net/sonic-buildimage/tree/master/dockers) に集約されています。
なお、 `docker-base-<debian_release_name>` のようにコンテナを作るためのベースコンテナとして利用されるものや、 `docker-fpm-gobgp` のようにデフォルトのビルド設定では作成されないコンテナも存在します。
また、 `docker-xxx` というイメージ名（Docker Image Name）と、コンテナ名は異なるため、知っていないと類推できないものもあります。
例えば `swss container` のイメージ名は `docker-orchagent` 、 `bgp container` は `docker-fpm-frr` となります。

サブシステム（コンテナ）内で起動されるモジュールは各フォルダ内の `supervisord.conf`, `[<docker-name>.]supervisord.conf.j2` を参照する事である程度把握することが可能です。
例えば `snmp container` の場合、 起動用の `start.sh` スクリプトと `rsyslogd` を除き、 `snmpd`, `snmp-subagent (python3 -m sonic_ax_impl)` ２つのSNMP関連モジュールがコンテナ内で起動する事が確認できます。

```
sonic-buildimage/dockers/docker-snmp$ grep -1 program supervisord.conf

[program:rsyslogd]
command=/usr/sbin/rsyslogd -n -iNONE

[program:start]
command=/usr/bin/start.sh

[program:snmpd]
command=/usr/sbin/snmpd -f -LS0-2d -u Debian-snmp -g Debian-snmp -I -smux,mteTrigger,mteTriggerConf,ifTable,ifXTable,inetCidrRouteTable,ipCidrRouteTable,ip,disk_hw -p /run/snmpd.pid

[program:snmp-subagent]
command=/usr/bin/env python3 -m sonic_ax_impl
```

## CLI / sonic-cfggen

> MEMO (後で消す)
> - Click (Python) ベースの CLI
>   - Click から `sonic_cfggen` 経由で `CONFIG_DB` や、 `CONFIG_DB` を利用しないモジュールの設定（ファイル）を操作する
>     - （TODO: どの操作がどのパスを通るか確認して更新）
>   - SONiC の CLI といえば（まだ）これで、多くのコマンドをサポートしている
>   - Source Code:
>     - `cli.py`: https://github.com/sonic-net/sonic-utilities/tree/master/utilities_common
>     - `sonic-cfggen`: https://github.com/sonic-net/sonic-buildimage/tree/master/src/sonic-config-engine
>   - コマンドリファレンス：https://github.com/sonic-net/sonic-utilities/blob/master/doc/Command-Reference.md

## database

### redis-server

## syncd

### syncd

## swss (Switch State Service)

Switch State Service の略である `swss container` は `database container` と共に SONiC システムの中核に位置し、各サブシステムやコンポーネント間を仲介する役割を担う、多くのモジュールから構成されます。

`swss container` に含まれる各モジュール一覧

- orchagent
- portsyncd
- neighsyncd
- fdbsyncd
- gearsyncd
- coppmgrd
- vlanmgrd
- intfmgrd
- portmgrd
- buffermgrd
- vrfmgrd
- nbrmgrd
- vxlanmgrd
- tunnelmgrd

### orchagent

https://github.com/sonic-net/sonic-swss/tree/master/orchagent

ポイント

- `/orchagent/main.cpp` が `/usr/bin/orchagent` として実行される。
- `orchDaemon` がデーモンとしての処理実装
- 以下３つのDBと接続する
  - DBConnector appl_db("APPL_DB", 0);
  - DBConnector config_db("CONFIG_DB", 0);
  - DBConnector state_db("STATE_DB", 0);
- `/orchagent/` の下には様々な `*.cpp` プログラムがあるが、必ずしも orchagent の一部ではなく、コマンドとして実行可能なものもある（例： `routeresync.cpp`）
- orchDaemon.h で `#include` されている `XXXorch.h` が実際の変換ロジックの実装
  - `class Srv6Orch : public Orch` のように、`XxxOrch` クラスが各ファイルで定義され、`orchDaemon` で `gSrv6Orch = new Srv6Orch(m_applDb, srv6_tables, gSwitchOrch, vrf_orch, gNeighOrch);` のようにインスタンス化されている。
  - `XxxOrch` のインスタンスは `orchdaemon.cpp: bool OrchDaemon::init()` で `m_orchList.push_back(gFdbOrch);` のように `m_orchList` に保存される。
- `for (Orch *o : m_orchList) { o->doTask(); }` のように、各クラスの `doTask()` ループが実行される
- 


メモ

- `routeresync.cpp`
  - `routersync start|stop` を実行すると `APPL_DB` に `ROUTE_TABLE:resync` エントリを追加・削除する。

### portsyncd

### neighsyncd

### fdbsyncd

### gearsyncd

### coppmgrd

### vlanmgrd

### intfmgrd

### portmgrd

### buffermgrd

### vrfmgrd

### nbrmgrd

### vxlanmgrd

### tunnelmgrd

## teamd

### teammgrd

### tlm_teamd

### teamsyncd

## snmp
### snmpd
### snmp-subagent (sonic_ax_impl)

## mgmt-framework (SONiC Management Framework)

> MEMO (後で消す)
> - Klish ベースの CLI
>   - Klish から Framework の REST API 経由で `CONFIG_DB` を操作する
>     - Klish は Cisco IOS Like な CLI を生成するフレームワーク
>   - サポートしているコマンドは限定的
>   - 2019年から開発が進められている、 [SONiC Management Framework (HLD)](https://github.com/sonic-net/SONiC/blob/master/doc/mgmt/Management%20Framework.md) の一部
>   - Source Code: https://github.com/sonic-net/sonic-mgmt-framework/tree/master/CLI/klish

### rest-server

## telemetry

### telemetry

### dialout
dialout_client_cli

## pmon (Platform Monitoring)

> - TODO：モニタリングフレームワークがこれ以外にもあるか調査。もしくはODMもしくはASICベンダ提供のツールを利用している？
> - 機種依存が多そうなので、実機ベースで再度調査する。

`pmon container` は名前の通り、プラットフォームを関するモジュールが含まれています。
`docker-pmon.supervisord.conf.j2` に記述されているモジュール一覧は以下の通りです。

なお、bash の場合、実際にデバイスにアクセスしているプログラムを更に呼び出している場合がありますので、詳細はさらにコードの中身を調査する必要があります。

- `[program:chassisd]` python3
  - Module information update daemon for SONiC
  - This daemon will loop to collect all modules related information and then write the information to state DB.
  - CHASSIS_INFO_UPDATE_PERIOD_SECS (10秒) 毎にループ
- `[program:chassis_db_init]` python3
  - 起動時に実行され終了
  - Chassis information update tool for SONiC.
  - This tool runs one time at the launch of the platform monitor in order to populate STATE_DB with chassis information such as model, serial number, and revision.
- `[program:lm-sensors]` bash
  - `/usr/bin/lm-sensors.sh`
  - 実際は `/usr/bin/sensors` （バイナリ）を実行している
  - `/etc/sensors.d/sensors.conf` があれば実行時に利用する
  - TODO: `/usr/bin/sensors` のソースコードは？
- `[program:fancontrol]` bash
  - `/usr/sbin/fancontrol`
  - 実際にFANを制御しているプログラムは要確認
- `[program:ledd]` python3
  - `/usr/local/bin/ledd`
  - Front-panel LED control daemon for SONiC
- `[program:xcvrd]` python3
  - `/usr/local/bin/xcvrd`, `/usr/local/lib/python3.9/dist-packages/xcvrd`
  - Transceiver information update daemon for SONiC
- `[program:ycabled]` python3
  - `/usr/local/bin/ycabled`, `/usr/local/lib/python3.9/dist-packages/ycable/`
  - Y-Cable interface/update daemon for SONiC
- `[program:psud]` python3
  - `/usr/local/bin/psud`
  - PSU information update daemon for SONiC
  - This daemon will loop to collect PSU related information and then write the information to state DB.
  - Currently it is implemented based on old plugins rather than new platform APIs. So the PSU information just includes three things: number of PSU, PSU presence and PSU status which is supported by old plugins.
  - PSU_INFO_UPDATE_PERIOD_SECS (3秒) 毎にループ
- `[program:syseepromd]` python3
  - `/usr/local/bin/syseepromd`
  - Syseeprom information gathering daemon for SONiC
  - This daemon will be started during the start phase of pmon container, gathering syseeprom info and write to state DB. It will continue monitoring the state DB for the syseeprom table, if table was deleted, it will write again. With this daemon, show syseeprom CLI will be able to get data from state DB instead of access hw or cache.
- `[program:thermalctld]` python3
  - `/usr/local/bin/thermalctld`
  - Thermal control daemon for SONiC
- `[program:pcied]` python3
  - `/usr/local/bin/pcied`
  - PCIe device monitoring daemon for SONiC

### pmon の各種モジュールの起動制御

各モジュールを起動するかは [sonic-buildimage: /dockers/docker-platform-monitor/](https://github.com/sonic-net/sonic-buildimage/tree/master/dockers/docker-platform-monitor) の `docker-pmon.supervisord.conf.j2` で制御され、設定は `pmon_daemon_control.json` に記述されています。

```
> docker-pmon.supervisord.conf.j2 抜粋

{% if not skip_chassisd and IS_MODULAR_CHASSIS == 1 %}
[program:chassisd]
command=/usr/local/bin/chassisd

{% if not skip_chassis_db_init %}
[program:chassis_db_init]
command=/usr/local/bin/chassis_db_init

{% if not skip_sensors and HAVE_SENSORS_CONF == 1 %}
[program:lm-sensors]
command=/usr/bin/lm-sensors.sh
...
```

- `pmon_daemon_control.json` の場所
  - GitHub Repo: [sonic-buildimage: /device/\<device\>/\<model\>/](https://github.com/sonic-net/sonic-buildimage/tree/master/device)
  - 実機（ホスト）： `/usr/share/sonic/device/<model>/`
  - 実機（`pmon container`）： `/usr/share/sonic/platform/`

```
> Wedge100BF-32 (x86_64-accton_wedge100bf_32x-r0) の例
admin@sonic:~$ docker exec -it pmon bash
root@sonic:/# cat /usr/share/sonic/platform/pmon_daemon_control.json
{
    "skip_pcied": false,
    "skip_fancontrol": true,
    "skip_thermalctld": false,
    "skip_ledd": true,
    "skip_xcvrd": false,
    "skip_psud": false,
    "skip_syseepromd": false
}
```

### `Wedge100BF-32` で起動している pmon 関連モジュール（サンプル）

`Wedge100BF-32` で確認したところ、 `x86_64-accton_wedge100bf_32x-r0/pmon_daemon_control.json` ではスキップしない（false）設定だが起動していないモジュールが多数ありました。
具体的には、 `pcied` しか起動していません。

これらは、"起動したけど停止した" もしくは "そもそも起動していない" の２パターンがありそう。（継続調査が必要）

```
admin@sonic:/var/log$ docker exec -it pmon head -30 /var/log/supervisor/supervisord.log
2022-07-06 22:59:03,296 INFO Included extra file "/etc/supervisor/conf.d/supervisord.conf" during parsing
2022-07-06 22:59:03,296 INFO Set uid to user 0 succeeded
2022-07-06 22:59:03,301 INFO RPC interface 'supervisor' initialized
2022-07-06 22:59:03,301 CRIT Server 'unix_http_server' running without any HTTP authentication checking
2022-07-06 22:59:03,302 INFO supervisord started with pid 1
2022-07-06 22:59:04,306 INFO spawned: 'dependent-startup' with pid 14
2022-07-06 22:59:04,309 INFO spawned: 'supervisor-proc-exit-listener' with pid 15
2022-07-06 22:59:05,629 INFO success: dependent-startup entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
2022-07-06 22:59:05,630 INFO success: supervisor-proc-exit-listener entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
2022-07-06 22:59:05,637 INFO spawned: 'rsyslogd' with pid 16
2022-07-06 22:59:06,701 INFO success: rsyslogd entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
2022-07-06 22:59:07,731 INFO spawned: 'chassis_db_init' with pid 20
2022-07-06 22:59:07,732 INFO success: chassis_db_init entered RUNNING state, process has stayed up for > than 0 seconds (startsecs)
2022-07-06 22:59:07,741 INFO spawned: 'xcvrd' with pid 21
2022-07-06 22:59:07,763 INFO spawned: 'pcied' with pid 22
2022-07-06 22:59:07,902 INFO exited: chassis_db_init (exit status 1; not expected)
2022-07-06 22:59:08,007 INFO exited: xcvrd (exit status 1; not expected)
2022-07-06 22:59:09,011 INFO spawned: 'xcvrd' with pid 23
2022-07-06 22:59:09,222 INFO exited: xcvrd (exit status 1; not expected)
2022-07-06 22:59:11,265 INFO spawned: 'xcvrd' with pid 24
2022-07-06 22:59:11,465 INFO exited: xcvrd (exit status 1; not expected)
2022-07-06 22:59:14,522 INFO spawned: 'xcvrd' with pid 25
2022-07-06 22:59:14,725 INFO exited: xcvrd (exit status 1; not expected)
2022-07-06 22:59:14,726 INFO gave up: xcvrd entered FATAL state, too many start retries too quickly
2022-07-06 22:59:17,798 INFO success: pcied entered RUNNING state, process has stayed up for > than 10 seconds (startsecs)
2022-07-07 23:03:15,692 WARN received SIGTERM indicating exit request
2022-07-07 23:03:15,692 INFO waiting for dependent-startup, supervisor-proc-exit-listener, rsyslogd, pcied to die
2022-07-07 23:03:15,734 INFO stopped: pcied (exit status 143)
2022-07-07 23:03:15,736 INFO exited: dependent-startup (exit status 3; expected)
2022-07-07 23:03:17,756 INFO stopped: rsyslogd (exit status 0)
```

## lldp

### lldpd
### lldp_syncd
### lldpmgrd

## radv (Router Advertiser)

`start.sh` で起動すべきかの判断を行い、 `wait_for_link.sh` が実行された場合のみ `/usr/sbin/radvd` を実行する。

起動すべきかの条件判断は以下の通り

```
> https://github.com/sonic-net/sonic-buildimage/blob/master/dockers/docker-router-advertiser/docker-router-advertiser.supervisord.conf.j2
{# Router advertiser should only run on ToR (T0) devices which have #}
{# at least one VLAN interface which has an IPv6 address asigned #}
{# But not for specific deployment_id #}
{%- set vlan_v6 = namespace(count=0) -%}
{%- if DEVICE_METADATA.localhost.deployment_id != "8" -%}
  {%- if DEVICE_METADATA.localhost.type -%}
    {%- if "ToRRouter" in DEVICE_METADATA.localhost.type or DEVICE_METADATA.localhost.type in ["EPMS", "MgmtTsToR"] -%}
      {%- if VLAN_INTERFACE -%}
        {%- for (name, prefix) in VLAN_INTERFACE|pfx_filter -%}
          {# If this VLAN has an IPv6 address... #}
          {%- if prefix | ipv6 -%}
            {%- set vlan_v6.count = vlan_v6.count + 1 -%}
          {%- endif -%}
        {%- endfor -%}
      {%- endif -%}
    {%- endif -%}
  {%- endif -%}
{%- endif -%}
```

## bgp (docker-fpm-frr)

`bgp container` は使用するルーティングアプリケーションによって動作しているモジュールが異なります。
ここではデフォルトである FRRouting を利用した `docker-fpm-frr` について記述します。

`docker-fpm-frr container` は [sonic-buildimage: /dockers/docker-fpm-frr](https://github.com/sonic-net/sonic-buildimage/tree/master/dockers/docker-fpm-frr) に存在します。

設定等により利用されるモジュールが異なりますが、デフォルト設定で利用されている以下モジュールを中心に説明します。

- fpmsyncd
- bgpmon
- zebra
- staticd
- bgpd
- bgpcfgd

### 起動するモジュールの違いとシーケンス

起動するモジュールを制御する `supervisord` の設定は [/dockers/docker-fpm-frr/frr/supervisord/](https://github.com/sonic-net/sonic-buildimage/tree/master/dockers/docker-fpm-frr/frr/supervisord) に保存されています。

`supervisord.conf.j2` では以下のように多くのモジュール（ `[program:xxx]` ）が定義されていますが、 設定により起動するモジュールが異なります。

- 共通のモジュール
  - fpmsyncd
  - bgpmon
  - zebra
  - staticd
  - bgpd
  - zsocket：起動後に終了（zebra がコネクションを受信可能な状態になったのを確認するスクリプト）
- `frr_mgmt_framework_config == true` では無い場合（デフォルト？）
  - bgpcfgd
- `frr_mgmt_framework_config == true` の場合
  - frrcfgd
  - bfdd
  - ospfd
  - pimd
- `DEVICE_METADATA.localhost.docker_routing_config_mode == "unified"`
  - vtysh_b
- `WARM_RESTART.bgp.bgp_eoiu == "true"`
  - bgp_eoiu_marker

TODO：設定毎の起動シーケンスを追加

### fpmsyncd

### bgpmon

### zebra

### staticd

### bgpd

### bgpcfgd
