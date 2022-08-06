# SONiCを学ぶための前提知識

SONiCは様々な機能を担当する多数のモジュールから構成されるため、設計や動作を理解するために必要な技術は多岐に渡ります。
そのため、SONiCについて学んでいると、SONiCそのものではなくSONiCで使われている技術の学習が途中で必要になることが多く、想定以上に学習や調査に時間がかかる事があります。
また、前提知識を理解してから学ぶことにより、SONiCの理解に集中する事が可能となり、必要な時間の短縮や理解度の深さ向上に役立つことがあります。

本セクションでは、SONiCを学ぶために必要な時間（期間）をイメージし、多少なりとも計画的に進める事ができるように、SONiCを学ぶために必要な前提知識を整理します。

なお、ここでは「どのような前提知識が必要になるか？」という事を紹介する事が目的のため、各技術に関しては概要説明のみとなります。
それぞれの技術に関しては、より詳細に解説しているサイトや書籍がありますので、それらを参照しながら学習してください。

- [参考資料](#参考資料)
- [スイッチ・ルータの基礎知識](#スイッチルータの基礎知識)
  - [コントロールプレーン・データプレーン](#コントロールプレーンデータプレーン)
  - [RIB, FIB, ASIC Table の違い](#rib-fib-asic-table-の違い)
- [SAI (Switch Abstration Interface)](#sai-switch-abstration-interface)
- [Redis DB](#redis-db)
- [Docker](#docker)
- [Linux Kernel Networking](#linux-kernel-networking)
- [Build Tools](#build-tools)
- [プログラミング言語](#プログラミング言語)
- [3rd Party Applications](#3rd-party-applications)

## 参考資料

SONiCに関連した複数の技術がカバーされている参考資料へのリンク。
個別技術に関連した参考資料はそれぞれのセクションに記載。

- [Speakerdeck: SONiCイントロダクション｜2018年](https://speakerdeck.com/imasaruoki/sonicintorodakusiyon)
  - SONiCの全体像、設定方法、内部構造まで幅広く概要がカバーされた、入門書的なスライド
- [Publickey: ホワイトボックススイッチとは何か？ オープン化がすすむネットワーク機器のハードとソフトの動向｜2015年](https://www.publickey1.jp/blog/15/post_255.html)
  - 情報が古いが、ホワイトボックススイッチについてざっと読むには短くて良い記事
- [PDF: 詳解ホワイトボックススイッチNOS｜MPLS Japan 2020](https://mpls.jp/2020/presentations/MPLS_Japan_Ishida.pdf)
  - ホワイトボックススイッチの内部構造だけでなく、NETLINKやSAIなどについても解説

## スイッチ・ルータの基礎知識

SONiCはホワイトボックススイッチをコントトールするネットワークOS（NOS）であるため、最低限のスイッチ・ルータの知識が必要となります。
但し、SONiCを学習しよう、と思う人はスイッチ・ルータの役割や設定方法などは商用スイッチ・ルータ等を通じて理解していると考えられますので、ここではスイッチ・ルータの内部構造を理解するために必要なキーワードを紹介します。

なお、以降は簡略化のため「スイッチ・ルータ」の両方を合わせて「スイッチ」と呼ぶことにします。

### コントロールプレーン・データプレーン

"コントロールプレーン" とは、スイッチがどのようにパケットを処理するのか決定し、また、運用者や運用ツール（監視装置、コントローラ、オーケストレータ、等）からの操作を受け、情報を提供する機能を提供します。
以下、コントロールプレーンを構成するモジュールの例を列挙します。

- インターフェース（CLI, NETCONF, REST, etc.）
- 設定や状態を管理するデータベース（ファイル）
- 転送経路を決定する各種ルーティングプロトコルデーモン（BGP, OSPF, ISIS, xSTP, etc.）
- 高度な機能を提供するエージェントやデーモン（SNMP, sFlow/IPFIX, LLDP, LAG, etc.）

"データプレーン" とは、パケットを受信し、コントロールプレーンから指示された方法に従いパケットの変更、転送、帯域制御やフィルタリング、等を実施します。
データプレーンの例を以下に列挙します。
SONiCで主に使われるデータプレーンは Switch ASIC 及び Linux Kernel Networking Stack となりますので、SONiCの学習にはその他データプレーンに関する理解は不要です。

- Switch ASIC
  - NPU (Network Processing Unit) とも呼ばれ、パケット転送に特化したチップ
  - SONiCで利用されるデータプレーンはこの Switch ASIC が中心となる
- Linux Kernel Networking Stack
  - CPUで動作する、OSのパケット処理機能
  - sonic-vs ではこれを利用しサーバ上で SONiC の動作検証が可能となる
- DPDK
  - CPUで動作。Kernelをバイパスしてユーザランドでパケットを処理する
  - CPUリソースを占有しながら動作するが、CPUを用いたパケット処理としては最速の技術
- SmartNIC
  - FPGA, Multi-core Processor, NPU 等のチップを搭載したNIC型のカード
  - CPUからパケット処理をオフロードし、高速低遅延でパケット処理が可能
  - Intel IPU(専用チップ), Mellanox DPU(ARMマルチコア) といった名称が広がりつつある

### RIB, FIB, ASIC Table の違い

スイッチには RIB, FIB, ASIC Table といった各種テーブルが存在します。
これらテーブル間のオブジェクト（エントリ）変換と設定がNOSの最も基本的な機能になります。
本書内でも、[全体アーキテクチャ] や [各モジュールの役割] 等、様々な場所で都度解説をしますが、まずは RIB, FIB, ASIC Table の関係を頭に入れておくと理解がしやすくなると思います。

全体の流れ： `各種ルーティングデーモン => RIB => FIB => ASIC Table`

- RIB: Routing Information Base
  - BGP, OSPF, IS-IS 等のプロトコルやスタティックな設定を通じて収集したトポロジー情報に基づき構築された、経路情報のデータベース
  - ネットワーク（アドレス）と、パケット転送先についての情報が保存されている
- FIB: Forwarding Information Base
  - 実際にパケットを転送する際の、ヘッダ変更内容と転送先インターフェースが格納されたデータベース
  - RIBと隣接ノード（Neighbor）情報などから構築される
- ASIC Table
  - Switch ASIC は Tbps クラスの超高速パケット転送とエントリ数の最大化のために、FIBを分割し保存したテーブル
  - パケットをステージに分けて処理をするために "（データプレーン｜パケット処理）パイプライン" とも呼ばれる
  - ASICベンダやASICの種類、ファームウェアや設定などにより様々なテーブル構成を取る

## SAI (Switch Abstration Interface)

- [Open Comput Project (OCP) - SAI Project Page](https://www.opencompute.org/projects/sai)
- [OCP SAI Mailing List & Archive](https://ocp-all.groups.io/g/OCP-SAI)
- [GitHub: SAI Repo](https://github.com/opencomputeproject/SAI/)

FIB を ASIC Table に投入するためには、ASICベンダのAPI(SDK)を利用する必要があります。
しかし、このAPIはASICベンダや種類毎に異なるため、異なるスイッチ上で動作するNOSを開発するには大きな工数やSDKを利用するためのライセンス費用が必要でした。

この状況を打破するために作られたのが SAI (Switch Abstration Interface) というベンダ共通のAPIです。
2015年に公開された [SAI v0.9.1 (pdf)](https://github.com/opencomputeproject/SAI/blob/master/doc/SAI-v0.9.1.pdf) は Microsoft, Dell,  Facebook, Broadcom, Intel, Mellanox が著者としてクレジットされていますが、他にも Cavium, Barefoot, Metaswitch 等の主要なASICやNOSベンダも関わっていました。

SAIはC言語のヘッダファイル [GitHub: SAI header files](https://github.com/opencomputeproject/SAI/tree/master/inc) として提供され、ASICベンダが提供するライブラリ（ドライバ）にリンクさせることにより様々なASICへの対応が可能となります。
なお、ASICベンダが提供するSAIドライバはバイナリ形式で提供されるため、通常SAIを拡張するためには各ASICベンダの協力が必要となります。

SAIのメジャーバージョンは現状6ヶ月毎にリリースされ、3ヶ月毎にマイナーバージョンがリリースされる場合もあります。
これは、 1. SAIの主なユーザであるSONiCが6ヶ月毎のリリースである事、 2. ASICベンダへ過剰な負担をかけない事、などが背景にあります。
リリースポリシーに関しては今でも議論が続けられており、2022年6月にもメーリングリストに議論内容が投稿されています。[該当するメーリングリストアーカイブ](https://ocp-all.groups.io/g/OCP-SAI/message/404)

スペックドキュメントは [Switch Abstraction Interface v0.9.2 (2015/06/24)](https://github.com/opencomputeproject/SAI/blob/master/doc/spec.md) の2015年以来更新されておらず、定義内容に関してはリリースブランチ毎のヘッダファイルを参照する必要があります。
また、[GitHub: SAI Repo > doc](https://github.com/opencomputeproject/SAI/tree/master/doc) フォルダにあるリリースノート（`SAI_1.x.y_ReleaseNotes.md`）や、機能に関する提案文書（`SAI-Proposal-xxx.md`）が参考になります。

## Redis DB

- https://redis.io/

SONiCで扱う各種オブジェクト（設定や状態）の多くは Redis DBに格納されています。
詳細は [全体アーキテクチ](sonic-architecture.md) で解説しますが、SONiCは "各種 Redis DB に格納されたオブジェクトを、機能毎の Agent が変換＆読み書きする事により動作するシステム" と言っても過言ではありません。

Redis DB とは以下特徴を持ったデータベースです。

- インメモリ（in-memory）
- 非リレーショナルデータベース
  - 単純なKey-Valueに加えて、ハッシュ型、リスト型、セット型、など、様々な種類のデータを取り扱う事ができる
- オープンソース：3条項BSDライセンス
- Pub/Sub 機能を持つ
  - Key に対して Subscribe する事により、該当する Key-Value が変更された場合等に通知を受ける事が可能

SONiCでは設定や状態の保存場所として以外にも、それらの変更の通知を受けて Agent が動作を開始するために利用されています。
Redis DB は複数のDB（デフォルトで16個）を持つことが可能であり、それぞれDBのID（数字）で識別されます。

SONiC学習の初期ではRedisの深い知識は不要ですので、まずは以下を理解した上で、必要や興味に応じて豊富にある文献を参照しながら学習を継続する事をお勧めします。

- SONiCで利用されているDB名とIDのマッピング定義
  - [GitHub: sonic-swss-common/common/schema.h](https://github.com/sonic-net/sonic-swss-common/blob/master/common/schema.h)
  - 主なDB名（ID）： APPL_DB(0), ASIC_DB(1), COUNTERS_DB(2), CONFIG_DB(4), STATE_DB(6)
- SONiC上でのDB参照方法（`sonic-db-cli` の利用）
  - 各DBのKey一覧参照： `sonic-db-cli <DB_NAME> keys \*`
  - KeyのTypeを確認： `sonic-db-cli <DB_NAME> type <KEY>`
  - KeyのValueを確認： `sonic-db-cli <DB_NAME> <COMMAND> <KEY>`
    - `<COMMAND>` は Type 毎に異なる：https://redis.io/commands/
    - 例：Type==hash の場合 `sonic-db-cli <DB_NAME> HGETALL <KEY>`
    - 参考BLOG：[Redis に保存されてる値を見ようと思った時に覚えておきたい redis コマンド](https://blog.eiel.info/blog/2014/08/26/remember-redis/)
- `sonic-db-cli` は `redis-cli` の便利なサブセットであるため、より詳細なアクセスが必要な場合は `redis-cli` を利用

## Docker

SONiCの各機能は Docker コンテナとしてパッケージされ動作しています。
そのため、以下のような Docker の最低限の基本操作は理解してから学習を始めましょう。

- コンテナ一覧表示： `docker ps`
- コンテナでコマンド実行： `docker exec -it <CT_NAME> <COMMAND>`
  - bash を利用： `docker exec -it <CT_NAME> bash`

また、各 Docker コンテナをビルドするための情報は [GitHub: sonic-buildimage /dockers](https://github.com/sonic-net/sonic-buildimage/tree/master/dockers) に存在します。
ビルドの効率化や機能拡張などを実施する際には、操作方法だけでなく Docker ファイルの作成方法についても学習しましょう。

> 参考：SONiCで起動している Docker コンテナの一覧（バージョンや有効にしている機能により異なります）
> ```
> admin@sonic:~$ docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Command}}" --no-trunc
> NAMES            IMAGE                                COMMAND
> snmp             docker-snmp:latest                   "/usr/local/bin/supervisord"
> mgmt-framework   docker-sonic-mgmt-framework:latest   "/usr/local/bin/supervisord"
> telemetry        docker-sonic-telemetry:latest        "/usr/local/bin/supervisord"
> pmon             docker-platform-monitor:latest       "/usr/bin/docker_init.sh"
> lldp             docker-lldp:latest                   "/usr/bin/docker-lldp-init.sh"
> radv             docker-router-advertiser:latest      "/usr/bin/docker-init.sh"
> syncd            docker-syncd-bfn:latest              "/usr/local/bin/supervisord"
> teamd            docker-teamd:latest                  "/usr/local/bin/supervisord"
> swss             docker-orchagent:latest              "/usr/bin/docker-init.sh"
> bgp              docker-fpm-frr:latest                "/usr/bin/docker_init.sh"
> database         docker-database:latest               "/usr/local/bin/docker-database-init.sh"
> ```

## Linux Kernel Networking

SONiCでは様々な用途でベースOSである Linux Kernel のネットワーク機能を利用しています。

- スイッチのポートに対応した仮想デバイスの作成
  - 管理ポートとの区別を明確にするため Front-Pannel Interface とも呼ばれる
- 仮想デバイスを通じた、自ノード宛てパケットや管理パケットの送受信
  - FRR等、ルーティングデーモンもこの機構を通じプロトコルパケットを送受信している
- 隣接ノードの解決（ARPやNeighbor Discovery）
- NETLINKを通じたネットワーク状態のモニタリングや設定への反映
- LAG等、Linuxの既存機能を流用した機能の実現

そのため、以下技術について基本的な理解が必要となります。

- NETLINK
- NETDEV
- Unix socket
- iproute2 等のネットワーク系コマンド（ip, route, ss etc.）
- VRF と network namespace (netns) 

## Build Tools

- [SONiC Buildimage Guide](https://github.com/sonic-net/sonic-buildimage/blob/master/README.buildsystem.md)

SONiCインストールイメージ（以後、SONiCイメージ）のビルドは様々なモジュールをビルドし結合して実施されるため、SONiCを理解するにあたり最も多くの技術やツールが関わる分野のひとつであり、関連ツールの初学者にとっては多くの学習時間が必要な分野となります。
そのため、SONiC学習の初期段階では、ビルド済みのイメージを利用したり、ビルドできることを確認済みのコミットベースで標準的なビルド方法のみ利用する事により、ビルドツールに関する学習を先延ばしにするのもSONiCの全体的な理解を深めるひとつの学習戦略といえます。

> ビルド済みイメージの利用方法については [ビルド済みイメージを利用した起動方法] を参照

但し、ある程度大きな不具合の修正や、独自機能の追加などに取り組む際にはビルドツールの理解が不可欠となります。
そのため、SONiCのビルドシステムについて学習を開始する前に、以下ツールに関して学習し理解する事が推奨されます。

- shell script
- GNU Make
- Jinja2 （Pythonテンプレートエンジン）
- Dockerfile を用いたコンテナの作成
- Debian packages の作成方法

## プログラミング言語

SONiCでは各モジュール毎に異なるプログラミング言語が利用されているため、理解を深めたい機能毎に必要なプログラミング言語が異なります。
しかし、大半のモジュールは `C++` もしくは `Python` で記述されているため、この２つの言語に関して "ソースコードを読んで何をしているのかを追える程度の理解" を得ておくことがお勧めです。

また、厳密にはプログラミング言語ではありませんが、 `YAML` `JSON` といったデータ形式は頻出でありかつ1時間程度で最低限の理解はできると思いますので、SONiCの学習を始める前にインターネット上の解説記事を検索し読んで理解しておくことを推奨します。

> TODO: SONiCの機能やモジュール毎に利用されているプログラミング言語の一覧は、[モジュールや機能毎の詳細解説] 等を記述した際に追加予定

## 3rd Party Applications

SONiCでは既存のオープンソース実装を組合せて機能を実現している場合も多いです。（例：Click, Klish, FRR, libteam, etc.）
そのため、学びたい機能毎に利用されているオープンソース実装について理解をしておく必要があります。

> TODO: SONiCに利用されている 3rd Party Application の一覧は、[モジュールや機能毎の詳細解説] 等を記述した際に追加予定