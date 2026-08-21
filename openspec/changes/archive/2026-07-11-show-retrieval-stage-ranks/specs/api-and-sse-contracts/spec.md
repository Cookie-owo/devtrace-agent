## ADDED Requirements

### Requirement: Retrieval stage rank contracts
共享 HTTP 与 SSE 引用契约 SHALL 支持向量、BM25 和 rerank 阶段排名，并与对应分数字段一起传递。

#### Scenario: 新引用通过 SSE 到达
- **WHEN** 聊天或 AIOps 发出知识库 `reference.source`
- **THEN** 引用 MUST 能够包含 `vectorRank`、`bm25Rank`、`rerankRank` 及对应阶段分数。

#### Scenario: 单路未召回
- **WHEN** 引用只来自一个粗召回阶段
- **THEN** 契约 MUST 允许另一个粗召回阶段的排名和分数为空，且 MUST 保留最终 rerank 排名和分数。
