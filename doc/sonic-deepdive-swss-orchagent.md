# Deep Dive: SwSS: orchagent

https://github.com/sonic-net/sonic-swss/tree/master/orchagent

ポイント

- `/orchagent/main.cpp` が `/usr/bin/orchagent` として実行される。
- `orchDaemon` がデーモンとしての処理実装
- 以下３つのDBと接続する
  - DBConnector appl_db("APPL_DB", 0);
  - DBConnector config_db("CONFIG_DB", 0);
  - DBConnector state_db("STATE_DB", 0);
- `/orchagent/` の下には様々な `*.cpp` プログラムがあるが、必ずしも orchagent の一部ではなく、コマンドとして実行可能なものもある（例： `routeresync.cpp`）
- orchDaemon.h で `#include` されている `XXXorch.h` が実際の変換ロジックの実装
  - `class Srv6Orch : public Orch` のように、`XxxOrch` クラスが各ファイルで定義され、`orchDaemon` で `gSrv6Orch = new Srv6Orch(m_applDb, srv6_tables, gSwitchOrch, vrf_orch, gNeighOrch);` のようにインスタンス化されている。
  - `XxxOrch` のインスタンスは `orchdaemon.cpp: bool OrchDaemon::init()` で `m_orchList.push_back(gFdbOrch);` のように `m_orchList` に保存される。
- `for (Orch *o : m_orchList) { o->doTask(); }` のように、各クラスの `doTask()` ループが実行される


メモ

- `routeresync.cpp`
  - `routersync start|stop` を実行すると `APPL_DB` に `ROUTE_TABLE:resync` エントリを追加・削除する。
