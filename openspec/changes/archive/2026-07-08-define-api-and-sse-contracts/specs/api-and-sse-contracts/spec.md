## ADDED Requirements

### Requirement: Unified HTTP response envelope
系统 SHALL 定义一个共享的 HTTP 响应封装，该封装使用稳定的鉴别器来表示成功响应、业务错误、验证错误和系统错误。

#### Scenario: Successful API response
- **WHEN** 端点成功
- **THEN** 响应契约 MUST 使用成功区分器，包含类型化的 `data`，并包含请求元数据。

#### Scenario: Business error response
- **WHEN** 一个领域规则阻止了该操作  
- **THEN** 响应契约 MUST 使用错误区分器，包括业务错误代码、消息和可选的详细信息列表。

#### Scenario: Validation error response
- **WHEN** 请求参数无效
- **THEN** 响应契约 MUST 包含带有字段路径、消息和验证代码的参数级验证详细信息。

#### Scenario: System error response
- **WHEN** 发生意外的基础设施或服务器故障
- **THEN** 响应契约 MUST 应包含系统错误代码和安全消息，而不会泄露秘密或内部堆栈跟踪。

### Requirement: Unified error code catalog
系统 SHALL 定义一个带有稳定代码标识符、分类、HTTP 状态映射和默认消息的共享错误代码目录。

#### Scenario: Error code has category and message
- **WHEN** 导出一个错误代码
- **THEN** 它 MUST 包含一个类别、HTTP 状态和默认消息，前端和后端都可以使用。

#### Scenario: SSE error reuses error structure
- **WHEN** 流操作会发出错误事件
- **THEN** SSE 有效负载 MUST 重用与 HTTP 错误响应相同的结构化错误消息格式。

### Requirement: OpenAPI contract coverage
系统 SHALL 定义了一个机器可读的 OpenAPI 合同，涵盖 health 检查、聊天、知识库、索引任务和 AIOps 诊断。

#### Scenario: Health path is described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它必须包含一个 health 检查端点，并具有成功的响应模式。

#### Scenario: Chat paths are described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它 MUST 包含聊天会话创建和聊天消息流式传输端点。

#### Scenario: Knowledge base paths are described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它 MUST 包含知识库列表和文档摄入端点。

#### Scenario: Index task paths are described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它 MUST 包含索引任务创建和状态端点。

#### Scenario: AIOps diagnostic paths are described
- **WHEN** 检查 OpenAPI 合约
- **THEN** 它应包含诊断创建、状态和流式传输端点。

### Requirement: SSE event contract
系统 SHALL 为聊天流和 AIOps 诊断进度定义了一个具有区分性的 SSE 事件契约。

#### Scenario: Required SSE event types exist
- **WHEN** 检查 SSE 事件类型目录
- **THEN** 它应包含内容差异、工具调用、参考源、任务状态、报告、完成和错误事件类型。

#### Scenario: Chat stream uses shared events
- **WHEN** 聊天流输出已实现
- **THEN** 它 MUST 仅发出符合共享 SSE 事件契约的事件负载。

#### Scenario: AIOps stream uses shared events
- **WHEN** AIOps 诊断过程输出已实现
- **THEN** 它 MUST 仅发出符合共享 SSE 事件契约的事件负载。

### Requirement: Single source contract consumption
前端和后端 SHALL 实现 API 响应和 SSE 事件从 `packages/api-contracts` 和 MUST NOT 构建临时端点或事件结构。

#### Scenario: Frontend imports shared contracts
- **WHEN** 前端代码需要 HTTP 响应或 SSE 事件类型
- **THEN** 它 MUST 从 `packages/api-contracts` 导入它们。

#### Scenario: Backend aligns with shared contracts
- **WHEN** 后端端点模型或流式事件已实现
- **THEN** 它们 MUST 必须与导出的 `packages/api-contracts` 响应、错误、OpenAPI 和 SSE 合同形状匹配。
