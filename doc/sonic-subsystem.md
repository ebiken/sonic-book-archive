# 各サブシステムやモジュールの役割

TODO: 各モジュールの役割を、「どのようなデータをどこから受信し、どのように変換しどこに送信（格納）するか」という視点で整理する。

## SwSS Switch State Service 

https://github.com/sonic-net/sonic-swss/tree/master/orchagent


## CLI / sonic-cfggen

> - Click (Python) ベースの CLI
>   - Click から `sonic_cfggen` 経由で `CONFIG_DB` や、 `CONFIG_DB` を利用しないモジュールの設定（ファイル）を操作する
>     - （TODO: どの操作がどのパスを通るか確認して更新）
>   - SONiC の CLI といえば（まだ）これで、多くのコマンドをサポートしている
>   - Source Code:
>     - `cli.py`: https://github.com/sonic-net/sonic-utilities/tree/master/utilities_common
>     - `sonic-cfggen`: https://github.com/sonic-net/sonic-buildimage/tree/master/src/sonic-config-engine
>   - コマンドリファレンス：https://github.com/sonic-net/sonic-utilities/blob/master/doc/Command-Reference.md

## SONiC Management Framework

> - Klish ベースの CLI
>   - Klish から Framework の REST API 経由で `CONFIG_DB` を操作する
>     - Klish は Cisco IOS Like な CLI を生成するフレームワーク
>   - サポートしているコマンドは限定的
>   - 2019年から開発が進められている、 [SONiC Management Framework (HLD)](https://github.com/sonic-net/SONiC/blob/master/doc/mgmt/Management%20Framework.md) の一部
>   - Source Code: https://github.com/sonic-net/sonic-mgmt-framework/tree/master/CLI/klish

