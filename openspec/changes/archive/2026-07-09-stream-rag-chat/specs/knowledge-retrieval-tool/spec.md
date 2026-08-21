## MODIFIED Requirements

### Requirement: Agent-facing knowledge retrieval tool
后端 SHALL 提供一个知识检索工具，当 Agent 需要 user 问题的文档上下文时可以调用该工具。

#### Scenario: 工具接受查询输入
- **WHEN** 调用工具时传入一个查询字符串
- **THEN** 它 MUST 对该查询进行嵌入，并通过向量存储边界执行向量搜索。

#### Scenario: 工具支持可选的 topK 和过滤器
- **WHEN** 工具输入包含可选的 `topK` 或过滤值
- **THEN** 工具 MUST 在对它们进行验证后，根据当前 user 的可访问知识库应用一个有限的 topK 值和请求的过滤器。

#### Scenario: Retrieval is not a mandatory pre-step
- **WHEN** 一个 user 发送聊天问题
- **THEN** 后端 MUST NOT 在模型决定是否调用工具之前，作为无条件的固定步骤运行知识检索。

#### Scenario: Tool is exposed to LangChain Agent
- **WHEN** 为请求创建流式聊天 Agent
- **THEN** 后端 MUST 为 tenant 范围的知识检索功能提供作为 LangChain 工具，该工具绑定到当前 user 可访问的知识库。

#### Scenario: LangChain tool preserves structured output
- **WHEN** 的 Agent 调用知识检索 LangChain 工具  
- **THEN** 的工具结果 MUST 保留结构化的命中结果和引用来源，以便聊天流可以发出引用并持久化引用元数据。
