# milvus-vector-store Specification

## Purpose

为知识库文档定义后端 Milvus 向量存储功能
chunk，包括集合模式、索引/搜索设置、显式连接
生命周期、health 检查以及 tenant 感知的插入/搜索边界。

## Requirements

### Requirement: Milvus chunk collection schema
后端 SHALL 为知识库文档 chunks 定义了一个 Milvus 集合模式，包括 chunk id、文档 id、知识库 id、owner user id、tenant id、内容、向量、元数据、来源和 created_at 字段。

#### Scenario: Schema exposes required chunk fields
- **WHEN** 该 Milvus 集合的模式已构建
- **THEN** 它 MUST 包含 `chunkId`、`documentId`、`knowledgeBaseId`、`ownerUserId`、`tenantId`、`content`、`source` 和 `createdAt` 的标量字段，一个 JSON 字段用于 `metadata`，以及一个 FLOAT_VECTOR 字段用于 `vector`。

#### Scenario: Schema uses configured vector dimension
- **WHEN** 向量存储设置提供嵌入维度
- **THEN** 的模式 MUST 创建 `vector` 字段，并使用该精确维度。

### Requirement: Milvus vector index settings
后端 SHALL 为 chunk 集合定义可配置的向量索引和搜索设置，包括向量维度、索引类型、距离度量和查询参数。

#### Scenario: Default vector settings are available
- **WHEN** 向量存储设置已加载，未被覆盖
- **THEN** 后端 MUST 使用默认的集合名称、1024 维度、HNSW 索引类型、COSINE 度量类型以及显式的 HNSW 搜索参数。

#### Scenario: Index initialization uses configured settings
- **WHEN** 集合已初始化
- **THEN** 后端 MUST 使用配置的索引类型、度量类型和索引参数创建向量索引。

### Requirement: Explicit Milvus connection lifecycle
后端 SHALL 提供显式的 Milvus 连接管理，并在模块导入期间 MUST NOT 连接到 Milvus。

#### Scenario: Importing vector modules has no network side effects
- **WHEN** 后端向量存储模块已导入
- **THEN** 不应构建 Milvus 客户端 MUST，也不应尝试建立连接 MUST。

#### Scenario: 显式创建连接
- **WHEN** 应用程序启动或配置检查显式创建向量存储连接
- **THEN** 后端 MUST 使用配置的 URI 和超时值构建 Milvus 客户端。

### Requirement: Milvus collection initialization
后端 SHALL 提供一个显式的初始化流程，该流程会创建 chunk 集合、标量索引、向量索引，并在需要时加载集合。

#### Scenario: 缺失的集合被创建
- **WHEN** 初始化运行，且 chunk 集合不存在
- **THEN** 后端 MUST 使用配置的模式和索引将其创建。

#### Scenario: Existing collection is reused
- **WHEN** 初始化运行，并且 chunk 集合已经存在
- **THEN** 后端 MUST 会复用它，并仍然确保应用了所需的索引和加载状态。

### Requirement: Milvus health check
后端 SHALL 暴露一个适用于 readiness 和配置验证的 Milvus health 检查。

#### Scenario: 健康的 Milvus 返回就绪状态
- **WHEN** 的 Milvus 客户端可以成功列出或描述集合
- **THEN** 的 health 检查 MUST 返回一个 health 的结果，其中包含目标集合名称。

#### Scenario: 未health的 Milvus 返回诊断详细信息
- **WHEN** 的 Milvus 客户端无法访问或返回错误
- **THEN** 的 health 检查 MUST 返回一个未health的结果，并带有简明的错误消息，而不是泄露传输内部信息。

### Requirement: Tenant-aware chunk records
后端 SHALL 要求在每次将记录插入 Milvus 以及对 Milvus 执行每次检索搜索时，都需提供 tenant ownership 元数据。

#### Scenario: Chunk insert includes ownership fields
- **WHEN** chunk 记录通过文档索引准备插入
- **THEN** 每条记录 MUST 均包含 `ownerUserId`、`tenantId`、`knowledgeBaseId`、`documentId` 和 `chunkId`，既作为标量字段，也作为检索使用的元数据契约。

#### Scenario: Retrieval applies tenant filter
- **WHEN** 对可访问的知识库执行向量搜索
- **THEN** 搜索 MUST 包含一个作用域为当前 tenant 和允许的知识库 ID 的 Milvus 过滤表达式。

