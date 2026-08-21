## MODIFIED Requirements

### Requirement: User-owned data isolation
系统 SHALL 按 tenant 范围对知识库文档、向量 chunks、聊天会话、聊天消息、工具调用审计、AIOps 诊断任务、证据、报告和图 checkpoint 进行隔离。

#### Scenario: User lists owned data
- **WHEN** 一个 user 列出受保护的数据
- **THEN** 系统 MUST 仅返回该 user 的 tenant 范围内的记录。

#### Scenario: User accesses another tenant resource
- **WHEN** 已认证的 user 请求另一个 tenant 拥有的资源 ID
- **THEN** 系统 MUST 以统一的授权错误拒绝该请求。

#### Scenario: User manages owned documents
- **WHEN** 上传、列出、读取、删除或索引知识文档
- **THEN** 每个仓库和向量操作 MUST 必须作用于当前 user 的 tenant 范围内。

### Requirement: Frontend scoped data access
前端 SHALL 仅从作用域限定于当前 user 的已认证 API 调用中渲染受保护的知识库、知识文档、聊天和 AIOps 数据。

#### Scenario: Authenticated user views protected data
- **WHEN** 前端显示知识库、知识文档、聊天或 AIOps 部分
- **THEN** 它使用存储的认证令牌和当前-user 状态来请求作用域内的后端数据。

#### Scenario: User logs out
- **WHEN** 一个 user 注销
- **THEN** 前端 MUST 清除可见 UI 中的已认证状态和受保护的数据。
