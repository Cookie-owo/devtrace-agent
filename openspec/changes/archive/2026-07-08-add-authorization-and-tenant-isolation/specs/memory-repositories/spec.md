## ADDED Requirements

### Requirement: Tenant-owned memory schema
后端 SHALL 在 user 专属的内存表和索引作用域中保留 owner 作用域以及常见的查找维度。

#### Scenario: Memory tables include owner scope
- **WHEN** Alembic 将一个全新的 SQLite 数据库升级到最新版本
- **THEN** 聊天会话、聊天消息、AIOps 诊断任务、诊断报告、工具调用审计条目以及图 checkpoints MUST 包含一个 owner user ID 列。

#### Scenario: Scoped indexes exist
- **WHEN** 检查迁移后的模式
- **THEN** 它 MUST 应包含支持通过 owner user ID 和时间或父 ID 过滤聊天和 AIOps 记录的索引。

### Requirement: Scoped repository boundary
后端 SHALL 要求仓库调用者为 tenant 范围的 user 专属内存操作提供 tenant 范围。

#### Scenario: Chat operations require owner scope
- **WHEN** 聊天会话或消息已创建或查询
- **THEN** 仓库方法签名 MUST 包含 owner user id 和查询 MUST 通过它进行筛选。

#### Scenario: AIOps operations require owner scope
- **WHEN** 诊断任务、报告、工具审计或 checkpoint 被创建或查询  
- **THEN** 仓库方法签名 MUST 包含 owner user ID 和按其过滤的查询 MUST

### Requirement: Cross-tenant repository denial
仓库实现 SHALL 不得在提供的 owner 范围之外对父资源进行写入。

#### Scenario: 向另一个 user 的聊天会话追加消息
- **WHEN** 调用者尝试使用一个不拥有该会话的 owner ID 追加聊天消息
- **THEN** 仓库 MUST 应该拒绝该操作，而不是写入消息。

#### Scenario: 将 AIOps 项目添加到另一个 user 的任务中
- **WHEN** 调用者添加报告、工具审计或带有不拥有该任务的 owner ID 的 checkpoint
- **THEN** 仓库 MUST 拒绝该操作，而不是写入该项目。

### Requirement: Vector ownership contract
后端 SHALL 暴露共享向量元数据和过滤帮助程序，这些帮助程序对 tenant ownership 进行编码，以便未来 Milvus 的索引和检索。

#### Scenario: Vector metadata helper includes ownership
- **WHEN** 向量 chunk 元数据已构建
- **THEN** 它 MUST 包含 owner user ID、tenant ID、知识库 ID、文档 ID 和 chunk ID。

#### Scenario: Vector filter helper scopes retrieval
- **WHEN** 为可访问的知识库构建了检索过滤器
- **THEN** 它 MUST 包括当前 tenant 范围和允许的知识库 ID。
