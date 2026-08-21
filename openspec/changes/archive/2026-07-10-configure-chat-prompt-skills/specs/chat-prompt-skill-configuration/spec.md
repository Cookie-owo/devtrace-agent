## ADDED Requirements

### Requirement: User chat assembly configuration
系统 SHALL 应提供一个 user 范围的聊天装配配置，其中包含一个有效的系统提示预设和零个或多个来自项目受控目录的有效技能标识符。

#### Scenario: 首次配置读取会创建默认值
- **WHEN** 一个已认证的 user 读取聊天组装配置，且之前没有保存的记录
- **THEN** 系统 MUST 保留并返回配置的默认提示预设和 `frontend-design` 技能作为默认选择。

#### Scenario: User saves valid selections
- **WHEN** 一个经过身份验证的 user 选择一个目录提示和一个或多个目录技能，并确认配置
- **THEN** 系统 MUST 验证标识符，仅对该 user 保留选择，并返回保存的配置。

#### Scenario: Invalid catalog selection is rejected
- **WHEN** 请求包含未知的提示 ID 或技能 ID  
- **THEN** 系统 MUST 会以统一的验证错误拒绝它，并保留 user 之前的配置。

### Requirement: Server-side chat assembly
流式聊天服务 SHALL 从当前 Agent 的保存配置中构建后续的 user 系统提示，同时保留强制性的系统安全、引用、MCP 和当前时间指令。

#### Scenario: Saved configuration affects a later chat request
- **WHEN** 一个 user 保存配置，然后发送新的聊天消息
- **THEN** 这个 Agent MUST 作为其服务器端系统提示的一部分接收选定的提示和技能指令。

#### Scenario: Existing conversations remain intact
- **WHEN** 在对话已包含消息后更改其配置  
- **THEN** 系统 MUST 仅将新配置应用于后续的 Agent 执行以及 MUST NOT 不修改已持久化的消息或工具审计。

### Requirement: Truthful reasoning context
系统 SHALL 仅在模型事件流实际提供推理内容时才会生成并持久化深度思考上下文。

#### Scenario: 模型返回推理内容
- **WHEN** 一个 OpenAI-compatible 模型 chunk 包含支持的推理内容
- **THEN** 聊天流 MUST 会发出有序的推理增量，并将累积的推理与完成的助手消息元数据一起保存。

#### Scenario: 模型未返回推理内容
- **WHEN** 模型未返回推理内容
- **THEN** 系统 MUST NOT 生成一个推理事件或合成思维文本。
