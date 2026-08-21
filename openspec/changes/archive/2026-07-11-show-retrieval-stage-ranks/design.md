## Context

混合检索内部已经知道向量和 BM25 的源列表名次，rerank 结果也天然按最终名次返回，但这些位置没有进入 `KnowledgeRetrievalHit`。当前共享契约只有四种分数，前端详情能显示分数，而摘要硬编码只显示 rerank 百分比。

## Goals / Non-Goals

**Goals:**

- 让每个引用携带向量、BM25 和 rerank 三阶段名次。
- 在流式引用与持久化历史中保持同一数据结构。
- 在紧凑引用摘要和详情中清楚展示阶段、名次和分数。
- 明确展示某一路未召回，而不是伪造名次或 0 分。

**Non-Goals:**

- 不改变召回、RRF 或 rerank 排序算法。
- 不把 BM25 原始分转换为百分比。
- 不新增数据库列；引用继续存储在消息 JSON metadata。

## Decisions

### 排名使用一基序号并允许源阶段为空

新增 `vectorRank`、`bm25Rank` 和 `rerankRank`。名次从 1 开始，与用户看到的排序一致。关键词独占候选的 `vectorRank/vectorScore` 为 `null`，向量独占候选的 `bm25Rank/bm25Score` 为 `null`；最终结果一定有 `rerankRank`。

后端从 RRF 的 `ReciprocalRank.vector_rank` 和 `bm25_rank` 传递源名次；遍历 rerank 返回列表时用最终列表位置产生 `rerankRank`，不假设 provider 返回的输入 index 就是最终名次。

### 摘要使用三段紧凑阶段轨迹

引用条目在文档标题下展示三个短标签：

- `向量 #1 · 68%`
- `BM25 #1 · 8.630`
- `精排 #1 · 99%`

某一路未命中显示 `向量 未召回` 或 `BM25 未召回`。BM25 保留三位小数，向量和 rerank 使用百分比。详情面板使用相同术语并保留 RRF 融合分，避免摘要和详情语义分裂。

## Risks / Trade-offs

- [引用摘要信息密度增加] → 使用小型阶段标签并允许移动端换行，不增加新的卡片层级。
- [历史引用缺少排名字段] → 字段在 SSE/历史引用中保持可选，旧消息只展示现有分数。
- [向量相似度不一定严格限定在 0 到 1] → 前端仅对当前 COSINE 配置按百分比显示，不改变原始契约值。

## Migration Plan

1. 扩展后端模型、payload 与聊天/AIOps 映射。
2. 更新共享 TypeScript、OpenAPI 和测试。
3. 更新引用摘要、详情和 Vue 组件测试。
4. 运行全量检查并从真实前端检索验证三阶段展示。
5. 回滚无需数据迁移，旧持久化引用继续兼容。

## Open Questions

无。
