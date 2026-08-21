## ADDED Requirements

### Requirement: Document index task contracts
系统 SHALL 导出共享文档索引任务 DTO、状态、请求类型和响应类型，用于前端和后端索引工作流。

#### Scenario: Index task DTOs are shared
- **WHEN** 前端或后端代码需要文档索引任务数据  
- **THEN** 它 MUST 使用共享的合同定义来指定索引任务 ID，owner user ID，知识库 ID，文档 ID，状态，失败原因，重试来源和时间戳。

#### Scenario: Index task status catalog is shared
- **WHEN** 前端或后端代码检查文档索引任务状态
- **THEN** 它 MUST 使用共享的 `pending`、`running`、`succeeded` 和 `failed` 状态目录。

## MODIFIED Requirements

### Requirement: OpenAPI contract coverage
系统 SHALL 定义一个机器可读的 OpenAPI 合同，涵盖 health 检查、聊天、知识库、知识文档、文档索引任务、索引任务以及 AIOps 诊断。

#### Scenario: Health path is described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它应包含一个 health 检查端点，并具有成功响应模式。

#### Scenario: Chat paths are described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它 MUST 包含聊天会话创建和聊天消息流式传输端点。

#### Scenario: Knowledge base paths are described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它包含知识库列表和文档上传、列出、详细信息及删除端点。

#### Scenario: Document upload policy is described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它 MUST 会描述最大文件大小、允许的文件类型、重复哈希冲突行为以及文档上传的显式覆盖行为。

#### Scenario: Document index task paths are described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它 MUST 包含用于创建文档索引任务、读取索引任务和重试失败的文档索引任务的受保护操作。

#### Scenario: Index task paths are described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它 MUST 应包含索引任务创建和状态端点。

#### Scenario: AIOps diagnostic paths are described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它应包含诊断创建、状态和流式处理端点。

### Requirement: Protected API contract security
系统 SHALL 将知识库、知识文档、文档索引、聊天和 AIOps API 合同标记为经过身份验证的表面。

#### Scenario: Protected paths include unauthorized response
- **WHEN** 保护聊天、知识库、知识文档、文档索引，或 AIOps OpenAPI 路径将被检查
- **THEN** 它们 MUST 将使用统一的错误响应模式返回 401 响应。

#### Scenario: Protected paths declare bearer auth
- **WHEN** 保护聊天、知识库、知识文档、文档索引，或 AIOps OpenAPI 操作将被检查
- **THEN** 它们通过 OpenAPI 安全方案声明承载者身份验证。

### Requirement: Protected API contract authorization responses
系统 SHALL 在认证失败响应之外，对受保护的知识库、知识文档、文档索引、聊天和 AIOps 操作返回授权失败响应。

#### Scenario: Protected paths include forbidden response
- **WHEN** 保护的聊天、知识库、知识文档、文档索引，或 AIOps OpenAPI 路径将被检查
- **THEN** 它们 MUST 将使用统一的错误响应模式返回 403 响应。

#### Scenario: Resource id paths are tenant scoped
- **WHEN** 受保护的路径针对特定的知识库、知识文档、文档索引任务、聊天会话或诊断ID
- **THEN** 其合同 MUST 要求持有者认证，并通过共享授权错误响应描述被禁止的访问。
