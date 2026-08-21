## MODIFIED Requirements

### Requirement: User-owned data isolation
系统 SHALL 按 tenant 范围隔离知识库文档、文档索引任务、向量 chunks、聊天会话、聊天消息、工具调用审计、AIOps 诊断任务、证据、报告和图 checkpoints。

#### Scenario: User lists owned data
- **WHEN** 一个 user 列表包含受保护的数据
- **THEN** 系统 MUST 仅返回属于该 user 的 tenant 范围内的记录

#### Scenario: User accesses another tenant resource
- **WHEN** 一个经过身份验证的 user 请求另一个 tenant 拥有的资源 ID  
- **THEN** 系统 MUST 以统一的授权错误拒绝该请求。

#### Scenario: User manages owned documents
- **WHEN** 上传、列出、读取、删除或索引知识文档
- **THEN** 每个仓库和向量操作 MUST 必须作用于当前 user 的 tenant 范围内。

### Requirement: Scoped vector metadata
系统 SHALL 在向量 chunk 元数据中包含 owner、user 和 tenant 信息，用于 Milvus 索引和检索。

#### Scenario: 创建块元数据
- **WHEN** 一份文档 chunk 被准备用于向量索引
- **THEN** 其元数据 MUST 包括 `ownerUserId`、`tenantId`、`knowledgeBaseId`、`documentId` 和 `chunkId`。

#### Scenario: Retrieval applies tenant filter
- **WHEN** 是一个检索工具，用于搜索向量 chunks
- **THEN** 它会根据当前 tenant 的作用域进行过滤，并且只包含 user 可以访问的知识库。
