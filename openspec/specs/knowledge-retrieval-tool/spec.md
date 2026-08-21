# knowledge-retrieval-tool Specification

## Purpose

定义一个面向代理的、tenant 范围的知识检索工具，该工具仅在被调用时搜索索引文档 chunk，返回结构化结果和引用来源，并在处理空调用或不安全调用时不会虚构内容。

## Requirements

### Requirement: Agent-facing knowledge retrieval tool
后端 SHALL 提供一个知识检索工具，当代理需要 user 问题的文档上下文时可以调用该工具。

#### Scenario: 工具接受查询输入
- **WHEN** 调用工具时提供一个查询字符串
- **THEN** 它 MUST 并行执行查询嵌入与 Milvus 向量搜索，以及 tenant 范围内的内存 BM25 关键词搜索。

#### Scenario: 工具支持可选的 topK 和过滤器
- **WHEN** 工具输入包含可选的 `topK` 或过滤值
- **THEN** 工具 MUST 在对它们进行验证后，根据当前 user 的可访问知识库对两路召回应用一个有限的 topK 值和请求的过滤器。

#### Scenario: Retrieval is not a mandatory pre-step
- **WHEN** 一个 user 发送聊天问题
- **THEN** 后端 MUST NOT 在模型决定是否调用工具之前，作为无条件的固定步骤运行知识检索。

#### Scenario: Tool is exposed to LangChain Agent
- **WHEN** 为请求创建流式聊天 Agent
- **THEN** 后端 MUST 为 tenant 范围的知识检索功能提供一个 LangChain 工具，该工具绑定到当前 user 可访问的知识库。

#### Scenario: LangChain tool preserves structured output
- **WHEN** 的 Agent 调用知识检索 LangChain 工具
- **THEN** 的工具结果 MUST 保留结构化命中结果和引用来源，以便聊天流可以发出引用并持久化引用元数据。

### Requirement: Structured retrieval output
检索工具 SHALL 返回包含 chunk 内容、源文档详情、元数据、向量召回分、BM25 分、RRF 融合分和精排分的结构化结果，其中兼容字段 `score` SHALL 表示最终精排分。

#### Scenario: Hits include chunk and source data
- **WHEN** 混合召回和精排返回匹配的 chunks
- **THEN** 每个工具结果 MUST 包括 chunk ID、文档 ID、知识库 ID、内容、来源、元数据、可空的 `vectorScore`、可空的 `bm25Score`、`rrfScore`、`rerankScore` 和等于 `rerankScore` 的 `score`。

#### Scenario: 空搜索返回空结果
- **WHEN** 向量搜索和 BM25 搜索都不返回任何有权限的 chunk
- **THEN** 工具 MUST 返回一个空的 `results` 数组和 MUST NOT 生成文档内容或调用 rerank。

### Requirement: Retrieval citation sources
检索工具 SHALL 暴露与精排命中一一对应的引用来源，使使用 chunk 的 RAG 回答能够返回可追溯的分阶段分数引用。

#### Scenario: Citation payloads map to hits
- **WHEN** 工具返回一个或多个精排结果
- **THEN** 它 MUST 提供引用相同 chunk、文档、知识库、来源、元数据、向量召回分、BM25 分、RRF 融合分和精排分的引用负载。

#### Scenario: RAG answer can emit references
- **WHEN** 聊天回答使用检索结果
- **THEN** 答案流 MUST 能够从引用负载发出共享参考源事件，并保持精排降序和最多 5 条限制。

### Requirement: Two-stage reranked retrieval
知识检索工具 SHALL 对 tenant 权限过滤后的向量与 BM25 双路候选执行 `RRF(k=60)` 融合，再调用配置的真实 rerank 模型，并 SHALL 返回最多 5 条按精排分数降序排列的结果。

#### Scenario: 双路召回并行执行
- **WHEN** 当前 user 至少有一个可访问知识库且调用知识检索工具
- **THEN** 后端 MUST 并行执行最多 20 条 Milvus 向量候选召回和最多 20 条内存 BM25 关键词候选召回。