#### Scenario: 检索返回结构化的搜索结果
- **WHEN** 检索工具搜索 Milvus
- **THEN** 向量存储 MUST 返回 chunk id、文档 id、知识库 id、owner user id、tenant id、内容、来源、创建时间戳、元数据和每个匹配结果的得分。

#### Scenario: Empty accessible knowledge base list skips Milvus search
- **WHEN** 授权过滤后检索请求没有可访问的知识库
- **THEN** 向量存储边界 MUST 在未发出无范围搜索的情况下返回空结果。

### Requirement: Tenant-scoped chunk enumeration
后端 Milvus 向量存储 SHALL 提供显式的 tenant 范围 chunk 列举边界，为内存关键词检索提供语料，并 MUST NOT 暴露无权限 chunk。

#### Scenario: 列举应用 tenant 和知识库过滤
- **WHEN** 检索工具列举当前 user 可访问的知识库 chunks
- **THEN** Milvus query MUST 包含当前 tenant ID 和允许知识库 ID 的过滤表达式。

#### Scenario: 列举分批读取标量字段
- **WHEN** tenant 范围内存在多个 chunks
- **THEN** 向量存储 MUST 使用 iterator 分批读取检索所需的标量字段，并 MUST NOT 为 BM25 读取 vector 字段。

#### Scenario: 空知识库范围跳过列举
- **WHEN** 授权过滤后没有可访问的知识库 ID
- **THEN** 向量存储 MUST 返回空列表，并 MUST NOT 发出无范围 Milvus query。

#### Scenario: 列举返回结构化 chunk
- **WHEN** Milvus 返回 tenant 范围内的实体
- **THEN** 向量存储 MUST 返回 chunk id、文档 id、知识库 id、owner user id、tenant id、内容、来源、创建时间戳和元数据。

### Requirement: 由 Compose 提供的 Milvus 运行时
后端 Milvus 向量存储 SHALL 将 Docker Compose Milvus 服务视为其本地运行时依赖项，并 SHALL NOT 从应用程序代码中启动 Milvus。

#### Scenario: Local settings target compose service
- **WHEN** 后端项目配置文件被检查
- **THEN** 它们 MUST 包含与 Compose 管理的 Milvus 服务兼容的 Milvus URI 和集合设置。

#### Scenario: Vector settings come from project config
- **WHEN** 后端向量存储配置已构建
- **THEN** 它从跟踪的项目配置文件中读取 MUST、collection、dimension、index、metric 和 search 设置，并从本地机器环境变量中 MUST NOT 读取。

#### Scenario: Application code does not launch Milvus
- **WHEN** 向量存储代码已检查
- **THEN** 它 MUST NOT 调用 Docker 的 shell，启动 Milvus 进程，或依赖 bat 或 sh 启动脚本。

### Requirement: Document-scoped vector deletion
后端 Milvus 向量存储 SHALL 提供一个文档范围的删除操作，用于删除当前 tenant 和知识库中属于某个文档的所有 chunk 向量。

#### Scenario: Document delete uses tenant filter
- **WHEN** 清理文档删除请求向量
- **THEN** 向向量存储 MUST 调用 Milvus 删除操作，并使用包含当前 tenant ID、知识库 ID 和文档 ID 的过滤器。

#### Scenario: Missing document id is not deleted globally
- **WHEN** 调用者提供空的文档 ID、tenant ID 或知识库 ID 用于向量删除
- **THEN** 向量存储 MUST 在调用 Milvus 之前拒绝该操作

### Requirement: Document indexing batch insert
后端 Milvus 向量存储 SHALL 支持在一个显式操作中插入文档索引任务生成的所有 chunk。

#### Scenario: Index task inserts chunk batch
- **WHEN** 一个文档索引任务生成 chunk 向量
- **THEN** 向量存储 MUST 接收一批包含 chunk 记录的 chunk id、文档 id、知识库 id、owner user id、tenant id、内容、向量、元数据、来源和创建时间戳的记录。

#### Scenario: Index task rejects dimension mismatch
- **WHEN** 索引的 chunk 向量与配置的向量维度不匹配
- **THEN** 向量存储 MUST 在写入无效数据之前会拒绝插入
