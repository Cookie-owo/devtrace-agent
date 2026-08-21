## MODIFIED Requirements

### Requirement: SQLite memory schema
后端 SHALL 使用 SQLAlchemy ORM 模型定义基于 SQLite 的内存模式，用于知识文档、文档索引任务、聊天会话、聊天消息、AIOps 诊断任务、诊断报告、工具调用审计条目以及 AIOps LangGraph checkpoints。

#### Scenario: Memory models expose required tables
- **WHEN** 检查后端内存元数据
- **THEN** 它 MUST 包含知识文档的表格、文档索引任务、聊天会话、聊天消息、诊断任务、诊断报告、工具调用审计条目和图 checkpoints。

#### Scenario: Memory records preserve structured payloads
- **WHEN** 文档、文档索引任务、消息、报告、工具审计或 checkpoint 包含结构化的元数据或有效负载
- **THEN** 将模式 MUST 持久化并作为结构化数据返回这些有效负载，而不是丢失信息的纯文本二进制大对象。

### Requirement: Tenant-owned memory schema
后端 SHALL 在 user 专属的内存表和索引范围内保留 owner 范围，并使用通用查找维度。

#### Scenario: Memory tables include owner scope
- **WHEN** Alembic 将一个全新的 SQLite 数据库升级到最新版本
- **THEN** 知识文档、文档索引任务、聊天会话、聊天消息、AIOps 诊断任务、诊断报告、工具调用审计条目以及图 checkpoints MUST 包含一个 owner user ID 列。

#### Scenario: Scoped indexes exist
- **WHEN** 检查迁移后的模式
- **THEN** 它 MUST 应包含支持通过 owner user ID 和时间或父 ID 对知识文档、文档索引任务、聊天和 AIOps 记录进行筛选的索引。

### Requirement: Scoped repository boundary
后端 SHALL 要求仓库调用者为 tenant 作用域的 user-拥有内存操作提供。

#### Scenario: Document operations require owner scope
- **WHEN** 知识文档被创建、查询、标记为已删除、去重或索引状态被更新  
- **THEN** 仓库方法签名 MUST 包含 owner user id 和按其过滤的查询 MUST

#### Scenario: Document index task operations require owner scope
- **WHEN** 文档索引任务被创建、查询、转换、失败、完成或重试
- **THEN** 仓库方法签名 MUST 包含 owner user id 和查询 MUST 通过它进行过滤

#### Scenario: Chat operations require owner scope
- **WHEN** 聊天会话或消息已创建或查询
- **THEN** 仓库方法签名 MUST 包含 owner user id 和查询 MUST 通过它进行过滤。

#### Scenario: AIOps operations require owner scope
- **WHEN** 诊断任务、报告、工具审计或 checkpoint 实例被创建或查询  
- **THEN** 存储库方法签名 MUST 包含 owner user ID 并查询 MUST 按其进行过滤

## ADDED Requirements

### Requirement: Document index task repository
后端 SHALL 暴露了创建文档索引任务、读取任务状态、列出文档的任务、转换为运行中、标记成功、用原因标记失败以及创建重试尝试的仓库操作。

#### Scenario: 可以创建索引任务
- **WHEN** 通过授权的文档索引请求
- **THEN** 仓库 MUST 持久化 owner user 的 id、知识库 id、文档 id、任务 id、状态、时间戳、可选的失败原因和可选的重试源。

#### Scenario: Index task can be read by owner scope
- **WHEN** 调用者读取具有 owner user ID 和任务 ID 的索引任务
- **THEN** 仓库 MUST 仅在任务属于该 owner 时才返回任务

#### Scenario: Index task failure reason is persisted
- **WHEN** 索引失败
- **THEN** 仓库 MUST 与失败任务一起保留一个安全的失败原因。

#### Scenario: Retry task links prior attempt
- **WHEN** 一个失败的索引任务将被重试  
- **THEN** 仓库 MUST 创建一个与同一 owner 范围内的前一个任务 ID 关联的新任务
