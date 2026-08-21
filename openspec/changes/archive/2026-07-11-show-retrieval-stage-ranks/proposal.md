## Why

当前后端已返回向量、BM25、RRF 和 rerank 分数，但对话引用摘要只展示“精排 99%”，用户无法判断文档在各召回阶段的来源、名次和分数。需要把三阶段检索轨迹完整暴露并以可扫描方式展示。

## What Changes

- 检索命中和引用新增 `vectorRank`、`bm25Rank`、`rerankRank`。
- 向量或 BM25 未命中的阶段使用空排名与空分数，最终 rerank 命中始终包含精排名次。
- 聊天 SSE、持久化引用和 AIOps 引用保持三阶段排名与分数。
- 前端引用摘要展示向量名次/相似度、BM25 名次/分数、rerank 名次/相关度。
- 引用详情以结构化阶段轨迹展示同一信息，并继续展示 RRF 融合分。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `knowledge-retrieval-tool`: 检索结果和引用增加三阶段排名契约。
- `api-and-sse-contracts`: 共享 HTTP/SSE 引用结构增加可选阶段排名字段。
- `knowledge-answer-citation-view`: 对话引用摘要和详情展示三个检索阶段的名次与分数。

## Impact

- 后端混合候选、检索结果、聊天与 AIOps 引用映射。
- TypeScript/OpenAPI/SSE 契约及测试。
- Vue 对话引用摘要、详情组件及组件测试。
- 不修改数据库 schema、Milvus collection、召回排序算法或模型配置。
