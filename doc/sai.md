# SAI (Switch Abstration Interface)


## SAI概要

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

## SAI Objects & Pipeline

SAI ではデータプレーンにアクセスする API を規定するために、SAI ではデータプレーン（ASIC等）内部のパケット処理パイプラインとオブジェクトを定義しています。

https://github.com/opencomputeproject/SAI/tree/master/doc

SAI Pipeline の情報が記載された文書は上記 doc フォルダに保存されています。
しかし、全体像を見渡せるドキュメントは存在せず、拡張に拡張が重ねられていますので、興味を持った機能に関しての文書を参照すると良いでしょう。

例えば SRv6 (Segment Routing IPv6) に関する SAI API / Pipeline / Object は2017年に Cavium により提案＆実装されました。
しかし、その後2021年に、他のトンネルプロトコルとの整合性や最新の RFC や Internet-Draft でのアップデートを取り込むため、Intelを中心に更新・実装されています。

そのため、2021年現在 SRv6 に関しては後者のドキュメントを参照する必要があります。

- 2017年 [SAI-Proposal-IPv6_Segment_Routing-1.md](https://github.com/opencomputeproject/SAI/blob/master/doc/SAI-Proposal-IPv6_Segment_Routing-1.md)
- 2021年 [SAI-IPv6-Segment-Routing-Update.md](https://github.com/opencomputeproject/SAI/blob/master/doc/SAI-IPv6-Segment-Routing-Update.md)