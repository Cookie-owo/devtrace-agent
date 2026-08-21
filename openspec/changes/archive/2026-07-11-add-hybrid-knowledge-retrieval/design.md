## Context

当前 `KnowledgeRetrievalTool` 先生成 query embedding，再从 Milvus 召回最多 20 条向量候选，经过权限和业务过滤后调用 `qwen3-vl-rerank`。这种实现对自然语言改写较稳健，但精确错误码、配置键、英文服务名和中文专有词可能因向量相似度不足而完全进不了精排候选集。

Milvus 是 chunk 的现有主存储，collection 已包含 BM25 所需的 `content`、文档、知识库、owner、tenant 和 metadata 字段。项目必须保持 tenant 隔离、Agent 自主选择工具、真实 rerank provider 和不在模块导入时连接外部系统等现有约束。

## Goals / Non-Goals

**Goals:**

- 并行执行语义向量召回和内存 BM25 关键词召回。
- 用 `RRF(k=60)` 融合两路排名，并对 chunk 去重。
- 用真实 rerank 模型精排融合后的最多 20 条候选，最终最多返回 5 条。
- 在所有分支读取内容前应用 tenant、知识库、文档和 metadata 过滤。
- 通过共享契约暴露向量、BM25、RRF 和 rerank 四个阶段的可解释分数。

**Non-Goals:**

- 不将 BM25 索引持久化到 SQLite、Milvus sparse vector 或新的搜索服务。
- 不改变 Milvus collection schema、向量索引或文档切分流程。
- 不设置最低相关度阈值，不改变 Agent 自主决定是否调用检索工具的行为。

## Decisions

### 使用 Milvus tenant-scoped query iterator 构建请求内 BM25 语料

向量存储新增 `list_chunks` 边界，通过 Milvus `query_iterator` 分批读取当前 tenant 与允许知识库内的标量 chunk 字段，不读取 vector。检索工具在应用文档和 metadata 过滤后，以这些 chunk 构建请求内 BM25 索引。

选择请求内索引而不是进程全局缓存，是因为文档可被随时新增、重建或删除，缓存失效会显著增加一致性与权限泄漏风险。该边界也避免业务层直接依赖 PyMilvus。

### 使用 `rank-bm25` 与中英文混合分词

BM25 排序使用成熟的 `rank-bm25` `BM25Okapi`。分词器将连续英文/数字/配置符号归一化为词项，并为连续中文生成单字和二元词项，使错误码、API 路径、服务名以及中文短语都能参与关键词匹配。空 query 或全零分不产生 BM25 候选。

未选择手写 BM25 公式，避免在文档频率、长度归一化和边界条件上产生不必要偏差；未引入完整中文分词服务，因为当前目标是本地、确定性、零额外运行时服务的关键词召回。

### 两路异步并行并在业务过滤后融合

使用 `asyncio.gather` 同时运行：

1. query embedding 与 Milvus vector search；
2. tenant-scoped chunk 枚举与 BM25 排序。

PyMilvus 的同步操作通过 `asyncio.to_thread` 执行，避免阻塞事件循环。两路结果都再次经过统一 `_filter_hits` 防御性过滤，然后各保留最多 20 条。

### 使用 RRF(k=60) 融合并保留分阶段分数

候选按 `chunk_id` 去重，每个列表中第 `rank` 名贡献 `1 / (60 + rank)`，同一 chunk 在两路命中时贡献相加。按 RRF 分数降序选择最多 20 条进入 rerank；并列时按最佳单路名次及 chunk id 确定性排序。

命中和引用保留：

- `vectorScore`: 向量分支命中时的 Milvus 相似度，否则为 `null`；
- `bm25Score`: BM25 分支命中时的原始 BM25 分，否则为 `null`；
- `rrfScore`: 两路排名融合分；
- `rerankScore`: 最终精排分；
- `score`: 继续等于 `rerankScore`。

### 任一粗召回分支失败时显式失败

双路召回是声明的产品语义，因此 embedding、向量搜索、chunk 枚举或 BM25 构建失败时均返回统一检索不可用错误，不静默退化为单路。rerank 失败继续沿用现有显式失败策略。

## Risks / Trade-offs

- [大知识库的请求内 BM25 会增加内存和延迟] → 使用 Milvus iterator 分批读取、不读取 vector，并只保留排序后的 20 条；后续可在不改变检索工具边界的情况下替换为持久 sparse index。
- [中英文启发式分词不等同于语言学分词] → 同时保留单字与二元词项，并由向量分支补足语义召回；用中文、英文、错误码测试覆盖行为。
- [两路都依赖 Milvus，严格意义上不是双存储高可用] → 本次目标是双检索算法提升召回率，不把它表述为基础设施容灾。
- [新增分数可能影响旧前端解析] → 新字段定义为可选/可空，`score` 与 `rerankScore` 的既有语义保持不变。

## Migration Plan

1. 增加 BM25 依赖、Milvus chunk 列举能力和单元测试。
2. 改造检索工具并更新共享/OpenAPI/SSE 契约。
3. 运行后端、前端、契约和 OpenSpec 全量验证，并对真实 Milvus 文档执行检索验证。
4. 回滚时整体回退该变更；无数据库或 collection 迁移。

## Open Questions

无。
