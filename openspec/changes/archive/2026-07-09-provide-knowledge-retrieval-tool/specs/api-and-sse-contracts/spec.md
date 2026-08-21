## ADDED Requirements

### Requirement: Knowledge retrieval tool contracts
系统 SHALL 导出共享知识检索工具的 DTO，用于输入、过滤器、命中结果、引用来源和输出。

#### Scenario: Retrieval DTOs are shared
- **WHEN** 前端或后端代码需要知识检索工具的结构
- **THEN** 它 MUST 可选地使用共享的合同定义进行检索查询、可选的 topK、过滤器、结果命中、引用来源和空结果输出。

#### Scenario: Retrieval output can represent no matches
- **WHEN** 没有检索到文档
- **THEN** 共享的输出契约 MUST 表示一个空的 `results` 数组，而不需要生成回退内容。

### Requirement: Knowledge retrieval citation events
共享的 SSE 引用源合约 SHALL 支持从知识检索命中生成的引用。

#### Scenario: Reference source carries retrieval identity
- **WHEN** 一个聊天流为检索到的知识提供引用源 chunk
- **THEN** 事件负载 MUST 应包含 chunk、文档和知识库的稳定标识符，以及源文本或 URI、元数据和评分。
