# sonic-book

SONiC Book ... a place to store SONiC information

Check [ebiken/nsdevnotes](https://github.com/ebiken/nsdevnotes) for non SONiC information.

> - Book と言いつつ多少綺麗に整理したメモ書きの集大成
> - SONiCの内部構造を理解し、最終的には改造したい人向けの情報を集める（コマンドや設定は最小限）
>   - 第1部は暇になったら書く（暇にならない？）
>   - ネットワークの基本知識は記述しない

## 目次

### 第0部

- [SONiC用語集](doc/terminology.md)
- [SONiC FAQ (memo)](doc/faq-sonic.md)
 
### 第1部 SONiC概要

- SONiCの歴史や背景
- 消えていったオープンソースNOSの記録（アーキテクチャ比較）
- コミュニティ運営と開発プロセス
  - 組織構成やメンバー（毎年変わる可能性があるので立ち上げメンバーの企業種別を中心に）
  - コミュニケーションチャネル（Mailing List, GitHub Issue/PR）
  - リリースプロセス
    - [リリースプロセス解説メール 2023/01/09 Tips/Requirements on SONiC 202305 release](https://lists.sonicfoundation.dev/g/sonic-dev/message/107)
  - 質問、不具合報告、修正

### 第2部 デザイン：アーキテクチャ、各モジュールの役割、SAI、ターゲット

- [SONiCを学ぶための前提知識](doc/prerequisites.md)
- TODO#2 [SONiCアーキテクチャ](doc/sonic-architecture.md)
- TODO#1 [各サブシステムやモジュールの役割](doc/sonic-subsystem.md)
- TODO#2 [機能毎のモジュール連携方法やデータの流れ](doc/subsystem-interaction.md)
- TODO#6 [SAI概要 & Objects & Dataplane Pipeline](doc/sai.md)
- sonic-vs データプレーンがどのように動作するか？

### 第3部 動かしてみる：ビルド、インストール、設定方法

ビルド、インストール
- [SONiCが動作する機材（Platform）](doc/sonic-platform.md)
- [Running SONiC on KVM (sonic-vs)](doc/running-sonic-kvm.md)
- [Running SONiC on ContainerLab (clab)](clab/README.md)
  - clab を利用した複数台Fabricのサンプル手順＆スクリプト
- Running SONiC on Fixed Function ASIC(TBD: running-sonic-asic.md) ⇒ 機材入手したら作成
- Running SONiC on Tofino ASIC (TBD: running-sonic-tofino.md) ⇒ 公開できない (T^T)
- [Getting pre-built image](doc/sonic-image-prebuilt.md)
- [ビルド方法： Building SONiC image from source code](doc/sonic-image.md)
- [SONiC Build Image Memo](doc/sonic-buildimage-memo.md) ビルド関連情報のメモ集約

設定方法
- [SONiC Commands](doc/sonic-commands.md)
- [SONiCの設定（サンプル）](doc/sonic-config.md)

### 第4部 Deep Dive とカスタマイズ

- SONiCに関連したレポジトリと役割
- 各種DBの解説（スキーマ、参照方法、書き込み方法）
- SAI Deep Dive
  - [SAIソースコードの場所と呼び出しフロー](doc/sai-sourcecode.md)
  - [SAI Challenger](doc/sai-challenger.md)
- 機能毎の詳細解説
  - CLI（Click）詳細
  - TODO#4 [Deep Dive: SRv6](doc/sonic-deepdive-srv6.md)
  - [Zenn: SRv6 on SONiC を設定してみる (End.DT46, H.Encaps.Red) (APPL_DB直接設定)](https://zenn.dev/ebiken_sdn/articles/2887c04cf977a9)
- モジュール毎の詳細解説（起動シーケンスやソースコード）
  - TODO#3 [Deep Dive: SwSS](doc/sonic-deepdive-swss-orchagent.md)
  - TODO#3 [Deep Dive: SwSS: orchagent](doc/sonic-deepdive-swss-orchagent.md)
  - TODO#3 [Deep Dive: sairedis & syncd](doc/sonic-deepdive-sairedis.md)
  - TODO#3 [Sonic Management Framework: CLI(Klish), REST, gNMI](doc/sonic-management-framework.md)
- 機能毎の解説（SAI Object や設定フローを含む）
  - [SONiC: Next Hop Group, SAI Object and Flow](doc/sonic-nexthopgroup.md)
- データプレーンのカスタマイズ（Tofino：P4/PINS）
  - データプレーン指定方法と裏側の動作（barefoot syncd container）
  - PINSを利用した独自テーブルの追加方法
  - （Intel switch.p4 の改造などはNDA範囲で記載不可？）
- DEBUG方法やTIPS（常時UPDATE）
  - [Tips: Debug](doc/tips-debug.md) ... デバッグTIPSのとりあえずメモ
  - [Redis Database](doc/sonic-redisdb.md)

## 参考文献

### Official Pages

- Main repo : https://github.com/sonic-net/SONiC
  - `This repository contains documentation, Wiki, master project management, and website for the Software for Open Networking in the Cloud (SONiC).`
- Wiki (GitHub): https://github.com/sonic-net/SONiC/wiki
- Wiki (OCP): https://www.opencompute.org/wiki/Networking/SONiC
  - Recordings from SONiC Sub-Project Calls に HLD Review 動画へのリンクあり
- Source Code (build Repo) : https://github.com/Azure/sonic-buildimage
- Roadmap : https://github.com/sonic-net/SONiC/wiki/Sonic-Roadmap-Planning
- Feature Docs (HDL) : https://github.com/sonic-net/SONiC/tree/master/doc

### non-official Pages

- [SONiCをはじめてみよう（2019）](https://speakerdeck.com/imasaruoki/sonicwohazimetemiyou)
  - 起動～コマンド利用方法の解説。
- [(PDF) JANOG44: OSSなWhitebox用NOSのSONiCが商用で使われている理由を考える （2019）](https://www.janog.gr.jp/meeting/janog44/application/files/1415/6396/6082/janog44_sonic_kuwata-00.pdf)
  - SONiC仮想マシン４台構成の設定例あり
- [(PDF) JANOG49: SONiCの開発状況アップデート](https://www.janog.gr.jp/meeting/janog49/wp-content/uploads/2022/01/JANOGWeeeeeK%C3%AE%C3%B7%C3%A8J%C3%84%C3%A6%C3%B9%E2%94%90_APRESIA_v.0.1.pdf)
  - https://www.janog.gr.jp/meeting/janog49/sonic/
  - SONiC ロードマップや機能リスト
- µSONiC (micro-SONiC) used in Optical White Box (TIP Goldstone)
  - "Open whitebox architecture for smart integration of optical networking and data center technology"
    - https://ieeexplore.ieee.org/document/9275288)
    - Page 6 `µSONiC is used in cases where it is necessary to control an Ethernet ASIC. µSONiC is a lightweight package of SONiC, the Microsoft NOS, in which only the components that control SONiC’s Ethernet ASIC are extracted and containerized for easy deployment on Kubernetes.`
  - Two repos under GitHub `oopt-goldstone` organization 
    - https://github.com/oopt-goldstone/usonic_new
    - https://github.com/oopt-goldstone/usonic

### non-SONiC

- 分かりやすい Tutorial の例：[Writing a container in Rust](https://litchipi.github.io/series/container_in_rust)
