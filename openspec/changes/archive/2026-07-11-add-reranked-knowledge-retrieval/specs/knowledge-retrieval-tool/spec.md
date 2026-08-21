## ADDED Requirements

### Requirement: Two-stage reranked retrieval
知识检索工具 SHALL 在 tenant 权限过滤后的 Milvus 向量候选上调用配置的真实 rerank 模型，并 SHALL 返回最多 5 条按精排分数降序排列的结果。

#### Scenario: 候选内容被精排
- **WHEN** Milvus 返回当前 user 有权访问的候选 chunks
- **THEN** 后端 MUST 将最多 20 条候选发送给 `qwen3-vl-rerank`，并按返回的 `relevance_score` 降序选择最多 5 条结果

#### Scenario: 不设置最低分阈值
- **WHEN** rerank 返回有效的候选相对分数
- **THEN** 后端 MUST NOT 使用未声明的最低分阈值删除结果，并 MUST 仅按请求 topK 与 5 条硬上限截断

#### Scenario: 精排服务不可用
- **WHEN** rerank 请求在有限重试后失败或返回无效结构
- **THEN** 工具 MUST 返回安全的统一系统错误，并 MUST NOT 将向量分数伪装成精排分数

## MODIFIED Requirements

### Requirement: Structured retrieval output
检索工具 SHALL 返回包含 chunk 内容、源文档详情、元数据、向量召回分和精排分的结构化结果，其中兼容字段 `score` SHALL 表示最终精排分。

#### Scenario: Hits include chunk and source data
- **WHEN** 两阶段检索返回匹配的 chunks
- **THEN** 每个工具结果 MUST 包括 chunk ID、文档 ID、知识库 ID、内容、来源、元数据、`vectorScore`、`rerankScore` 和等于 `rerankScore` 的 `score`

#### Scenario: 空搜索返回空结果
- **WHEN** 向量搜索不返回任何有权限的 chunk
- **THEN** 工具 MUST 返回一个空的 `results` 数组和 MUST NOT 生成文档内容或调用 rerank

### Requirement: Retrieval citation sources
检索工具 SHALL 暴露与精排命中一一对应的引用来源，使使用 chunk 的 RAG 回答能够返回可追溯的双分数引用。

#### Scenario: Citation payloads map to hits
- **WHEN** 工具返回一个或多个精排结果
- **THEN** 它 MUST 提供引用相同 chunk、文档、知识库、来源、元数据、向量召回分和精排分的引用负载

#### Scenario: RAG answer can emit references
- **WHEN** 聊天回答使用检索结果
- **THEN** 答案流 MUST 能够从引用负载发出共享参考源事件，并保持精排降序和最多 5 条限制