#### Scenario: RRF 融合候选
- **WHEN** 任一路粗召回返回有权限的候选 chunks
- **THEN** 后端 MUST 按 chunk ID 去重，并以每路排名贡献 `1 / (60 + rank)` 计算 RRF 分数，按融合分选择最多 20 条候选。

#### Scenario: 融合候选被精排
- **WHEN** RRF 返回一个或多个融合候选
- **THEN** 后端 MUST 将最多 20 条候选发送给 `qwen3-vl-rerank`，并按返回的 `relevance_score` 降序选择最多 5 条结果。

#### Scenario: 不设置最低分阈值
- **WHEN** rerank 返回有效的候选相对分数
- **THEN** 后端 MUST NOT 使用未声明的最低分阈值删除结果，并 MUST 仅按请求 topK 与 5 条硬上限截断。

#### Scenario: 粗召回分支不可用
- **WHEN** embedding、向量搜索、chunk 枚举或 BM25 排序失败
- **THEN** 工具 MUST 返回安全的统一系统错误，并 MUST NOT 静默退化为单路召回。

#### Scenario: 精排服务不可用
- **WHEN** rerank 请求在有限重试后失败或返回无效结构
- **THEN** 工具 MUST 返回安全的统一系统错误，并 MUST NOT 将向量、BM25 或 RRF 分数伪装成精排分数。

### Requirement: Safe retrieval failures
检索工具 SHALL 在遇到无效输入、未经授权的筛选器或基础设施故障时，使用统一的应用程序错误安全地失败。

#### Scenario: 缺失的查询将被拒绝
- **WHEN** 工具被调用时查询为空
- **THEN** 它将通过验证错误拒绝调用，并且 MUST NOT 搜索向量存储。

#### Scenario: Unauthorized knowledge base filter is rejected
- **WHEN** 将工具输入过滤到当前 user 可访问集之外的知识库
- **THEN** 它 MUST 以统一的授权错误拒绝调用，并 MUST NOT 查询 Milvus。

#### Scenario: Vector or embedding failure is safe
- **WHEN** 嵌入生成或向量搜索失败
- **THEN** 工具 MUST 返回或引发一个安全系统错误而不暴露秘密。

### Requirement: Non-negative BM25 lexical scoring
知识检索工具 SHALL 使用正 IDF 的 BM25 词法排序语义，并 SHALL NOT 为有关键词命中的候选返回负 `bm25Score`。

#### Scenario: 小语料精确词项保持正分
- **WHEN** tenant 语料只有一个或少量 chunks，查询精确命中错误码或专有词
- **THEN** 命中 chunk 的 `bm25Score` MUST 大于 0。

#### Scenario: 高频词项不产生负贡献
- **WHEN** 查询词项出现在超过一半的 tenant chunks 中
- **THEN** BM25 排序 MUST 为这些命中返回非负分，并 MUST NOT 因累积负 IDF 而惩罚包含更多查询词的文档。

#### Scenario: 未命中词项贡献为零
- **WHEN** 某个 chunk 不包含任何查询词项
- **THEN** 该 chunk MUST NOT 仅因 BM25 变体的常量或 delta 项进入关键词候选。

### Requirement: Retrieval stage rank traceability
知识检索工具 SHALL 为最终命中和引用保留向量召回、BM25 召回和 rerank 三阶段的一基排名。

#### Scenario: 候选在两路粗召回中命中
- **WHEN** 最终结果同时来自向量和 BM25 候选列表
- **THEN** 结果 MUST 包含对应的 `vectorRank`、`bm25Rank` 和最终 `rerankRank`。

#### Scenario: 候选只在单路粗召回中命中
- **WHEN** 最终结果只在向量或 BM25 一路出现
- **THEN** 未命中阶段的排名和分数 MUST 为空，命中阶段与 rerank 排名 MUST 保留。

#### Scenario: rerank 改变融合候选顺序
- **WHEN** rerank provider 返回与 RRF 候选顺序不同的排序
- **THEN** `rerankRank` MUST 表示最终输出位置，而不是候选输入 index。
