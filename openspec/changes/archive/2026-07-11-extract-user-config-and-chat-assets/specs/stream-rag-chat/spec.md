## MODIFIED Requirements

### Requirement: Configured Agent system prompt
流式 RAG 聊天 Agent SHALL 在每次 Agent 调用时使用当前 user 持久化选择的系统提示词正文和所选 Skill 文件内容。

#### Scenario: Agent receives selected user prompt assembly
- **WHEN** 已认证的 user 发送流式聊天消息
- **THEN** 后端 MUST 通过 Repository 加载当前 user 的聊天配置和系统提示词，并将该提示词正文传递给 Agent system prompt。

#### Scenario: Agent receives selected user Skill assembly
- **WHEN** 已认证的 user 选择一个或多个自己上传的 `SKILL.md` 并发送流式聊天消息
- **THEN** 后端 MUST 通过 Repository 加载这些 Skill 的文件名和内容，并将其作为动态 Skill 指令装配进 Agent system prompt。

#### Scenario: Mandatory system instructions are preserved
- **WHEN** 后端装配用户提示词和 Skill
- **THEN** system prompt MUST 同时保留强制性的安全、引用、MCP 查询和当前时间工具调用指令。
