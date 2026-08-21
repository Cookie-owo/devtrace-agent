# memory-repositories Specification

## Purpose

定义后端内存持久化、SQLAlchemy/Alembic 模式管理以及知识文档、文档索引、聊天、AIOps 诊断、工具审计和 LangGraph checkpoint 数据的仓库合约。
## Requirements
### Requirement: SQLite memory schema
后端 SHALL 使用 SQLAlchemy ORM 模型定义基于 SQLite 的内存模式，用于知识文档、文档索引任务、聊天会话、聊天消息、AIOps 诊断任务、诊断报告、工具调用审计条目以及 AIOps LangGraph checkpoints。

#### Scenario: Memory models expose required tables
- **WHEN** 检查后端内存元数据
- **THEN** 它 MUST 包含知识文档的表格、文档索引任务、聊天会话、聊天消息、诊断任务、诊断报告、工具调用审计条目和图 checkpoint。

#### Scenario: Memory records preserve structured payloads
- **WHEN** 文档、文档索引任务、消息、报告、工具审计或 checkpoint 包含结构化元数据或有效负载
- **THEN** 的模式 MUST 将这些有效负载作为结构化数据保存并返回，而不是丢失的纯文本块。

### Requirement: Alembic-managed memory migrations
后端 SHALL 通过 Alembic 迁移来管理内存数据库模式更改。

#### Scenario: Fresh SQLite database is migrated
- **WHEN** Alembic 将一个全新的 SQLite 数据库升级到最新版本
- **THEN** 所有仓库实现所需的内存表和索引 MUST 都已存在。

#### Scenario: Application schema creation uses migrations
- **WHEN** 开发人员需要初始化内存数据库
- **THEN** 记录的命令 MUST 应使用 Alembic 迁移命令，而不是生产应用程序代码调用元数据 `create_all()`。

### Requirement: Memory database project configuration
后端 SHALL 从跟踪的项目配置文件中加载 SQLite 内存数据库设置。

#### Scenario: Memory database URL comes from project config
- **WHEN** 后端内存数据库配置已构建
- **THEN** 它 MUST 从跟踪的项目配置中读取数据库 URL，并 MUST NOT 读取本地机器环境变量。

#### Scenario: Alembic uses project config for application migrations
- **WHEN** Alembic 在应用程序启动或开发者迁移命令期间运行
- **THEN** 它 MUST 能够从后端应用程序使用的相同跟踪项目配置文件中解析内存数据库 URL 。

### Requirement: Repository abstraction boundary
后端 SHALL 暴露仓库协议和数据类记录，以便业务代码可以访问内存数据，而无需依赖 SQLite 表、SQLAlchemy ORM 模型或 SQL 语句。

#### Scenario: Business code depends on repository interfaces
- **WHEN** 应用程序服务需要内存持久化
- **THEN** 它们 MUST 能够依赖于暴露记录和查询参数的仓库协议，而不是 SQLAlchemy 模型类。

#### Scenario: SQLite implementation remains replaceable
- **WHEN** 将引入一个未来的 PostgreSQL 仓库实现
- **THEN** 它 MUST 能够在不更改业务服务方法签名的情况下实现相同的仓库协议。

### Requirement: Chat memory repositories
后端 SHALL 为创建聊天会话、追加聊天消息和查询消息历史提供仓库操作。

#### Scenario: Chat history can be queried by session
- **WHEN** 一个聊天会话包含多条持久化消息
- **THEN** 当通过会话 ID 查询时，存储库 MUST 应按创建顺序返回会话的消息。

#### Scenario: Chat history can be queried by time range
- **WHEN** 在请求的时间范围内外都存在消息
- **THEN** 仓库 MUST 仅返回创建时间戳在请求范围内的消息

### Requirement: AIOps diagnostic memory repositories
后端 SHALL 为诊断任务、诊断报告、工具调用审核条目和 LangGraph checkpoint 提供仓库操作。

#### Scenario: Diagnostic artifacts can be queried by task
- **WHEN** 诊断任务有报告、工具审计条目和 checkpoints
- **THEN** 仓库 MUST 在通过诊断任务 ID 查询时返回这些工件

#### Scenario: Diagnostic tasks can be queried by time range
- **WHEN** 诊断任务存在于请求的时间范围内外
- **THEN** 任务仓库 MUST 仅返回创建时间戳在请求范围内的任务。

#### Scenario: Tool call audit preserves execution metadata
- **WHEN** 一个工具调用审计条目被存储
- **THEN** 仓库 MUST 保留工具名称、状态、参数、结果负载、错误信息和时间戳。

#### Scenario: LangGraph checkpoint preserves thread namespace
- **WHEN** 为 AIOps 诊断图存储一个 checkpoint
- **THEN** 存储库 MUST 保留诊断任务 ID、线程 ID、checkpoint 命名空间、checkpoint ID 和 checkpoint 负载。

### Requirement: Auth memory schema
后端 SHALL 将内存数据库模式扩展为 user 和可撤销的授权会话。

