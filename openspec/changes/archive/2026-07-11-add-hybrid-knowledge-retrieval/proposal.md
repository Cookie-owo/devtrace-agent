## Why

当前知识检索只依赖 Milvus 向量召回，容易遗漏包含精确错误码、服务名、配置键或专有术语但语义向量排名不高的文档。需要加入 BM25 关键词召回并融合两路排名，再用现有 rerank 模型精排，以同时提高语义问题与精确关键词问题的召回质量。

## What Changes

- 将知识检索粗召回改为 Milvus 向量召回与 tenant 范围内的内存 BM25 关键词召回双路并行执行。
- 使用 Reciprocal Rank Fusion（RRF，`k=60`）对两路候选去重和融合，最多向 rerank 提交 20 条融合候选。
- 继续使用配置的真实 `qwen3-vl-rerank` 对融合候选精排，最终最多返回 5 条结果。
- 全链路严格应用当前用户、知识库、文档和 metadata 过滤，BM25 不得读取或排序无权限 chunk。
- 检索命中与引用新增 `bm25Score` 和 `rrfScore`，保留 `vectorScore`、`rerankScore`，兼容字段 `score` 继续表示最终精排分。
- 使用成熟 BM25 实现，并提供适合中英文混合运维文本的确定性分词。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `knowledge-retrieval-tool`: 将单路向量粗召回升级为向量与 BM25 双路并行召回、RRF 融合和 rerank 精排，并扩展检索分数契约。
- `milvus-vector-store`: 增加 tenant 范围内显式列举 chunk 的读取边界，为内存 BM25 提供受权限约束的语料。

## Impact

- 后端检索工具、Milvus 客户端协议与实现、聊天/AIOps 引用映射和测试。
- TypeScript 共享契约、OpenAPI schema 与对应契约测试。
- 后端新增 BM25 运行时依赖，`uv.lock` 随依赖更新。
- 不涉及数据库迁移，不改变 Milvus collection schema，也不改变 Agent 是否自主调用检索工具的行为。
