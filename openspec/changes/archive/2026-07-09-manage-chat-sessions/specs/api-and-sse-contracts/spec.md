## ADDED Requirements

### Requirement: Chat session management contracts
系统 SHALL 导出共享聊天会话和消息 DTO、请求类型、响应类型以及用于聊天会话管理的 OpenAPI 路径。

#### Scenario: Chat DTOs are shared
- **WHEN** 前端或后端代码需要聊天会话、聊天消息、消息元数据、列表响应、详细响应、创建请求、追加消息请求、清除响应或删除响应的结构
- **THEN** 它 MUST 将从 `packages/api-contracts` 共享契约定义中使用

#### Scenario: Chat lifecycle paths are described
- **WHEN** 检查 OpenAPI 合约
- **THEN** 它 MUST 应包含用于创建会话、列出会话、读取会话历史记录、追加消息、清除消息和删除会话的受保护路径。

#### Scenario: Chat message metadata is described
- **WHEN** 检查 OpenAPI 合约
- **THEN** 聊天消息模式 MUST 包含结构化元数据，能够携带引用参考和工具调用标识符。

#### Scenario: Chat protected responses are described
- **WHEN** 受保护的聊天会话管理路径将被检查
- **THEN** 它们 MUST 声明承载认证并包含统一的 401 和 403 错误响应。