#### Scenario: User and session tables are migrated
- **WHEN** Alembic 将全新的 SQLite 数据库升级到最新版本
- **THEN** 的内存模式 MUST 包含 `users` 和 `auth_sessions` 表，并为电子邮件和令牌哈希查找建立了索引。

#### Scenario: Plaintext secrets are not stored
- **WHEN** 一个 user 注册或登录
- **THEN** 数据库 MUST 存储密码哈希和令牌哈希，而不是明文密码或明文承载令牌。

### Requirement: Auth repository boundary
后端 SHALL 为 users 和身份验证会话提供仓库操作，而不会将 SQLAlchemy 模型泄露给身份验证服务。

#### Scenario: 用户查找支持电子邮件和ID
- **WHEN** 身份验证服务需要注册或认证一个 user
- **THEN** 仓库 MUST 支持创建 user 并通过规范化的电子邮件或ID查找 user。

#### Scenario: 会话查找支持令牌哈希
- **WHEN** 身份验证依赖项验证承载令牌
- **THEN** 仓库 MUST 通过令牌哈希查找活动会话并拒绝被撤销的会话。

#### Scenario: Session revocation is persisted
- **WHEN** 一个 user 注销
- **THEN** 的仓库 MUST 标记认证会话已撤销，并阻止该令牌的未来验证。

### Requirement: Tenant-owned memory schema
后端 SHALL 在 user 专属的内存表和索引范围内使用通用查找维度进行持久化 owner 范围。

#### Scenario: Memory tables include owner scope
- **WHEN** Alembic 将一个全新的 SQLite 数据库升级到最新版本
- **THEN** 知识文档、文档索引任务、聊天会话、聊天消息、AIOps 诊断任务、诊断报告、工具调用审计条目以及图 checkpoints MUST 包含一个 owner user id 列。

#### Scenario: Scoped indexes exist
- **WHEN** 检查迁移后的模式
- **THEN** 它 MUST 应包含支持通过 owner user ID 和时间或父 ID 对知识文档、文档索引任务、聊天和 AIOps 记录进行筛选的索引。

### Requirement: Scoped repository boundary
后端 SHALL 要求仓库调用者为 tenant 作用域的 user-拥有内存操作提供。

#### Scenario: Document operations require owner scope
- **WHEN** 知识文档被创建、查询、标记为已删除、去重或更新索引状态
- **THEN** 仓库方法签名 MUST 包含 owner user id 并通过它进行查询 MUST 过滤

#### Scenario: Document index task operations require owner scope
- **WHEN** 文档索引任务被创建、查询、转换、失败、完成或重试
- **THEN** 仓库方法签名 MUST 包含 owner user id 并通过它进行查询 MUST 过滤。

#### Scenario: Chat operations require owner scope
- **WHEN** 聊天会话或消息已创建或查询
- **THEN** 仓库方法签名 MUST 包含 owner user id 并通过它进行查询 MUST 。

#### Scenario: AIOps operations require owner scope
- **WHEN** 诊断任务、报告、工具审计或 checkpoint 被创建或查询  
- **THEN** 仓库方法签名 MUST 包含 owner user ID 和按其过滤的查询 MUST

### Requirement: Cross-tenant repository denial
仓库实现 SHALL 不得在提供的 owner 范围之外对父资源进行写入操作。

#### Scenario: 向另一个 user 的聊天会话中追加消息
- **WHEN** 调用者尝试使用一个不拥有该会话的 owner ID 追加聊天消息
- **THEN** 仓库 MUST 应该拒绝该操作，而不是写入消息。

#### Scenario: 将 AIOps 项目添加到另一个 user 的任务中
- **WHEN** 调用者添加报告、工具审核或带有 owner ID 的 checkpoint，该 ID 并不拥有该任务
- **THEN** 仓库 MUST 应拒绝该操作，而不是写入该项目。

### Requirement: Vector ownership contract
后端 SHALL 暴露共享向量元数据和过滤帮助程序，这些帮助程序对 tenant ownership 进行编码，以便未来的 Milvus 索引和检索。

#### Scenario: Vector metadata helper includes ownership
- **WHEN** 向量 chunk 元数据已构建
- **THEN** 它 MUST 包含 owner user ID、tenant ID、知识库 ID、文档 ID 和 chunk ID。

#### Scenario: Vector filter helper scopes retrieval
- **WHEN** 为可访问的知识库构建了检索过滤器
- **THEN** 它 MUST 包括当前 tenant 范围和允许的知识库 ID。

### Requirement: Knowledge document repository
后端 SHALL 暴露了用于创建文档元数据、列出文档、读取文档详情、通过哈希查找重复项以及标记文档已删除的仓库操作。

#### Scenario: 可以创建文档元数据
- **WHEN** 上传文档通过 API 验证
- **THEN** 仓库 MUST 持久化 owner user 的 id、知识库 id、文件名、字节大小、MIME 类型、内容哈希、状态、索引状态、元数据和上传时间戳。

#### Scenario: Documents can be queried by time range
- **WHEN** 在请求的时间范围内外都存在文档
- **THEN** 仓库 MUST 仅返回上传时间戳在请求范围内的文档

