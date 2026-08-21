## Why

当前内存关键词召回使用 `BM25Okapi`，在小语料或词项出现在超过一半文档时会产生负 IDF，真实前端验证已经出现负 BM25 分数。这会降低分数可解释性，并可能让更完整的关键词匹配因累积更多负贡献而排名更低。

## What Changes

- 将内存关键词召回从 `BM25Okapi` 调整为使用正 IDF 的 `BM25L`。
- 保持未命中词项贡献为 0、仅有词项交集的文档进入 BM25 候选的现有规则。
- 增加单文档、小语料、高文档频率和精确错误码场景测试，保证 BM25 分数非负且更完整匹配排名更高。
- 保持向量召回、`RRF(k=60)`、rerank、候选数量和共享契约不变。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `knowledge-retrieval-tool`: 明确 BM25 关键词召回必须使用非负 IDF 语义，返回的 `bm25Score` 不得为负数。

## Impact

- 后端混合检索 BM25 scorer 工厂和对应单元测试。
- 不新增依赖，不修改数据库、Milvus collection 或 API schema。
