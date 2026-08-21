## ADDED Requirements

### Requirement: SQLite memory schema
后端 SHALL 使用 SQLAlchemy ORM 模型定义基于 SQLite 的内存模式，用于聊天会话、聊天消息、AIOps 诊断任务、诊断报告、工具调用审计条目以及 AIOps LangGraph checkpoints。

#### Scenario: Memory models expose required tables
- **WHEN** 检查后端内存元数据
- **THEN** 它 MUST 包含用于聊天会话、聊天消息、诊断任务、诊断报告、工具调用审计条目和图 checkpoint 的表。

#### Scenario: Memory records preserve structured payloads
- **WHEN** 消息、报告、工具审计或 checkpoint 包含结构化的元数据或负载
- **THEN** 的模式 MUST 会持久化并以结构化数据而非损失性文本块的形式返回这些负载。

### Requirement: Alembic-managed memory migrations
后端 SHALL 通过 Alembic 迁移来管理内存数据库模式更改。

#### Scenario: Fresh SQLite database is migrated
- **WHEN** Alembic 将一个全新的 SQLite 数据库升级到最新版本
- **THEN** 所有内存表和索引都已存在，这些表和索引是仓库实现 MUST 所需要的。

#### Scenario: Application schema creation uses migrations
- **WHEN** 开发人员需要初始化内存数据库
- **THEN** 记录的命令 MUST 应使用 Alembic 迁移命令，而不是生产应用程序代码调用元数据 `create_all()`。

### Requirement: Repository abstraction boundary
后端 SHALL 暴露仓库协议和数据类记录，以便业务代码可以访问内存数据，而无需依赖 SQLite 表、SQLAlchemy ORM 模型或 SQL 语句。

#### Scenario: Business code depends on repository interfaces
- **WHEN** 应用程序服务需要内存持久化
- **THEN** 它们 MUST 需要能够依赖于暴露记录和查询参数的仓库协议，而不是 SQLAlchemy 模型类。

#### Scenario: SQLite implementation remains replaceable
- **WHEN** 将引入一个未来的 PostgreSQL 仓库实现
- **THEN** 它必须能够在不更改业务服务方法签名的情况下实现相同的仓库协议。

### Requirement: Chat memory repositories
后端 SHALL 为创建聊天会话、追加聊天消息和查询消息历史提供仓库操作。

#### Scenario: Chat history can be queried by session
- **WHEN** 一个聊天会话包含多个持久化的消息
- **THEN** 仓库 MUST 在通过会话 ID 查询时会按创建顺序返回会话的消息。

#### Scenario: Chat history can be queried by time range
- **WHEN** 在请求的时间范围内外都存在消息
- **THEN** 仓库 MUST 仅返回创建时间戳在请求范围内的消息

### Requirement: AIOps diagnostic memory repositories
后端 SHALL 为诊断任务、诊断报告、工具调用审计条目和 LangGraph checkpoint 提供仓库操作。

#### Scenario: Diagnostic artifacts can be queried by task
- **WHEN** 诊断任务包含报告、工具审核条目和 checkpoints
- **THEN** 仓库 MUST 在通过诊断任务 ID 查询时返回这些工件。

#### Scenario: Diagnostic tasks can be queried by time range
- **WHEN** 诊断任务存在于请求的时间范围内外
- **THEN** 任务仓库 MUST 仅返回创建时间戳在请求范围内的任务。

#### Scenario: Tool call audit preserves execution metadata
- **WHEN** 一个工具调用审计条目被存储
- **THEN** 仓库 MUST 保留工具名称、状态、参数、结果负载、错误信息和时间戳。

#### Scenario: LangGraph checkpoint preserves thread namespace
- **WHEN** 为 AIOps 诊断图存储一个 checkpoint
- **THEN** 仓库 MUST 保留诊断任务 ID、线程 ID、checkpoint 命名空间、checkpoint ID 和 checkpoint 负载。