#### Scenario: Duplicate hash lookup is scoped
- **WHEN** 执行重复性检查
- **THEN** 通过 owner user ID、知识库 ID 和内容哈希值搜索仓库 MUST，排除已删除的文档。

#### Scenario: Document deletion is scoped
- **WHEN** 调用者标记一个文档为已删除  
- **THEN** 仓库 MUST 仅影响由提供的 owner user ID 拥有的文档。

### Requirement: Document index task repository
后端 SHALL 暴露了创建文档索引任务、读取任务状态、列出文档的任务、转换为运行中、标记成功、用原因标记失败以及创建重试尝试的仓库操作。

#### Scenario: 可以创建索引任务
- **WHEN** 通过授权的文档索引请求
- **THEN** 仓库 MUST 持久化 owner user ID、知识库 ID、文档 ID、任务 ID、状态、时间戳、可选的失败原因以及可选的重试源。

#### Scenario: Index task can be read by owner scope
- **WHEN** 一个调用者读取具有 owner user ID 和任务 ID 的索引任务
- **THEN** 仓库 MUST 仅在任务属于该 owner 时返回任务

#### Scenario: Index task failure reason is persisted
- **WHEN** 索引失败
- **THEN** 仓库 MUST 与失败任务一起保留一个安全的失败原因。

#### Scenario: Retry task links prior attempt
- **WHEN** 一个失败的索引任务将被重试  
- **THEN** 仓库 MUST 在相同的 owner 范围内创建一个与前一个任务 ID 关联的新任务。

### Requirement: Chat session lifecycle repositories
后端 SHALL 在 owner 范围内公开用于更新聊天会话标题、清除聊天消息和删除聊天会话的仓库操作。

#### Scenario: Session title can be updated by owner
- **WHEN** 业务代码使用 owner user ID 和会话 ID 更新聊天会话标题
- **THEN** 仓库 MUST 仅对属于该 user 的会话保存新标题

#### Scenario: Session messages can be cleared by owner
- **WHEN** 业务代码清除具有 owner user ID 和会话 ID 的聊天消息
- **THEN** 仓库 MUST 仅删除属于该 user 会话的消息，并保持会话记录完整。

#### Scenario: Session can be deleted by owner
- **WHEN** 业务代码根据 owner user ID 和会话 ID 删除聊天会话
- **THEN** 仓库 MUST 仅删除该 user 的会话及其消息。

#### Scenario: Cross-tenant lifecycle mutation is denied
- **WHEN** 调用者在提供的 owner 范围之外更新、清除或删除聊天会话
- **THEN** 仓库 MUST 应拒绝或返回无变更，而不是修改其他 user 的数据。

### Requirement: Generic tool call audit repository
后端 SHALL 为创建、完成和查询 tenant 范围的工具调用审计记录提供了一个仓库协议，而不会向业务服务暴露 SQLite 或 SQLAlchemy 的详细信息。

#### Scenario: Chat tool audit can be updated by lifecycle id
- **WHEN** 业务代码创建了一个聊天工具审计记录，之后收到了同一工具调用 ID 的终端事件
- **THEN** 它会 MUST 完成现有的 owner 范围的审计记录，而不是创建重复的记录。

#### Scenario: Diagnostic tool audit can use the common boundary
- **WHEN** 一个未来的 AIOps 诊断流程记录工具调用
- **THEN** 它 MUST 能够通过相同的通用仓库协议，使用其诊断任务 ID 创建和查询记录。

### Requirement: Diagnostic evidence-chain repository boundary
后端 SHALL 暴露存储库记录以及 owner 范围内的诊断步骤、证据、报告证据链接、历史查询和完整证据链查询，而不会泄露 SQLAlchemy 详情。

#### Scenario: Repository writes validate task ownership
- **WHEN** 业务代码存储一个步骤、证据记录或报告证据链接
- **THEN** 仓库 MUST 验证诊断任务是否属于提供的 owner user ID。

#### Scenario: Repository reads complete chain within owner scope
- **WHEN** 业务代码请求一个带有 owner user ID 和任务 ID 的诊断证据链
- **THEN** 仓库 MUST 仅返回属于该 owner 和任务的记录

### Requirement: User chat configuration repository
内存层 SHALL 为读取和更新聊天组装配置提供一个 user 范围的 Repository，而不会将 SQLite 模型或 SQL 详情泄露给业务服务。

#### Scenario: Repository scopes reads and writes by user
- **WHEN** 服务读取或更新聊天配置
- **THEN** 仓库 MUST 需要 owner user ID 并仅返回或修改该 user 的行。

#### Scenario: 迁移创建配置存储
- **WHEN** 初始化或升级内存模式
- **THEN** Alembic MUST 使用唯一的 owner 边界和 JSON 安全的技能选择持久化创建 user 聊天配置存储。

### Requirement: Persisted document chunking configuration
文档仓库 SHALL 会保留并返回经过验证的 chunking 配置作为文档元数据，同时保留现有的 owner 和知识库作用域边界。

#### Scenario: 返回已存储的配置以供拥有文档使用
- **WHEN** 一个经过身份验证的 user 在上传后读取其拥有的文档
- **THEN** 仓库支持的响应 MUST 返回文档的持久化 chunk 配置。
