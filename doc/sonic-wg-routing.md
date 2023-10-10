# SONiC Routing Working Group

- [概要](#概要)
- [Link](#link)
- [ASOC: Alibaba Summer of Code 2023](#asoc-alibaba-summer-of-code-2023)
- [Meeting Summary](#meeting-summary)
  - [2023/05/04 Kick Off Meeting](#20230504-kick-off-meeting)
  - [2023/05/11 SRv6 use case and challenges in SONiC](#20230511-srv6-use-case-and-challenges-in-sonic)
  - [2023/05/18 FRR patch for Table/VRF id](#20230518-frr-patch-for-tablevrf-id)
  - [2023/05/25 SONiC FRR Upgrade, Alibaba Summer of Code 2023](#20230525-sonic-frr-upgrade-alibaba-summer-of-code-2023)
  - [2023/06/01 FRR, SONiC, Kernel Communication](#20230601-frr-sonic-kernel-communication)
  - [2023/06/08 SRv6 VPN SWSS code PR](#20230608-srv6-vpn-swss-code-pr)
  - [2023/06/15 orchagent/syncd workflow (bottle neck調査)](#20230615-orchagentsyncd-workflow-bottle-neck調査)
  - [2023/06/22 ASOC途中経過報告：skip kernel routes, memory usage](#20230622-asoc途中経過報告skip-kernel-routes-memory-usage)
  - [2023/06/29 SRv6 Policy 対応検討](#20230629-srv6-policy-対応検討)
  - [2023/07/06 FRR communication channel](#20230706-frr-communication-channel)
  - [2023/07/13 Fpmsyncd NHG by NTT (ebiken)](#20230713-fpmsyncd-nhg-by-ntt-ebiken)
  - [2023/07/20 Protobuf channel, Recursive NHG](#20230720-protobuf-channel-recursive-nhg)
  - [2023/07/27 Accton活動紹介、MSFT T2 zebra crash](#20230727-accton活動紹介msft-t2-zebra-crash)
  - [2023/08/03 improve routes downloading speed](#20230803-improve-routes-downloading-speed)
  - [2023/08/10 improve routes downloading speed](#20230810-improve-routes-downloading-speed)
  - [2023/08/17 ASOC活動報告：memory optimization, BGP node breakup](#20230817-asoc活動報告memory-optimization-bgp-node-breakup)
  - [2023/09/07](#20230907)
  - [2023/09/14](#20230914)
  - [2023/09/21](#20230921)
  - [2023/09/28](#20230928)
  - [2023/10/05](#20231005)

## 概要

- Chair: Eddie Ruan @ Alibaba
- Co-Chairs: Praveen Bhagwatula (Cisco), Syed Hasan Raza Naqvi (Broadcom), Rita Hui (Microsoft)
- Meetings
  - Weekly Meeting: Every Friday 9:30 AM JST -> 10:30 after Nov 10th , 2023（夏時間）
  - 2023年5月4日のKick Offから10月12日時点で計回開催
- 概要
  - （High Scale Switch ではなく） Routerとしての機能やスケーラビリティの改善にフォーカスしたWG
    - Routing related features, such as L3 VPN
    - High scale L3 VPN routes（L3 VPN routes のスケーラビリティ向上）
    - Routes loading time （ASICへの投入速度）
    - Routes convergence time （コンバージェンス）
    - Routes memory reduction （メモリ消費の削減）
    - Efficient communication among FRR, kernel and SONiC（FRR/kernel/SONiC間のコミュニケーション改善）
    - その他ルーティングに関連した改善
  - プロセス
    - SONiCに対する機能追加や変更を、まずこのWGでルーティング専門家の視点から議論やレビューを実施
    - その後に通常のリリースプロセスに従ってコミュニティから全般的なレビューを受ける
  - FRRoutingとSONiC双方のコミュニティから力を合わせて hite Box Switch におけるルーター機能の改善を行う
    - 基本的にFRRoutingの利用を前提とした提案や議論（BGP Container）
    - FRRouting から Donald Sharp & Jeff Tantsura (NVIDIA) が参加、助言を与えている
  - 日本からはNTT、NECが参加（2023年10月現在）

## Link

- TOP：https://lists.sonicfoundation.dev/g/sonic-wg-routing/
- Wiki：https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki
- Minutes：https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/33844

## ASOC: Alibaba Summer of Code 2023

- https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/33985
- SONiC Routing WG 関連課題の調査＆開発のためのインターンプロジェクト（Alibabaがスポンサー）
- 期間：12週間
‐ 中国の大学院生（master program）が、以下指導者の下で実施
  ‐ Alibaba Sponsor: Gunyao
  ‐ Routing WG Advisors: Donald Sharp, Jeff Tantsura
  ‐ Intern Mentors:  Shuai, Hanyu, Guoguo, Gongjian, Yunnan, and Qingyan from Alibaba AliNOS Team

[Routing WG] ASOC Intern project 1: Reduce bgp path memory usage routing Triaged #15528
[Routing WG] ASOC Intern project 2: Reduce bgp node memory usage routing Triaged #15557
[Routing WG] ASOC Intern project 3: Finalize SRv6 Policy downloading and handling routing Triaged #15558
[Routing WG] ASOC Intern project 4: Skip kernel routes downloading routing Triaged #15559
[Routing WG] ASOC Intern project 5: Improve orchagent's routes downloading speed routing Triaged #15560
[Routing WG] enable BGP PIC in FRR for SRv6 VPN use case routing #16366

## Meeting Summary

### 2023/05/04 Kick Off Meeting
> 05/04 Kick Off Meeting : https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/33848

- 各自自己紹介
- 設立意義の説明
- Routing WG で扱う課題の共有

事前配布された Routing Working Group Proposal 資料 [Routing working group.pdf](https://lists.sonicfoundation.dev/g/sonic-wg-routing/files/Routing%20working%20group.pptx)

- High Scale Switch ではなく、Routerとしての機能やスケーラビリティの改善を行う
- FRRoutingとSONiC双方のコミュニティから力を合わせて hite Box Switch におけるルーター機能の改善を行う

課題の解説

- Communication among FRR, kernel and SONiC
  - netlink message を利用
    - netlinkで未定義のAttributeが必要とする機能がある（SRv6等）
  - kernel への（不要な）forwarding structure の挿入
    - e.g. avoid insterting 2M VPN routes into kernel
    - （SONiCとは関連無いが、FRRコミュニティで FreeBSD でも同様の課題が有るとのこと）
  - SONiCからFRRに対する feedback channel の不在
    - e.g. BFD hardware offload の場合、ASICからFRRへsession statusの通知が必要
  - Feedback Channel に関しては改善も進んでいる
    - [FIB Suppress Announcements of Routes Not Installed in HW #1103](https://github.com/sonic-net/SONiC/pull/1103)
    - [[fpmsyncd] Implement pending route suppression feature #2551](https://github.com/sonic-net/sonic-swss/pull/2551)
- BGP memory usage
  - e.g. vpn-sid を route entry から attribute に移動する事により、route entry あたり 144B メモリ消費を削減(384B->240B)
- Orchagent memory usage
  - 2M routes を処理する際に orchagent は現状 3.5GB のメモリを消費
  - saimeta に flag を設定する事により 1.4GB まで削減可能
  - https://github.com/eddieruan-alibaba/SONiC/blob/eruan-srv6/doc/srv6/srv6_vpn.md
- BGP loading time
  - 当初のターゲットは 10K router per second
  - 更に改善していきたい
- Route Convergence time (BGP/IGP)
- Route installation のボトルネック（BRCMコメント）
  - FRR/fpmsyncdの性能に関わらず、APPL_DB -> orchagent の読み込みがボトルネックとなる
- Link down convergence 速度
  - orchagent は処理内容による優先制御が無いため、orchagent が別の仕事で忙しい場合 link down 時に nexthop group からの entry 削除に時間がかかる
- Recursive route resloution（Ciscoコメント）
  - MPLS Label や IP nexthop (NH) の共有がされないため、大量のNHエントリが必要になる
  - 現在は VXLAN tunnel のみサポート
- Sharing of nexthops for prefixes（Ciscoコメント）


### 2023/05/11 SRv6 use case and challenges in SONiC
> 05/11 SRv6 use case and challenges in SONiC : https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/33882 

Alibabaのユースケースや課題をSRv6を中心に解説

- Single Routing Silicon + Single Routing Stack 
  - No chassis, no internal BGP and no distributed forwarding
  - No MPLS or SR-MPLS
  - No IGP, only BGP
- DCI (eCore) の ESR で SRv6 を利用
- VPN SID を MP-BGP で広報

Alibabaの課題

- Linux Kernel need to support SRv6 forwarding with VPN SID
  - FRR/SONiC ではなく Linux Kernel (netdev) コミュニティで対応する必要がある
- Routes loading time
  - High scale routes >2M - service routes x 4
  - Performance < 10K/sec with bulk
  - 現在のボトルネック：Orchagent
- Memory footprint
  - FRR (BGP)
  - Orchagent (sai meata)
  - Vendor SAI
- Underlay routes flap affect Overlay SRv6 routes
  - 数百万(millions)単位のエントリのため、underlayがフラップするとZebraが overlay nexthop を解決できない事がある
  - 数百万もの overlay route update があると、underlay route update が1つの場合でもブロックされてしまう
- Hierarchical ECMP
  - Overlay two level ECMP(#1,#2) & Underlay single ECMP(#3)
    - Route -(ECMP#1)-> SRPolicy -(ECMP#2) -> SIDList -(ECMP#2)-> Underlay NH
  - Orchagent は multi level ECMP をサポートしていない
  - ASICも 2 level ECMP しかサポートしていない chip が多い

その他ディスカッション

- FRR には既に BFD HW offload 機能があるので要確認
- sharpd のアドバイス
  - メッセージやり取り全てに zebra を使うのではなく、BFDはzebraをバイパスする等を検討すると良い
  - bgp_path_info_extra のように、機能が有効になっていなくても使用する構造体を抽象化するとメモリ削減に役立つ


### 2023/05/18 FRR patch for Table/VRF id
> 05/18 meeting minutes. https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/33946

- SONiC FRR patch for table id and vrf id
  - 管理用VRFでdeafult routeを削除すると、パケット転送用（ASIC）のdefault routeも削除される
  - fpmsyncdはtable idを認識していないため、Table ID と VRF ID の取り扱いの違いが課題
  - 将来的にはfpmsyncdをtable idに対応させパッチを不要にするのが理想
  - `0009-ignore-route-from-default-table.patch`
  - `0023-Use-vrf_id-for-vrf-not-tabled_id.patch`
- SONiC FRR Upgrade プロセスの議論
  - 5/25を参照
- Hasan BRCM による 1M routing entry のスケーラビリティ議論
  - memroy footprint ~3.7G for 1M routes
  - routing convergence time ~247sec
  - docker memory OOM in link flap test; show ip route caused memroy overshot

### 2023/05/25 SONiC FRR Upgrade, Alibaba Summer of Code 2023
> 05/25 meeting minutes. https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/34007

- SONiC FRR Upgrade 解説
  - Hasan and Adam が提案を解説 [SONiC Community FRR Upgrade Process v1.pptx](https://lists.sonicfoundation.dev/g/sonic-wg-routing/files/SONiC%20Community%20FRR%20Upgrade%20Process%20v1.pptx)
  - TSCに提案 ⇒ 年１回アップグレードで結論
- Alibaba Summer of Code 2023 の紹介（5つのプロジェクト）
  - https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/33985
  - Alibaba インターン（修士学生）が sharpd / JeffT の助言を得ながら進める

### 2023/06/01 FRR, SONiC, Kernel Communication
> 06/01meeting minutes. https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/34072

FRR, SONiC, Kernel Communication 改善の提案（Gongjian from Alibaba）
- [FRR communication channel proposal v3.pdf](https://lists.sonicfoundation.dev/g/sonic-wg-routing/files/FRR%20communication%20channel%20proposal%20v3.pdf)
- fpmsyncdの課題（Alibaba）
  - 既存のnetlink attrではAlibabaユースケースをカバーできない（e.g. SRv6 Policy）
  - kernelに挿入不要なメッセージがある（スケーラビリティ向上の足かせ）
  - netlink/protobufのどちらかを選択する必要がある（同時利用不可）
  - SONiC(fpmsyncd)->Zebraの通知はnetlinkのみ
- Hardware offload BFD の実現のため、fpmsyncdではなく独自のチャネル(bfdyncd)でFRR BFDDと会話
  - `struct bfddp_message`
- VPN Routeを削除する際に時間がかかる： 270sec(/24) & 50sec(/32) per 2M route
  - Kernelには不要なエントリなため、バイパスしたい
  - 案 a. Zebra would treat Linux kernel as part of data plane. It will only give messages to fpm, let fpm decide what routes to be added into kernel.
  - 案 b. Use route policy to set a flag to indicate some routes would skip kernel insertion. Zebra will skip kenel insertion based on this flag
- MY_SID/SRv6_POLICY/LOCAL_SID 挿入方法の検討
  - Alibabaは netlink/protobuf の並存が好ましいと考える
  - ⇒ race condition 等、不具合の原因になるのでは？
- コミュニケーションチャネルは、routing関連はzebra/fpm経由、それ以外はSONiC直が良い？（案）

### 2023/06/08 SRv6 VPN SWSS code PR
> 06/08 meeting minutes https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/34083

- SRv6 VPN SWSS code のPRレビュー
  - [202305][SRv6]: SRv6 VPN SID #2765
  - [202305][SRv6]: SRv6 VPN Unit Tests #2766. 
  - The purpose to move in these codes to 202305 is for Cisco to pick up changes and be able to test on their C8K.
- kernel routes をスキップする方法の検討（以下、現時点での案）
  - Add zebra policy with skip kernel insertion as an action
  - Use zebra policy to set a flag in zebra route node
  - use this flag to skip kernel routes insertion
  - Add fpm simulate, all API params and event sequence would be stored in a file for UT. 

### 2023/06/15 orchagent/syncd workflow (bottle neck調査)
> 06/15 meeting minutes https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/34144

- zebra~fpmsyncd間の通信はボトルネックでは無い（Hasan調査による）
  - orchagent/syncd や Redis DB がボトルネック
- ボトルネック調査の解説 (Yubin Lee, Alibaba)
  - [Route enhancement in SONiC(1).pptx](https://lists.sonicfoundation.dev/g/sonic-wg-routing/files/Route%20enhancement%20in%20SONiC%281%29.pptx)
  - Orchagent, Syncd workflow 解説がとても参考になる
- データセンターネットワーク（DCN）からデータセンタ間（DCI）へユースケースを拡張すると、さらなるスケーラビリティが必要
  - Route Scale from 100k -> 1M+
  - route insert 性能を、現在の 8k/sec を 20k/sec にすることが目標
- Fast converge のためにはプロセス・スレッドの実行priorityを適切にセットする事が必要
- 将来的には orchagent/syncd を multi-thread 化したい

### 2023/06/22 ASOC途中経過報告：skip kernel routes, memory usage
> 06/22 meeting minutes https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/34200

ASOC途中経過報告：[各Issue一覧](https://github.com/sonic-net/sonic-buildimage/issues?q=label%3Arouting)

- [Routing WG] ASOC Intern project 4: Skip kernel routes downloading
  - Wenbo presented his plan on how to skip kernel routes programming
- [Routing WG] ASOC Intern project 1: Reduce bgp path memory usage
  - He Jun presented his plan on optimizing bgp_path_extra_info's memory usage
- [Routing WG] ASOC Intern project 2: Reduce bgp node memory usage
  - Yuqing presented her plan on BGP node break down

### 2023/06/29 SRv6 Policy 対応検討
> 06/29 meeting minutes https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/34260

SRv6 Policy サポートするにあたり FRR / SONiC communication channel に必要な改善を検討

- SRv6 policy の Insert 経路
  - pathd -> zebra -> (protobuf) -> fpmsyncd
  - SRv6 policy & My SID の protobuf フォーマットを新たに定義する
- route 解決のロジックを現在の orchagent から zebra に移動する
- orchagentの3段階のロードバランスロジックは platform (ASIC) 依存なので、orchagent のまま
  - ASICの制約により、フラットにする必要がある？
  - TODO: 具体的に何を指しているかは要確認

### 2023/07/06 FRR communication channel
> 07/06 meeting minutes https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/34289

- [FRR communication channel proposal v3.pdf](https://lists.sonicfoundation.dev/g/sonic-wg-routing/files/FRR%20communication%20channel%20proposal%20v3.pdf)
  - FRR/SONiC間のコミュニケーションチャネルが図示されていて参考になる
- frrcfgd vs bgpcfgd -> MSFTは bgpcfgd が良いと考えている

### 2023/07/13 Fpmsyncd NHG by NTT (ebiken)
> 07/13 meeting minutes https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/34321

- NTT(ebiken)による Fpmsyncd NHG 拡張提案の解説
  - [sonic-fmsyncd-nhg-NTT-20230714-01.pdf](https://lists.sonicfoundation.dev/g/sonic-wg-routing/files/sonic-fmsyncd-nhg-NTT-20230714-01.pdf)
- FpmsyncdのNHGサポートは BGP PIC 等にも利用できるため好意的
  - recursive routes handling 等、他の適用先もコメントがあった
- 本当にNHGを活かすにはFRR側の改善も必要
- 現在はNHGの NHID consistancy や階層的なNHG対応のために orchagent で NHG/NH ID をアサインしている
  - Fpmsyncd NHG拡張ではOrchagentの機能を活用されない（FRRがIDを管理）
  - メリデメをクリアにすると、どちらを利用するか分かり易くなる
- Default設定をOffにするなど、既存ユーザへの配慮が必要
- フィードバックを元にHLDを更新する

### 2023/07/20 Protobuf channel, Recursive NHG
> 07/20 meeting minutes https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/34378

- Protobuf channel proposal : https://lists.sonicfoundation.dev/g/sonic-wg-routing/files/wg%E5%88%86%E4%BA%AB.pptx
  - Protobuf対応によりnetlinkを壊さない事が重要
  - SONiC以外のプラットフォームでは protobuf が利用できない（利用しない）可能性があるため
- Alibaba Recursive NHG use case : https://lists.sonicfoundation.dev/g/sonic-wg-routing/files/recursive%20nexthop%20use%20case%20-%20Routing%20WG.pptx
  - FRR側でも大きな変更が必要なため、FRR weekly meeting にて Eddie が説明する

### 2023/07/27 Accton活動紹介、MSFT T2 zebra crash
> 07/27 meeting minutes https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/34402

- Accton の活動紹介
  - 企業紹介だが参加者でAccton知らない人いないのでは？
  - 3名の Software Engg を FRR/SONiC routing 担当としてアサインする
- Nokia (Sakthi, Keesara) による MSFT T2 テスト環境の解説（筐体版SONiC）
  - Linecard間のフルメッシュ通信にはiBGPが利用されている
  - 筐体外部とはeBGPで接続
  - routing policy を利用して ECMP を設定。最大 64 ECMP。
- Live core file check（recursive routeでクラッシュしたコアファイルの解析） by Hasan BRCM
  - FRR PR を適用したら crash しなくなった
  - MSFT zebra crash: https://github.com/sonic-net/sonic-buildimage/issues/15803

### 2023/08/03 improve routes downloading speed
> 08/03 meeting minutes https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/34499

- [improve routes downloading speed(2).pptx](https://lists.sonicfoundation.dev/g/sonic-wg-routing/files/improve%20routes%20downloading%20speed%282%29.pptx)
  - Improve Orchagent's Routes Downloading Speed
  - Yang Fengsheng, Alibaba
- 改善内容：10K/sec -> 16K/sec へ改善
  - Orchagent の APPL_DB -> ASIC_DB 処理のパイプライン化
  - Syncd へ新しい processBulkEvent function を追加
  - mutex buffer -> ring buffer への置き換え
- コメント
  - flush timer を大きくするとバッチ処理できて性能向上がある半面、convergenceで課題発生の可能性あるのでは？
  - Hasan は Zebraがボトルネックと主張。
  - sharpd は topotest で 1M routes 処理するのに 7sec しかかからない事を見せた。
- Action Item
  - large buffer のインパクト確認
  - BRCM TD4 ASIC の場合どうなるかテスト
  - LUA script への影響確認

### 2023/08/10 improve routes downloading speed
> 08/10 meeting minutes https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/34531

- [improve routes downloading speed (1).pptx](https://lists.sonicfoundation.dev/g/sonic-wg-routing/files/improve%20routes%20downloading%20speed%20%281%29.pptx)
- 8/03のAIだったテスト結果を共有（Fengsheng）
  - "Linux kernel -> zebra ACK message" を skip する事で fpmsyncd で 500K routes 処理する場合18秒から9秒に短縮できた。
- Zebra main thread の route 取り扱いについて確認
  - zebra's main thread handles BGP -> zebra message handling, Linux kernel -> zebra ACK message and zebra -> fpmsyncd message.
  - 但し、sharpd含め確信をもっていなかったので自分で確認する必要あり
- Hasan, Venket, Yunnan, Shangshuai and Fengsheng will form a small group to come up a routes loading time enhancement HDL.

### 2023/08/17 ASOC活動報告：memory optimization, BGP node breakup
> 08/17 meeting minutes https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/34597

- ASOC活動報告
- Jun He: [ASoC-Structure Memory Optimizations of FRR BGP.pdf](https://lists.sonicfoundation.dev/g/sonic-wg-routing/files/ASoC-Structure%20Memory%20Optimizations%20of%20FRR%20BGP.pdf)
- Yuqing Zhao: [BGP_nodeBreakupSummary_yuqing_0817.pdf](https://lists.sonicfoundation.dev/g/sonic-wg-routing/files/BGP_nodeBreakupSummary_yuqing_0817.pdf)

### 2023/09/07
> 09/07 meeting minutes https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/34786

### 2023/09/14
> 09/14 meeting minutes https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/34834

### 2023/09/21
> 09/21 meeting minutes https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/34949

### 2023/09/28
> 09/28 meeting minutes https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/34965

### 2023/10/05
> 10/05 meeting minutes https://lists.sonicfoundation.dev/g/sonic-wg-routing/wiki/35036

