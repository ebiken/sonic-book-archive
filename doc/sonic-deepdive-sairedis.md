# sairedis

アーキテクチャ上は別物だが、実装としては sairedis と syncd は同じレポジトリに存在している。

- https://github.com/sonic-net/sonic-sairedis

sairedis の役割

- ASIC_DB に SAI Object を登録する際の API を提供（Orchagentが利用）
- ASIC_DB と ASIC の同期（syncd）


## orchagent -> sairedis -> ASIC_DB の流れ

orchagent は `SAI/inc/sai.h` や `sai<機能名>.h` に定義された API を呼び出しているが、それは SAI API ではなく ASIC_DB に書き込むための sairedis を呼び出している。
ASICにアクセスするためのSAI API の実装は、各 ASIC ベンダ提供の SAI Driver に実装があるが、それは `syncd` が呼び出している。
しかし、ASIC_DBにアクセスするための実装は（関数名直書きのコードとしては）存在しない。

よって、ここでは、同じAPI名（関数名）を利用して ASIC_DB にどうアクセスしているか、コードの流れ (code path) を理解する。

```
>>> SAI API の例
> SAI/inc/sai.h
typedef enum _sai_api_t
{
    SAI_API_UNSPECIFIED      =  0, /**< unspecified API */
    SAI_API_SWITCH           =  1, /**< sai_switch_api_t */
    SAI_API_PORT             =  2, /**< sai_port_api_t */
    SAI_API_FDB              =  3, /**< sai_fdb_api_t */
    SAI_API_VLAN             =  4, /**< sai_vlan_api_t */
    SAI_API_VIRTUAL_ROUTER   =  5, /**< sai_virtual_router_api_t */
    SAI_API_ROUTE            =  6, /**< sai_route_api_t */
    SAI_API_NEXT_HOP         =  7, /**< sai_next_hop_api_t */
    SAI_API_NEXT_HOP_GROUP   =  8, /**< sai_next_hop_group_api_t */
    SAI_API_ROUTER_INTERFACE =  9, /**< sai_router_interface_api_t */
    SAI_API_NEIGHBOR         = 10, /**< sai_neighbor_api_t */
    SAI_API_ACL              = 11, /**< sai_acl_api_t */
...
} sai_api_t;

> SAI/inc/sai_acl.h

/**
 * @brief Port methods table retrieved with sai_api_query()
 */
typedef struct _sai_acl_api_t
{
    sai_create_acl_table_fn                     create_acl_table;
    sai_remove_acl_table_fn                     remove_acl_table;
    sai_set_acl_table_attribute_fn              set_acl_table_attribute;
    sai_get_acl_table_attribute_fn              get_acl_table_attribute;
...
} } sai_acl_api_t;
```

## sairedis の関数定義マクロ

`orchagent -> sairedis -> ASIC_DB` の関数がどう定義されているのか？はマクロを理解することが必要

メモ

- From : https://hackmd.io/@octobersky/ryXksBmm_ : SAI
  - `Sai.cpp` is the core implmetation of redis_sai or sairedis module.
  - `sai_redis_switch.cpp` provide the sai_api_query input material.
  - It will help to bind the implementation of `Sai::redis_sai` with `sai_switch_api` table.
- `lib/sai_redis.h`
  - SAI API (`sai_*_t`) の type を持つ sairedis API (redis_*_api) が宣言されている
  - `redis_create_*` 等の関数を定義するマクロが定義されている
    - `REDIS_GENERIC_QUAD`
    - `REDIS_CREATE` etc.
    - `REDIS_CREATE_ENTRY` etc.
- `sairedis/lib/sai_redis_<feature>.cpp` に、 `const sai_<feat>_api_t redis_<feat>_api = {};` が定義されている。
  - 例えば SRv6 では以下２つが対応
    - `sairedis/lib/sai_redis_srv6.cpp` => `const sai_srv6_api_t redis_srv6_api = {`
    - `SAI/inc/saisrv6.h` => `typedef struct _sai_srv6_api_t { } sai_srv6_api_t;`
  - 
