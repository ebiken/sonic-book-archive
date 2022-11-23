# SAI Challenger

The SONiC-Based Framework for SAI Testing and Integration

https://github.com/opencomputeproject/SAI-Challenger

## 概要

動作中のSONiC上では動作できないため、手軽なテストツールとしては利用できない。
テスト環境を構築したうえで繰り返しテストする際に非常に便利なツール。

- SAIのテストやインテグレーションを実施するためのツール。
- SAI を起動するテストは ASIC_DB に直接エントリを設定する事で実施可能だが、SAI objects ID (SAI OID or Real ID: RID) と Orchagent ID (Virtual OID: VID)の生成が必要なエントリの場合等、インタラクティブにエントリの内容を決める必要がある場合は手動でのテストは困難となるため、このようなツールが有用になる。
  - VID/RID間のマッピングは ASIC_DB に保存される： vid2rid, rid2vid

## Contributer

- PLVision社が開発し、OCPに Contribution した。
  - [PLVisionによる解説BLOG (2021/02/20)](https://plvision.eu/rd-lab/blog/opensource/sai-challenger-sonic-based-framework)

## memo

```
admin@sonic:~$ sonic-db-cli ASIC_DB HGETALL RIDTOVID
{'oid:0x34000000000004': 'oid:0x1700000000002a', 'oid:0x2d00000000001a': 'oid:0x15000000000020', 'oid:0x2d00000000005f': 'oid:0x15000000000114', 'oid:0x2d000000000109': 'oid:0x1500000000034a', 'oid:0x34000000000051': 'oid:0x170000000000e4', 'oid:0x3400000000000b': 'oid:0x17000000000031', 'oid:0x2d000000000067': 'oid:0x1500000000012e', 'oid:0x34000000000078': 'oid:0x1700000000014f', 'oid:0x2d00000000002c': 'oid:0x15000000000075', 'oid:0xa00000000003c': 'oid:0x1a00000000013f', 'oid:0xa000000000053': 'oid:0x1a0000000001a6', 'oid:0x1a000000000001': 'oid:0x12000000000391', 'oid:0x3400000000006f': 'oid:0x17000000000135', 'oid:0x340000000000c9': 'oid:0x17000000000239', 'oid:0x2d000000000113': 'oid:0x15000000000366', 'oid:0x2d00000000005d': 'oid:0x15000000000112', ...snip... }

admin@sonic:~$ sonic-db-cli ASIC_DB HGETALL VIDTORID
{'oid:0x1500000000005e': 'oid:0x2d000000000027', 'oid:0x1700000000016a': 'oid:0x34000000000082', 'oid:0x15000000000213': 'oid:0x2d0000000000aa', 'oid:0x170000000001d4': 'oid:0x340000000000a8', 'oid:0x15000000000384': 'oid:0x2d00000000011f', 'oid:0x150000000000a9': 'oid:0x2d00000000003c', 'oid:0x15000000000015': 'oid:0x2d00000000000f', 'oid:0x17000000000131': 'oid:0x3400000000006b', 'oid:0x17000000000183': 'oid:0x3400000000008a', 'oid:0x1a00000000020c': 'oid:0xa000000000069', 'oid:0x170000000002d1': 'oid:0x340000000000fb', 'oid:0x1a0000000002a8': 'oid:0xa00000000008d', 'oid:0x1000000000258': 'oid:0x27000000000018', 'oid:0x15000000000013': 'oid:0x2d00000000000d', 'oid:0x1500000000024b': 'oid:0x2d0000000000be', 'oid:0x15000000000246': 'oid:0x2d0000000000b9',  ...snip... }
```