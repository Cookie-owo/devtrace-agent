## MODIFIED Requirements

### Requirement: Knowledge retrieval tool contracts
系统 SHALL 导出共享知识检索工具 DTO，用于输入、过滤器、命中结果、引用来源和输出，并 SHALL 区分向量召回分与最终精排分。

#### Scenario: Retrieval DTOs are shared
- **WHEN** 前端或后端代码需要知识检索工具的形状
- **THEN** 它 MUST 使用共享合同定义检索查询、最多为 5 的可选 topK、过滤器、结果命中、引用来源、`vectorScore`、`rerankScore` 和空结果输出

#### Scenario: Retrieval output can represent no matches
- **WHEN** 没有检索到文档
- **THEN** 共享输出契约 MUST 表示一个空的 `results` 数组，而不生成回退内容

### Requirement: Knowledge retrieval citation events
共享 SSE 引用源合约 SHALL 支持从精排知识检索结果生成的引用，并统一双分数字段语义。

#### Scenario: Reference source carries retrieval identity
- **WHEN** 聊天流为检索到的知识 chunk 提供引用源
- **THEN** 事件负载 MUST 包含 chunk、文档和知识库的稳定标识符、源文本或 URI、元数据、`vectorScore`、`rerankScore`，且兼容字段 `score` MUST 等于 `rerankScore`
