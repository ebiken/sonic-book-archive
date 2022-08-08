# sonic-book

SONiC Book ... a place to store SONiC information

> - Book と言いつつ多少綺麗に整理したメモ書きの集大成
> - SONiCの内部構造を理解し、最終的には改造したい人向けの情報を集める（コマンドや設定は最小限）
>   - 第1部は暇になったら書く（暇にならない？）
>   - ネットワークの基本知識は記述しない

## 目次

第0部

- [SONiC用語集](doc/terminology.md)

第1部 SONiC概要

- SONiCの歴史や背景
- 消えていったオープンソースNOSの記録（アーキテクチャ比較）

第2部 デザイン：アーキテクチャ、各モジュールの役割、SAI、ターゲット

- [SONiCを学ぶための前提知識](doc/prerequisites.md)
- [SONiCアーキテクチャ](doc/sonic-architecture.md)
- [各サブシステムやモジュールの役割](doc/sonic-subsystem.md)
- [機能毎のモジュール連携方法やデータの流れ](doc/subsystem-interaction.md)
- [SAI Objects & Dataplane Pipeline](doc/)

第3部 動かしてみる：ビルド、インストール、設定方法

- ビルド済みイメージを利用した起動方法（sonic-vs, 物理スイッチ）
- ビルド方法（全体ビルド、コンテナのビルドや入替）
- 設定（サンプル）
  - L2/L3基本動作（VLAN + L3 Routing）
  - [SRv6 (APPL_DB直接設定)](doc/)

第4部 Deep Dive とカスタマイズ

- SONiCに関連したレポジトリと役割
- 各種DBの解説（スキーマ、参照方法、書き込み方法）
- [SAIソースコードの場所と呼び出しフロー](doc/sai-sourcecode.md)
- モジュールや機能毎の詳細解説
  - CLI（Click）詳細
  - [SRv6 Deep Dive](doc/)
- Sonic Management Framework (REST, Klish)
- データプレーンのカスタマイズ（Tofino：P4/PINS）
  - データプレーン指定方法と裏側の動作（barefoot syncd container）
  - PINSを利用した独自テーブルの追加方法
  - （Intel switch.p4 の改造などはNDA範囲で記載不可？）
- [DEBUG方法（常時UPDATE）](doc/)

参考文献

- TBD