- orchagent から sai_srv6_api_t を呼んだ時に redis_srv6_api が実行されるマッピング
  - TODO

```
>> REDISマクロ展開例 SRv6 redis_srv6_api

> sai_redis_srv6.cpp (オリジナル)
REDIS_BULK_CREATE(SRV6_SIDLIST, srv6_sidlist);
REDIS_BULK_REMOVE(SRV6_SIDLIST, srv6_sidlist);
REDIS_GENERIC_QUAD(SRV6_SIDLIST,srv6_sidlist);
REDIS_BULK_QUAD_ENTRY(MY_SID_ENTRY,my_sid_entry);
REDIS_GENERIC_QUAD_ENTRY(MY_SID_ENTRY,my_sid_entry);

const sai_srv6_api_t redis_srv6_api = {

    REDIS_GENERIC_QUAD_API(srv6_sidlist)

    redis_bulk_create_srv6_sidlist,
    redis_bulk_remove_srv6_sidlist,

    REDIS_GENERIC_QUAD_API(my_sid_entry)
    REDIS_BULK_QUAD_API(my_sid_entry)
};

> 展開後 -> SAI/inc/saisrv6.h の sai_srv6_api_t 定義と同等になる。

const sai_srv6_api_t redis_srv6_api = {

    redis_create_srv6_sidlist,
    redis_remove_srv6_sidlist,
    redis_set_srv6_sidlist_attribute,
    redis_get_srv6_sidlist_attribute,

    redis_bulk_create_srv6_sidlist,
    redis_bulk_remove_srv6_sidlist,

    redis_create_my_sid_entry,
    redis_remove_my_sid_entry,
    redis_set_my_sid_entry_attribute,
    redis_get_my_sid_entry_attribute,
    
    redis_bulk_create_my_sid_entry,
    redis_bulk_remove_my_sid_entry,
    redis_bulk_set_my_sid_entry,
    redis_bulk_get_my_sid_entry,
};
```

### Orchagent がどうやって `redis_<feature>_api` を呼んでいるか？

- `orchagent/main.cpp` で `orchagent/saihelper.cpp:initSaiApi()` を実行。
- その中の `sai_api_query()` で SAI_API_XXX に応じた関数を
（`SAI/inc/sai.h` ではなく） `sai_redis_interfacequery.cpp:static` `sai_apis_t redis_apis` から拾って `sai_XXX_api` にセット。
- `sairedis/lib/sai_redis_interfacequery.cpp` の `static sai_apis_t redis_apis` と `SAI/lib/sai.h` の `sai_api_t` で関数の順番が同じである事を前提としている。結構壊れやすい実装に見えるが、このパターンでマッピングするのは良くあるパターン＆分かっていればコード量は少なくなる、のか？

```
~/sonic$ grep -r -E "redis_[a-z|0-9]*_api"
sonic-sairedis/lib/sai_redis_srv6.cpp:const sai_srv6_api_t redis_srv6_api = {
sonic-sairedis/lib/sai_redis_counter.cpp:const sai_counter_api_t redis_counter_api = {
sonic-sairedis/lib/sai_redis_wred.cpp:const sai_wred_api_t redis_wred_api = {
sonic-sairedis/lib/sai_redis.h:PRIVATE extern const sai_acl_api_t              redis_acl_api;
sonic-sairedis/lib/sai_redis.h:PRIVATE extern const sai_bfd_api_t              redis_bfd_api;
sonic-sairedis/lib/sai_redis.h:PRIVATE extern const sai_bmtor_api_t            redis_bmtor_api;
...

=> sonic-sairedis/lib/sai_redis_<feature>.cpp か sonic-sairedis/lib/sai_redis.h しか検索されない
```

