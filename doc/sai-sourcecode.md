# SAIソースコードの場所と呼び出しフロー

> タイトルは内容に応じて適宜変更

## SAI の定義（ヘッダファイル）

https://github.com/opencomputeproject/SAI の [SAI: /inc](https://github.com/opencomputeproject/SAI/tree/master/inc) にヘッダファイルが存在する。
実質これがSAIの定義（スペック）となっている。



## SONiC 実装

```
sonic-swss/orchagent$ grep -r create_my_sid_entry
srv6orch.cpp:        status = sai_srv6_api->create_my_sid_entry(&my_sid_entry, (uint32_t) attributes.size(), attributes.data());
```

SAI_API_SRV6 という ID と、SAIの分類に応じたメソッドが格納されている構造体へのマップ

```
sonic-swss/orchagent$ grep SAI_API_SRV6 *

saihelper.cpp:    sai_api_query(SAI_API_SRV6,                 (void **)&sai_srv6_api);
saihelper.cpp:    sai_log_set(SAI_API_SRV6,                   SAI_LOG_LEVEL_NOTICE);
ebiken@dcig17:~/sandbox/sonic-swss/orchagent$ grep -r SAI_API_SRV6
saihelper.cpp:    sai_api_query(SAI_API_SRV6,                 (void **)&sai_srv6_api);
saihelper.cpp:    sai_log_set(SAI_API_SRV6,                   SAI_LOG_LEVEL_NOTICE);
```

SAIの分類ごとのメソッドを格納している場所

```
SAI/inc$ grep -r sai_srv6_api_t
saisrv6.h:typedef struct _sai_srv6_api_t
saisrv6.h:} sai_srv6_api_t;
sai.h:    SAI_API_SRV6             = 35, /**< sai_srv6_api_t */

> SAI/inc$ vi saisrv6.h
/**
 * @brief SRV6 methods table retrieved with sai_api_query()
 */
typedef struct _sai_srv6_api_t
{
    sai_create_srv6_sidlist_fn             create_srv6_sidlist;
    sai_remove_srv6_sidlist_fn             remove_srv6_sidlist;
    sai_set_srv6_sidlist_attribute_fn      set_srv6_sidlist_attribute;
    sai_get_srv6_sidlist_attribute_fn      get_srv6_sidlist_attribute;
    sai_bulk_object_create_fn              create_srv6_sidlists;
    sai_bulk_object_remove_fn              remove_srv6_sidlists;

    sai_create_my_sid_entry_fn             create_my_sid_entry;
    sai_remove_my_sid_entry_fn             remove_my_sid_entry;
    sai_set_my_sid_entry_attribute_fn      set_my_sid_entry_attribute;
    sai_get_my_sid_entry_attribute_fn      get_my_sid_entry_attribute;

    sai_bulk_create_my_sid_entry_fn        create_my_sid_entries;
    sai_bulk_remove_my_sid_entry_fn        remove_my_sid_entries;
    sai_bulk_set_my_sid_entry_attribute_fn set_my_sid_entries_attribute;
    sai_bulk_get_my_sid_entry_attribute_fn get_my_sid_entries_attribute;

} sai_srv6_api_t;
```

メソッドの定義

```
> SAI/inc$ vi saisrv6.h
typedef sai_status_t (*sai_create_my_sid_entry_fn)(
        _In_ const sai_my_sid_entry_t *my_sid_entry,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list);
```

## Tofino 実装

Tofino の SAI Driver のソースコードは公開されていないが、NDA/SLA契約を締結してアクセス可能な Intel SDE に含まれている。

SDEにアクセス可能な場合は `switch-p4-16/sai/*.cpp` を参照。


