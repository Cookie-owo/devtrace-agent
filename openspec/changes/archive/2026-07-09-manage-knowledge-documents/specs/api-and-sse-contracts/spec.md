## MODIFIED Requirements

### Requirement: OpenAPI contract coverage
系统 SHALL 定义一个机器可读的 OpenAPI 合同，涵盖 health 检查、聊天、知识库、知识文档、索引任务和 AIOps 诊断。

#### Scenario: Health path is described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它应包含一个 health 检查端点，并具有成功的响应模式。

#### Scenario: Chat paths are described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它 MUST 包含聊天会话创建和聊天消息流式传输端点。

#### Scenario: Knowledge base paths are described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它应包含知识库列表和文档上传、列出、详细信息及删除的端点。

#### Scenario: Document upload policy is described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它 MUST 描述最大文件大小、允许的文件类型、重复哈希冲突行为以及文档上传的显式覆盖行为。

#### Scenario: Index task paths are described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它 MUST 包含索引任务创建和状态端点。

#### Scenario: AIOps diagnostic paths are described
- **WHEN** 检查 OpenAPI 合约
- **THEN** 它应包含诊断创建、状态和流式传输端点。

### Requirement: Protected API contract security
系统 SHALL 将知识库、知识文档、聊天和 AIOps API 合同标记为认证表面。

#### Scenario: Protected paths include unauthorized response
- **WHEN** 保护聊天、知识库、知识文档或 AIOps OpenAPI 路径将被检查
- **THEN** 它们 MUST 将使用统一的错误响应模式返回 401 响应

#### Scenario: Protected paths declare bearer auth
- **WHEN** 保护的聊天、知识库、知识文档或 AIOps OpenAPI 操作将被检查
- **THEN** 他们 MUST 通过 OpenAPI 安全方案声明承载者身份验证。

### Requirement: Protected API contract authorization responses
系统 SHALL 除了认证失败响应外，还会对授权失败的受保护知识库、知识文档、聊天和 AIOps 操作返回授权失败响应。

#### Scenario: Protected paths include forbidden response
- **WHEN** 受保护的聊天、知识库、知识文档或 AIOps OpenAPI 路径将被检查
- **THEN** 它们 MUST 将使用统一的错误响应模式返回 403 响应。

#### Scenario: Resource id paths are tenant scoped
- **WHEN** 受保护的路径针对特定的知识库、知识文档、聊天会话或诊断ID  
- **THEN** 它们的契约 MUST 要求持有者身份验证，并通过共享的授权错误响应描述被禁止的访问。

## ADDED Requirements

### Requirement: Knowledge document contracts
系统 SHALL 导出共享知识文档 DTO、上传策略常量和前端及后端文档管理的响应类型。

#### Scenario: Document DTOs are shared
- **WHEN** 前端或后端代码需要文档元数据结构
- **THEN** 它 MUST 会使用共享的契约定义，包括文档摘要、文档详情、上传响应、列表响应、删除响应、文档状态和索引状态。

#### Scenario: Upload policy constants are shared
- **WHEN** 前端或后端代码验证文档上传策略
- **THEN** 它 MUST 使用共享的合同值来确定最大文件大小、允许的 MIME 类型、允许的扩展名以及覆盖行为。