sai_switch_api と Sai::redis_sai の対応付けをしている？
```

sonic-swss/orchagent/main.cpp
int main(int argc, char **argv)
{
...コマンドオプションの処理...
    initSaiApi();
    initSaiRedis(record_location, sairedis_rec_filename);
initSaiApi();
 -> sonic-swss/orchagent/saihelper.cpp
    void initSaiApi()
     -> sonic-sairedis/lib/sai_redis_interfacequery.cpp
        sai_api_query(SAI_API_SWITCH,  (void **)&sai_switch_api)
         -> *api_method_table = ((void**)&redis_apis)[sai_api_id - 1];

> sonic-sairedis/lib/sai_redis_interfacequery.cpp
#define API(api) .api ## _api = const_cast<sai_ ## api ## _api_t*>(&redis_ ## api ## _api)
static sai_apis_t redis_apis = {
    API(switch),
    API(port),
    API(fdb),
    API(vlan),
    API(virtual_router),
    API(route),
...

>> orchagent/saihelper.cpp

void initSaiApi()
{
...
    sai_api_initialize(0, (const sai_service_method_table_t *)&test_services);

    sai_api_query(SAI_API_SWITCH,               (void **)&sai_switch_api);
    sai_api_query(SAI_API_BRIDGE,               (void **)&sai_bridge_api);
    sai_api_query(SAI_API_VIRTUAL_ROUTER,       (void **)&sai_virtual_router_api);
    sai_api_query(SAI_API_PORT,                 (void **)&sai_port_api);
    sai_api_query(SAI_API_FDB,                  (void **)&sai_fdb_api);
...
}

>> sai_redis_interfacequery.cpp
> IDを指定する事により、sai_switch_api に api_method_table から sai_switch_api に関数ポインタをセットする
sai_status_t sai_api_query(
        _In_ sai_api_t sai_api_id,      => SAI_API_SWITCH
        _Out_ void** api_method_table)  => (void **)&sai_switch_api
{
...
    if (sai_metadata_get_enum_value_name(&sai_metadata_enum_sai_api_t, sai_api_id))
    {
        *api_method_table = ((void**)&redis_apis)[sai_api_id - 1];
        return SAI_STATUS_SUCCESS;
    }
...


static sai_apis_t redis_apis = {
    API(switch),
    API(port),
    API(fdb),
    API(vlan),
    API(virtual_router),
...
}

```



```
>sonic-sairedis/lib/sai_redis.h
sai_switch_api_t           redis_switch_api

PRIVATE extern std::shared_ptr<sairedis::SaiInterface>   redis_sai;

// QUAD OID
#define REDIS_CREATE(OT,ot)                             \
    static sai_status_t redis_create_ ## ot(            \
            _Out_ sai_object_id_t *object_id,           \
            _In_ sai_object_id_t switch_id,             \
            _In_ uint32_t attr_count,                   \
            _In_ const sai_attribute_t *attr_list)      \
{                                                       \
    SWSS_LOG_ENTER();                                   \
    return redis_sai->create(                           \
            (sai_object_type_t)SAI_OBJECT_TYPE_ ## OT,  \
            object_id,                                  \
            switch_id,                                  \
            attr_count,                                 \
            attr_list);                                 \
}
...
// QUAD DECLARE
#define REDIS_GENERIC_QUAD(OT,ot)  \
    REDIS_CREATE(OT,ot);           \
    REDIS_REMOVE(OT,ot);           \
    REDIS_SET(OT,ot);              \
    REDIS_GET(OT,ot);

... 他にも REDIS_BULK_QUAT_API 等のマクロが続いている ...


> sonic-sairedis/lib/sai_redis_switch.cpp
const sai_switch_api_t redis_switch_api = {

    redis_create_switch_uniq,
    redis_remove_switch,
    redis_set_switch_attribute,
    redis_get_switch_attribute,

    REDIS_GENERIC_STATS_API(switch)

    redis_switch_mdio_read,
    redis_switch_mdio_write,

    REDIS_GENERIC_QUAD_API(switch_tunnel)
};
```


## 参考文献

- [https://hackmd.io/@octobersky : SAI](https://hackmd.io/@octobersky/ryXksBmm_)
- 