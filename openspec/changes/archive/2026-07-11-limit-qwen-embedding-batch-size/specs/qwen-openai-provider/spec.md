## ADDED Requirements

### Requirement: Qwen embedding batch compatibility
后端 SHALL 确保通过 OpenAI-compatible 接口发送给 `text-embedding-v4` 的每个 Embedding 请求最多包含 10 条文本，同时 MUST 为任意数量的输入返回顺序对应的完整向量集合。

#### Scenario: Small embedding input uses one compatible batch
- **WHEN** 调用方请求为不超过 10 条文本生成向量
- **THEN** Embedding 客户端 MUST 在单个不超过提供商上限的请求中处理这些文本

#### Scenario: Large embedding input is split into compatible batches
- **WHEN** 文档索引包含超过 10 个 chunk
- **THEN** Embedding 客户端 MUST 将输入拆分为每批最多 10 条的多个请求，并按输入顺序返回每个 chunk 的向量

#### Scenario: Large document indexing completes
- **WHEN** 一个可访问的文档被拆分为超过 10 个有效 chunk 且 Embedding 与 Milvus 服务可用
- **THEN** 索引任务 MUST 成功生成全部向量、写入全部 chunk 并标记为 `succeeded`
