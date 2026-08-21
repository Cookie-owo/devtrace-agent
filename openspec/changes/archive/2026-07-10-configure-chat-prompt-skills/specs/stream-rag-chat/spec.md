## ADDED Requirements

### Requirement: Configured Agent system prompt
流式 RAG 聊天 Agent SHALL 在每次 Agent 调用时会使用当前 user 的持久化系统提示预设和选定的技能指令。

#### Scenario: Agent receives controlled prompt assembly
- **WHEN** 已认证的 user 发送流式聊天消息
- **THEN** 后端 MUST 通过 Repository 加载 user 的配置，并仅从项目控制的目录条目和强制性安全指令构建 Agent 系统提示。

### Requirement: Reasoning-aware streaming persistence
流式聊天服务 SHALL 在继续其现有的回答、工具、参考、完成和错误生命周期的同时，将模型提供的推理元数据与已完成的助手响应一起持久化。

#### Scenario: Completed response includes available reasoning
- **WHEN** 一个 Agent 在完成前返回答案差异和推理差异  
- **THEN** 持久化的助手元数据和完整结果 MUST 包含累积的推理，而不将其视为最终答案内容。
