# 機能毎のモジュール連携方法やデータの流れ

TODO："各サブシステムやモジュールの役割" ではイメージできない、機能毎のモジュール間連携方法やデータの流れを具体例を元に整理する。

## TODO: 連携パターンの代表例（仮題）

TODO: DB/ASIC/Linux Kernel 等の連携方法を３～４パターンに分類し描画。どの機能がどのパターンに該当するかを記載。

- CONFIG_DB -> APPL_DB -> ASIC_DB -> ASIC
- APPL_DB -> ASIC_DB -> ASIC
- ?? Linux Kernel -> APPL_DB -> ASIC_DB -> ASIC
- ?? ASIC -> ASIC_DB/STATS_DB ??
- TBD


## 機能毎に必要なサブシステムやモジュール

TODO: 機能毎に最小限の構成を整理 ⇒ 各種DBとASICの連携フローを描画

