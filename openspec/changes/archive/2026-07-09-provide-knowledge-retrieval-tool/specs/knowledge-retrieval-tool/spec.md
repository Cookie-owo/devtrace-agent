## ADDED Requirements

### Requirement: Agent-facing knowledge retrieval tool
后端 SHALL 提供一个知识检索工具，当代理需要 user 问题的文档上下文时可以调用该工具。

#### Scenario: 工具接受查询输入
- **WHEN** 调用工具时提供一个查询字符串
- **THEN** 它 MUST 对该查询进行嵌入，并通过向量存储边界执行向量搜索。

#### Scenario: 工具支持可选的 topK 和过滤器
- **WHEN** 工具输入包含可选的 `topK` 或过滤值
- **THEN** 工具 MUST 在对它们进行验证后，针对当前 user 的可访问知识库应用一个有限的 topK 值和请求的过滤器。

#### Scenario: Retrieval is not a mandatory pre-step
- **WHEN** 一个 user 发送聊天问题
- **THEN** 后端 MUST NOT 在模型决定是否调用工具之前，作为无条件的固定步骤运行知识检索。

### Requirement: Structured retrieval output
检索工具 SHALL 会返回包含 chunk 内容、源文档详情、元数据和相关性评分的结构化结果。

#### Scenario: Hits include chunk and source data
- **WHEN** 向量搜索返回匹配的 chunks
- **THEN** 每个工具结果 MUST 包括 chunk ID、文档 ID、知识库 ID、内容、来源、元数据和分数。

#### Scenario: 空搜索返回空结果
- **WHEN** 向量搜索不返回任何 chunk 
- **THEN** 工具 MUST 返回一个空的 `results` 数组和 MUST NOT 生成文档内容。

### Requirement: Retrieval citation sources
检索工具 SHALL 会暴露引用/来源数据，这些数据在使用 chunk 时，RAG 的回答可以返回。

#### Scenario: Citation payloads map to hits
- **WHEN** 工具返回一个或多个检索结果
- **THEN** 它 MUST 还会提供引用相同 chunk 的引用来源有效负载，包括文档、知识库、来源、元数据和评分。

#### Scenario: RAG answer can emit references
- **WHEN** 一个聊天回答使用检索结果
- **THEN** 答案流 MUST 能够发出从这些引用有效负载中派生的共享参考源事件。

### Requirement: Safe retrieval failures
检索工具 SHALL 在遇到无效输入、未经授权的筛选器或基础设施故障时，会安全地失败，并使用统一的应用程序错误。

#### Scenario: 缺少查询时将被拒绝
- **WHEN** 工具被调用时查询为空
- **THEN** 它将通过验证错误拒绝调用，并 MUST NOT 搜索向量存储。

#### Scenario: Unauthorized knowledge base filter is rejected
- **WHEN** 将工具输入过滤到当前 user 可访问集之外的知识库
- **THEN** 它 MUST 以统一的授权错误拒绝调用，并 MUST NOT 查询 Milvus。

#### Scenario: Vector or embedding failure is safe
- **WHEN** 嵌入生成或向量搜索失败
- **THEN** 工具 MUST 返回或引发一个安全系统错误，而不会暴露秘密。
