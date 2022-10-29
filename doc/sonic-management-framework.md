# SONiC Management Framework

- [Reference](#reference)
- [処理の流れ](#処理の流れ)
- [YANGとABNFの関係](#yangとabnfの関係)

## Reference

- [本家：doc/mgmt/Management Framework.md](https://github.com/sonic-net/SONiC/blob/master/doc/mgmt/Management%20Framework.md)

## 処理の流れ

REST Server は YANG Model を元にしたペイロードを受信します。
REST Server は受信したペイロードを Translib に渡し、Translib は ABNF に変換します。
Config Validation Library (CVL) は YANG から生成された Redis ABNF schema を利用し、Translib から受信した ABNF JSON の Syntax / Semantic を Validate します。

## YANGとABNFの関係

- REST Server
  - YANG Model は OpenConfig ベース（要確認）
- Translib のロジックはどうやって生成している？
- CVL
  - Redis ABNF schema から SONiC YANG を生成


