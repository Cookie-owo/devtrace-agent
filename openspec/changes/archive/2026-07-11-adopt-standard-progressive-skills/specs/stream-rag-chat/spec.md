## MODIFIED Requirements

### Requirement: Configured Agent system prompt
流式 RAG 聊天 Agent SHALL 在每次 Agent 调用时使用当前 user 持久化选择的系统提示词正文，并通过 `langchain.agents.create_agent`、轻量 Skill catalog 和 `load_skill` Tool 向模型提供所选 Skill 的渐进式加载能力。

#### Scenario: Agent receives selected user prompt assembly
- **WHEN** 已认证的 user 发送流式聊天消息
- **THEN** 后端 MUST 通过 Repository 加载当前 user 的聊天配置和系统提示词，并将该提示词正文传递给 Agent system prompt

#### Scenario: Agent discovers selected user Skills
- **WHEN** 已认证的 user 选择一个或多个自己上传的标准 `SKILL.md` 并发送流式聊天消息
- **THEN** 后端 MUST 通过 user-scoped Repository 加载这些 Skill，使模型先看到 name 和 description，并仅能通过 `load_skill(name)` Tool 在相关时读取完整内容

#### Scenario: Unselected Skill is unavailable
- **WHEN** 当前 user 未选择某个已上传 Skill 或该 Skill 属于另一个 user
- **THEN** 本次 Agent 的 Skill catalog 和 `load_skill` registry MUST NOT 包含该 Skill

#### Scenario: Mandatory system instructions are preserved
- **WHEN** 后端装配用户提示词并创建 Agent
- **THEN** system prompt MUST 同时保留强制性的安全、引用、MCP 查询和当前时间工具调用指令，并且 MUST NOT 包含所选 Skill 的完整 Markdown 正文
