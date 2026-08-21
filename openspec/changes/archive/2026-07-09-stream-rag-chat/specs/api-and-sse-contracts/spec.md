## MODIFIED Requirements

### Requirement: OpenAPI contract coverage
系统 SHALL 定义一个机器可读的 OpenAPI 合同，涵盖 health 检查、聊天、知识库、知识文档、文档索引任务、索引任务以及 AIOps 诊断。

#### Scenario: Health path is described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它应包含一个 health 检查端点，并具有成功响应模式。

#### Scenario: Chat paths are described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它 MUST 包括聊天会话创建、列表、历史记录、生命周期和统一的聊天消息流端点。

#### Scenario: Knowledge base paths are described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它应包含知识库列表和文档上传、列出、详细信息及删除的端点。

#### Scenario: Document upload policy is described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它 MUST 描述了文档上传的最大文件大小、允许的文件类型、重复哈希冲突行为以及显式覆盖行为。

#### Scenario: Document index task paths are described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它 MUST 包含用于创建文档索引任务、读取索引任务和重试失败的文档索引任务的受保护操作。

#### Scenario: Index task paths are described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它 MUST 包含索引任务创建和状态端点。

#### Scenario: AIOps diagnostic paths are described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它应包含诊断创建、状态和流式传输端点。

### Requirement: SSE event contract
系统 SHALL 为聊天流和 AIOps 诊断进度定义了区分的 SSE 事件契约。

#### Scenario: Required SSE event types exist
- **WHEN** 检查 SSE 事件类型目录
- **THEN** 它应包含内容差异、工具调用、参考源、任务状态、报告、完成和错误事件类型。

#### Scenario: Tool call lifecycle statuses exist
- **WHEN** 检查 SSE 工具调用事件契约
- **THEN** 它 MUST 表示工具调用的开始、增量、完成和失败状态。

#### Scenario: Chat stream uses shared events
- **WHEN** 聊天流式输出已实现
- **THEN** 它 MUST 仅发出符合共享 SSE 事件契约的事件有效载荷。

#### Scenario: AIOps stream uses shared events
- **WHEN** AIOps 诊断过程输出已实现
- **THEN** 它 MUST 仅发出符合共享 SSE 事件契约的事件负载。

### Requirement: Chat session management contracts
系统 SHALL 导出共享聊天会话和消息 DTO、请求类型、响应类型以及用于聊天会话管理和流式聊天发送的 OpenAPI 路径。

#### Scenario: Chat DTOs are shared
- **WHEN** 前端或后端代码需要聊天会话、聊天消息、消息元数据、列表响应、详细响应、创建请求、追加消息请求、流请求、清除响应或删除响应的结构
- **THEN** 它 MUST 会从 `packages/api-contracts` 使用共享的契约定义

#### Scenario: Chat lifecycle paths are described
- **WHEN** 检查 OpenAPI 合约
- **THEN** 它应包含用于创建会话、列出会话、读取会话历史、追加消息以供持久化使用、流式传输 user 发送、清除消息和删除会话的受保护路径。

#### Scenario: Chat message metadata is described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 聊天消息模式 MUST 包含能够携带引用参考和工具调用标识符的结构化元数据。

#### Scenario: Chat streaming path is described
- **WHEN** 检查 OpenAPI 合约
- **THEN** 它应包含一个受保护的 SSE 端点，用于流式传输聊天发送，请求体包含 user 内容和可选元数据。

#### Scenario: Chat protected responses are described
- **WHEN** 受保护的聊天会话管理路径将被检查
- **THEN** 它们 MUST 声明承载者身份验证并包含统一的 401 和 403 错误响应。
