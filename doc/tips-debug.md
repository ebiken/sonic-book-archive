# Tips: Debug

デバッグ関連のTIPSをとりあえず記録する場所

- [ログの参照やレベルの変更](#ログの参照やレベルの変更)
  - [SWSS Log (sairedis.rec, swss.rec)](#swss-log-sairedisrec-swssrec)

## ログの参照やレベルの変更

### SWSS Log (sairedis.rec, swss.rec)

`swss container` からでもホストからでもログ参照やログレベル変更が可能。

```
> host (or swss container)
swssloglevel -l SAI_LOG_LEVEL_DEBUG -s -a

> host
admin@sonic:~/tmp$ tail -f /var/log/swss/sairedis.rec
```
