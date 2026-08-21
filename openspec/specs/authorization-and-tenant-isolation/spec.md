# authorization-and-tenant-isolation Specification

## Purpose
定义用户权限控制和 tenant 隔离边界，确保知识库、向量数据、聊天、工具审计和 AIOps 诊断数据都只能由当前授权 user 访问。
## Requirements
### Requirement: Tenant scope identity
系统 SHALL 将经过身份验证的 user ID 用作 tenant 范围，用于 user 拥有数据，直到引入单独的组织 tenant 模型。

#### Scenario: Authenticated request establishes tenant scope
- **WHEN** 一个受保护的 API 请求解析有效的 bearer 会话
- **THEN** 后端 MUST 将当前 user 的 id 作为 tenant 范围传递给下游数据访问代码。

#### Scenario: Anonymous request has no tenant scope
- **WHEN** 请求没有有效的身份验证 user
- **THEN** 后端 MUST NOT 访问该请求的 user 专属数据存储库。

### Requirement: User-owned data isolation
系统 SHALL 按 tenant 范围隔离知识库文档、文档索引任务、向量 chunks、聊天会话、聊天消息、工具调用审计、AIOps 诊断任务、证据、报告和图 checkpoints。

#### Scenario: User lists owned data
- **WHEN** 一个 user 列表包含受保护的数据
- **THEN** 系统 MUST 仅返回该 user 的 tenant 范围内的记录。

#### Scenario: User accesses another tenant resource
- **WHEN** 一个经过身份验证的 user 请求另一个 tenant 拥有的资源 ID
- **THEN** 系统 MUST 以统一的授权错误拒绝该请求。

#### Scenario: User manages owned documents
- **WHEN** 上传、列出、读取、删除或索引知识文档
- **THEN** 每个仓库和向量操作 MUST 必须在当前 user 的 tenant 范围内。

### Requirement: Scoped vector metadata
系统 SHALL 在向量 chunk 元数据中包含 owner、user 和 tenant 信息，用于 Milvus 索引和检索。

#### Scenario: 创建块元数据
- **WHEN** 一个文档 chunk 被准备用于向量索引
- **THEN** 其元数据 MUST 包括 `ownerUserId`、`tenantId`、`knowledgeBaseId`、`documentId` 和 `chunkId`。

#### Scenario: Retrieval applies tenant filter
- **WHEN** 是一个检索工具，用于搜索向量 chunks
- **THEN** 它会根据当前 tenant 的作用域进行过滤，并且只包含 user 可以访问的知识库。

#### Scenario: Retrieval rejects unauthorized filters
- **WHEN** 检索工具调用请求了当前 user 的 tenant 范围外的知识库
- **THEN** 系统 MUST 以统一授权错误拒绝该调用，并 MUST NOT 搜索 Milvus。

#### Scenario: Retrieval omits inaccessible data
- **WHEN** 检索工具调用成功完成
- **THEN** 每个返回的命中项和引用来源 MUST 都属于当前 tenant 范围内且可访问的知识库。

### Requirement: Frontend scoped data access
前端 SHALL 仅从作用域限定于当前 user 的经过身份验证的 API 调用中渲染受保护的知识库、知识文档、聊天和 AIOps 数据。

#### Scenario: Authenticated user views protected data
- **WHEN** 前端显示知识库、知识文档、聊天或 AIOps 部分
- **THEN** 它使用存储的认证令牌和当前-user 状态来请求作用域后端数据。

#### Scenario: User logs out
- **WHEN** 一个 user 注销
- **THEN** 前端 MUST 清除认证状态和受保护数据从可见的用户界面中。

### Requirement: Unified authorization denial
系统 SHALL 为未被授权访问受保护资源的已认证调用者使用共享的授权错误结构。

#### Scenario: Forbidden access response
- **WHEN** 已认证的 user 尝试跨 tenant 访问
- **THEN** 后端 MUST 返回统一的错误封装，包含权限错误码和 HTTP 403 状态。

### Requirement: Chat session operation isolation
系统 SHALL 将每个聊天会话管理操作的作用域限定为已认证的 user 的 tenant 作用域。

#### Scenario: Chat list is scoped
- **WHEN** 一个 user 列出聊天会话
- **THEN** 后端 MUST 仅返回属于该 user 的 tenant 范围内的会话

#### Scenario: Chat history is scoped
- **WHEN** 读取、追加到、清除或删除一个聊天会话
- **THEN** 后端 MUST 将当前 user 的 tenant 范围应用到仓库操作。

#### Scenario: Cross-tenant chat mutation is forbidden
- **WHEN** 一个已认证的 user 尝试读取、追加到、清空或删除另一个 user 的聊天会话
- **THEN** 后端 MUST 返回统一的授权错误，并且 MUST NOT 不修改其他 user 的聊天数据。
