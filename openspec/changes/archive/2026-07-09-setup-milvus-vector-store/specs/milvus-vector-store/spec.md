## ADDED Requirements

### Requirement: Milvus chunk collection schema
后端 SHALL 为知识库文档 chunk 定义一个 Milvus 集合模式，包括 chunk id、文档 id、知识库 id、owner user id、tenant id、内容、向量、元数据、来源和 created_at 字段。

#### Scenario: Schema exposes required chunk fields
- **WHEN** 该 Milvus 集合的模式已构建
- **THEN** 它 MUST 包含 `chunkId`、`documentId`、`knowledgeBaseId`、`ownerUserId`、`tenantId`、`content`、`source` 和 `createdAt` 的标量字段，一个 JSON 字段用于 `metadata`，以及一个 FLOAT_VECTOR 字段用于 `vector`。

#### Scenario: Schema uses configured vector dimension
- **WHEN** 向量存储设置提供嵌入维度
- **THEN** 的模式 MUST 会使用该精确维度创建 `vector` 字段

### Requirement: Milvus vector index settings
后端 SHALL 为 chunk 集合定义可配置的向量索引和搜索设置，包括向量维度、索引类型、距离度量和查询参数。

#### Scenario: Default vector settings are available
- **WHEN** 向量存储设置已加载，无覆盖
- **THEN** 后端 MUST 使用默认的集合名称、1024 维度、HNSW 索引类型、COSINE 度量类型和显式的 HNSW 搜索参数。

#### Scenario: Index initialization uses configured settings
- **WHEN** 集合已初始化
- **THEN** 后端 MUST 使用配置的索引类型、度量类型和索引参数创建向量索引。

### Requirement: Explicit Milvus connection lifecycle
后端 SHALL 提供显式的 Milvus 连接管理以及 MUST NOT 在模块导入期间连接到 Milvus。

#### Scenario: Importing vector modules has no network side effects
- **WHEN** 后端向量存储模块已导入
- **THEN** 不应构建 Milvus 客户端，且不应尝试建立连接 MUST。

#### Scenario: 显式创建连接
- **WHEN** 应用程序启动或配置检查显式创建向量存储连接
- **THEN** 后端 MUST 使用配置的 URI 和超时值构建 Milvus 客户端。

### Requirement: Milvus collection initialization
后端 SHALL 提供了一个显式的初始化流程，该流程会创建 chunk 集合、标量索引、向量索引，并在需要时加载集合。

#### Scenario: 缺失的集合被创建
- **WHEN** 初始化运行，且 chunk 集合不存在
- **THEN** 后端 MUST 使用配置的模式和索引创建它。

#### Scenario: Existing collection is reused
- **WHEN** 初始化运行，chunk 集合已经存在
- **THEN** 后端 MUST 会复用它，并仍然确保应用了所需的索引和加载状态。

### Requirement: Milvus health check
后端 SHALL 暴露一个适用于 readiness 和配置验证的 Milvus health 检查。

#### Scenario: 健康的 Milvus 返回就绪状态
- **WHEN** 的 Milvus 客户端可以成功列出或描述集合
- **THEN** 的 health 检查 MUST 返回一个 health 的结果，其中包含目标集合名称。

#### Scenario: 未health的 Milvus 返回诊断详细信息
- **WHEN** 的 Milvus 客户端无法到达或返回错误
- **THEN** 的 health 检查 MUST 返回一个未health的结果，并带有简明的错误消息，而不是泄露传输内部信息。

### Requirement: Tenant-aware chunk records
后端 SHALL 要求在每个 chunk 记录插入到 Milvus 时都包含 tenant ownership 元数据。

#### Scenario: Chunk insert includes ownership fields
- **WHEN** chunk 记录已准备插入
- **THEN** 每条记录 MUST 均包含 `ownerUserId`、`tenantId`、`knowledgeBaseId`、`documentId` 和 `chunkId`，既作为标量字段，也包含在检索使用的元数据契约中。

#### Scenario: Retrieval applies tenant filter
- **WHEN** 对可访问的知识库执行向量搜索
- **THEN** 搜索 MUST 包含一个作用于当前 tenant 和允许的知识库 ID 的 Milvus 过滤表达式。

### Requirement: ### 需求：由 Compose 提供的 Milvus 运行时
后端 Milvus 向量存储 SHALL 将 Docker Compose Milvus 服务视为其本地运行时依赖项，并 SHALL NOT 从应用程序代码中启动 Milvus 。

#### Scenario: Local settings target compose service
- **WHEN** 后端环境示例正在被检查
- **THEN** 它们 MUST 包含与 Compose 管理的 Milvus 服务兼容的 Milvus URI 和集合设置。

#### Scenario: Application code does not launch Milvus
- **WHEN** 向量存储代码被检查
- **THEN** 它 MUST NOT shell 调用 Docker，启动 Milvus 进程，或依赖 bat 或 sh 启动脚本。
