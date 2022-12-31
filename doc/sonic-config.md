# SONiC Configuration

SONiC設定サンプル.
仮想環境の場合は仮想マシンやコンテナ関連の構築スクリプトを載せている場合があります。

Reference:
- [Edgecore SONiC のサポートサイト](https://support.edge-core.com/hc/en-us/categories/360002134713-Edgecore-SONiC) が充実しているので、本家の前にこちらを参照するのも良い。（OSS版ではサポートされていない機能や動作が異なる場合もあるので注意）

Samples:

- [demo01: Layer 2/3 with VLAN (type=bridge) on KVM](running-sonic-kvm.md#demo01-layer-23-with-vlan-typebridge)
  - libvirt domain 設定（sonic.xml） で `<interface type='bridge'>` を利用したサンプル
  - ホスト側に bridge & veth pair を作成する必要があるため、netns をホストと見立てたテストには煩雑
  - 逆に、スイッチやルーターの仮想インスタンスを接続する場合には有用な方式
- [demo02: Layer 2/3 with VLAN (type=network) on KVM](running-sonic-kvm.md#demo02-layer-23-with-vlan-typenetwork)
  - libvirt domain 設定（sonic.xml） で `<interface type='network'>` を利用したサンプル
  - ホスト側に bridge & veth pair 設定が不要なため、netns をホストと見立てたテストを簡単に実施可能

