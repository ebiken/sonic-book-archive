# SONiCアーキテクチャ

> SONiCアーキテクチャの全体像と、各サブシステムやモジュール間の連携方法（の一部）は、公式SONiCレポジトリのWikiにて解説されている。
> 公式な情報が必要な場合はこちらを参照のこと。
> - [GiHub: SONiC > Wiki/Architecture](https://github.com/sonic-net/SONiC/wiki/Architecture)

- [アーキテクチャの全体像](#アーキテクチャの全体像)
- [主要なサブシステムやモジュールの概要](#主要なサブシステムやモジュールの概要)
  - [サブシステムやモジュールの命名規則](#サブシステムやモジュールの命名規則)
  - [database container](#database-container)
  - [CLI / sonic-cfggen](#cli--sonic-cfggen)
  - [swss container](#swss-container)
  - [syncd container](#syncd-container)
  - [bgp container](#bgp-container)
- [フロントパネルインターフェースと仮想インターフェース](#フロントパネルインターフェースと仮想インターフェース)

## アーキテクチャの全体像

![sonic-official-wiki-high-level-architecture](figures/official-wiki-section4_pic1_high_level.png)
> 引用：section4_images/section4_pic1_high_level.png https://github.com/sonic-net/SONiC/wiki/Architecture

SONiCはそれぞれ異なる機能を担うサブシステムが連携して動作しています。
上記は公式Wikiから抜粋した図でその概要を示しています。
**現在は上記図に記載されているコンテナ以外も追加されている事に注意してください（TODO：最新の図を作成しリプレース）**

各機能を担うサブシステムはコンテナとして分離動作する事により、プラットフォーム（ハードウェアやホストOS）に依存せず機能を提供する事が可能となります。
例外は `CLI` と `sonic-cfggen` で、これらモジュールはホストOS上で動作しています。

各サブシステム（コンテナ）内では実際に機能を提供する各種モジュールが動作しています。
例えば `lldp container` 内では、`lldpd` `lldpmgrd` `lldp_syncd` といったモジュールが動作しています。
モジュールはSONiC用に開発されたものに加え、既存オープンソース実装を利用している場合もあります。
既存オープンソース実装を利用しているモジュールの例としては、 `FRR(bgpd/zebra)` `teamd` `lldpd` 等があります。

各サブシステム（実際には内部で動作するモジュール）は、主に `database container` を介してデータをやりとりする事により連携しています。
SONiC は Redis (https://redis.io/) をデータベースとして利用しています。
Redis は複数のデータベースを保持する事が可能で、それぞれDBID（整数の database id）で識別されます。
SONiC ではそれぞれの役割に応じデータベースに名前（DB名）を付けて管理しており、DB名と Redis DBID との対応（及び各データベース内のテーブル名）は [sonic-swss-common/common/schema.h](https://github.com/sonic-net/sonic-swss-common/blob/master/common/schema.h) に定義されています。
主なDB名（ID）は `APPL_DB(0)`, `ASIC_DB(1)`, `COUNTERS_DB(2)`, `CONFIG_DB(4)`, `STATE_DB(6)` があります。

各サブシステムは `database container` 以外とも連携します。
1つ目はホストOSで、 `netlink` `/sys file-system` `netdev`（仮想デバイス） 等を用いて各種ステートの取得や反映、コントロールパケットの送受信を実施します。
2つ目は Switch ASIC で、ASICベンダが提供する ASIC SDK やドライバを通じて設定の反映、ステータスや統計情報等のやり取りを実施します。
他にも、設定を保存したファイル（例：`config_db.json`）や、CLIを通じたオペレータとの連携、周辺機器（ペリフェラル）とドライバ等を通じた連携があります。

## 主要なサブシステムやモジュールの概要

スイッチをコントロールする "ネットワークOS" としての中心を担う、主要なサブシステムについて概要を説明します。
各サブシステムとモジュールの詳細については、引き続き [各サブシステムやモジュールの役割](doc/sonic-subsystem.md) を参照してください。

### サブシステムやモジュールの命名規則

概ね各サブシステムやモジュールは名前毎に以下のような役割を持ちます。
但し、これはあくまでも目安であり、`syncd container` と `swss container` 内の `*syncd` モジュール等、必ずしも分かりやすい命名規則には従っていない場合がある事、以下に記載した以外の役割を担っている場合もある事に注意が必要です。

- `*syncd` モジュール
  - 各機能を担うモジュールとデータベースを仲介します。
  - 例えば `lldp_syncd` は `lldpd` の状態をデータベースとやり取りします。
- `*mgrd` モジュール
  - 主にデータベース以外のコンポーネント（例：ホストOS）と、モジュールやデータベースの間を仲介します。
  - 例えば `IntfMgrd` は `APPL_DB`, `CONFIG_DB`, `STATE_DB` をモニタし、ホスト（Linux Kernel）に反映させます。
- `*orch`
  - `orchagent` モジュール内部の、各機能毎に `APPL_DB` から `ASIC_DB` への変換を行う機能名です。
  - 実態は `fdborch.cpp` `srv6orch.cpp` 等、C++プログラムでありモジュール名では無い事に注意が必要です。

> TODO：各モジュール名と役割の説明は、調査が進んだ時点で再度分かりやすく表現や内容を更新する。

### database container

設定、状態、統計情報など、SONiCで扱うあらゆるデータを格納します。
データを格納するだけでなく、各サブシステム（モジュール）は、Key に対して Subscribe する事により、該当する Key-Value が変更された場合等に通知を受けとり、処理を開始する事も可能です。
すなわち、データベースという名前ですが、実際はデータの格納場所だけでなく、各サブシステム間のデータハブとしても機能しています。

主なDB名（ID）は `APPL_DB(0)`, `ASIC_DB(1)`, `COUNTERS_DB(2)`, `CONFIG_DB(4)`, `STATE_DB(6)` であり、それぞれ以下の役割を持ちます。

- `APPL_DB(0)`
  - 各サブシステム（モジュール）で生成されたオブジェクト情報を格納します。
  - 例えば、ルーティング情報、next-hop、neighbor情報、等があります。
  - サブシステム連携の中核を担う、最も重要なデータベースです。
- `ASIC_DB(1)`
  - ASICをコントロールするために必要な情報を、ASICに親和性の高い形式でデータを保存します。
  - 例えば、SAIに関連するデータは、SAI Object と同様の形式で保存されます。（TODO：要確認）
  - このデータベースに格納されたデータは `syncd container` を通じてASICに反映されます。
- `COUNTERS_DB(2)`
  - 統計情報が格納されます。
  - 例えば、ポート毎のカウンター情報が挙げられます。
  - CLIを通じて参照したり、他のサブシステムによりテレメトリ情報として利用する事が可能です。
- `CONFIG_DB(4)`
  - 設定情報が格納されます。
  - 例えば、物理ポート、インターフェース、VLAN等、あらゆる設定情報を格納可能です。
  - 但し、サブシステムによっては `CONFIG_DB` を利用せず、独自の方法で設定を保持している場合がある事に注意が必要です。
- `STATE_DB(6)`
  - 動作状態（ operational state ）が格納され、相互依存するサブシステム間の連携に利用されます。
  - 例えば LAG の状態が挙げられます。

### CLI / sonic-cfggen

TODO

### swss container

- `*orch`
  - `orchagent` モジュール内部の、各機能毎に `APPL_DB` から `ASIC_DB` への変換を行う機能名です。
  - 実態は `fdborch.cpp` `srv6orch.cpp` 等、C++プログラムでありモジュール名では無い事に注意が必要です。


### syncd container

TODO

### bgp container

TODO

## フロントパネルインターフェースと仮想インターフェース

TODO