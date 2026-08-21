## MODIFIED Requirements

### Requirement: ### 需求：可替换的 LLM 提供者抽象
后端 SHALL 暴露一个提供者抽象，以便后续的 OpenAI-compatible 模型提供者可以替换 Qwen 而不更改业务代码。

#### Scenario: Business code depends on abstraction
- **WHEN** 应用服务需要聊天模型访问权限
- **THEN** 它们 MUST 依赖于 LLM 提供商抽象，而不是直接构建特定提供商的客户端。

#### Scenario: 测试中可以提供提供者
- **WHEN** 测试会验证模型相关的行为
- **THEN** 它们 MUST 能够在不进行网络调用的情况下提供假的提供者或假的聊天模型。

#### Scenario: 提供者提供 Agent 兼容的聊天模型
- **WHEN** 流式聊天服务创建一个 LangChain Agent
- **THEN** 它 MUST 通过提供者抽象获取聊天模型，并将其传递给 `create_agent`。
