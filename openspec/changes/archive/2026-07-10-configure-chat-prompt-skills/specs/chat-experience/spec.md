## ADDED Requirements

### Requirement: Chat assembly controls
经过身份验证的 Chat 工作区 SHALL 让 user 可以在中文环境下查看、选择、确认和恢复其基于服务器的系统提示和多选技能配置。

#### Scenario: User opens chat configuration
- **WHEN** 已认证的 user 打开 Chat 工作区
- **THEN** 前端 MUST 通过共享合约加载当前配置，并显示保存的提示和技能，而不以 localStorage 作为事实来源。

#### Scenario: User confirms an updated assembly
- **WHEN** 一个 user 更改所选提示或技能并确认
- **THEN** 前端通过输入的 API 客户端保存 MUST，显示保存的装配摘要，并用于后续消息。

### Requirement: Collapsible assistant execution context
聊天工作区 SHALL 将每个助手消息的可用工具调用和模型提供的深度思考内容作为单独的中文、可使用键盘操作的、默认折叠的详细信息显示在该消息下方。

#### Scenario: Assistant used tools
- **WHEN** 流式或持久化的助手响应包含工具审计记录
- **THEN** 前端 MUST 在相应的助手消息下方显示折叠的工具调用摘要，并在 user 展开后才显示绑定的详细信息

#### Scenario: Assistant has reasoning content
- **WHEN** 流式或持久化助手响应包含模型提供的推理元数据
- **THEN** 前端 MUST 在该消息下方显示一个折叠的深度思考摘要，而不将推理作为最终答案文本展示。
