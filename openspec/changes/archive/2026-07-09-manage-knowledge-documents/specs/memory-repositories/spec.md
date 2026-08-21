## MODIFIED Requirements

### Requirement: SQLite memory schema
后端 SHALL 使用 SQLAlchemy ORM 模型定义基于 SQLite 的内存模式，用于知识文档、聊天会话、聊天消息、AIOps 诊断任务、诊断报告、工具调用审计条目以及 AIOps LangGraph checkpoints。

#### Scenario: Memory models expose required tables
- **WHEN** 检查后端内存元数据
- **THEN** 它 MUST 包含知识文档、聊天会话、聊天消息、诊断任务、诊断报告、工具调用审计条目和图 checkpoint 的表格。

#### Scenario: Memory records preserve structured payloads
- **WHEN** 文档、消息、报告、工具审核或 checkpoint 包含结构化的元数据或有效载荷
- **THEN** 的模式 MUST 会保留并以结构化数据的形式返回这些有效载荷，而不是丢失信息的纯文本块。

### Requirement: Tenant-owned memory schema
后端 SHALL 在 user 专属的内存表和索引范围内保留 owner 范围以及常见的查找维度。

#### Scenario: Memory tables include owner scope
- **WHEN** Alembic 将一个全新的 SQLite 数据库升级到最新版本
- **THEN** 知识文档、聊天会话、聊天消息、AIOps 诊断任务、诊断报告、工具调用审计条目以及图 checkpoints MUST 包含一个 owner user id 列。

#### Scenario: Scoped indexes exist
- **WHEN** 检查迁移后的模式
- **THEN** 它 MUST 应包含支持通过 owner user ID 和时间或父 ID 对知识文档、聊天和 AIOps 记录进行筛选的索引。

### Requirement: Scoped repository boundary
后端 SHALL 要求仓库调用者为 tenant 作用域的 user-拥有内存操作提供。

#### Scenario: Document operations require owner scope
- **WHEN** 知识文档被创建、查询、标记为已删除或去重
- **THEN** 仓库方法签名 MUST 包含 owner user id 和通过它进行过滤的查询 MUST

#### Scenario: Chat operations require owner scope
- **WHEN** 聊天会话或消息已创建或查询
- **THEN** 仓库方法签名 MUST 包含 owner user ID 和查询 MUST 通过它进行过滤。

#### Scenario: AIOps operations require owner scope
- **WHEN** 诊断任务、报告、工具审计或 checkpoint 会被创建或查询  
- **THEN** 仓库方法签名 MUST 包含 owner user ID，并且查询 MUST 会根据该 ID 进行过滤

## ADDED Requirements

### Requirement: Knowledge document repository
后端 SHALL 暴露了创建文档元数据、列出文档、读取文档详情、通过哈希查找重复项以及标记文档为已删除的仓库操作。

#### Scenario: 可以创建文档元数据
- **WHEN** 上传文档通过 API 验证
- **THEN** 仓库 MUST 持久化 owner user 的 ID、知识库 ID、文件名、字节大小、MIME 类型、内容哈希、状态、索引状态、元数据和上传时间戳。

#### Scenario: Documents can be queried by time range
- **WHEN** 在请求的时间范围内外都存在文档
- **THEN** 仓库 MUST 仅返回上传时间戳在请求范围内的文档

#### Scenario: Duplicate hash lookup is scoped
- **WHEN** 进行重复检查
- **THEN** 通过 owner user 的 ID、知识库 ID 和内容哈希值搜索仓库，排除已删除的文档。

#### Scenario: Document deletion is scoped
- **WHEN** 调用者将文档标记为已删除
- **THEN** 仓库 MUST 仅影响由提供的 owner user ID 拥有的文档。
