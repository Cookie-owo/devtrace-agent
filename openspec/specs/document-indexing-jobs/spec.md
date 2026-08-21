# document-indexing-jobs Specification

## Purpose

定义经过身份验证的、tenant 范围的、非阻塞的文档索引任务，这些任务将上传的文档文本chunk，调用配置的嵌入模型，将范围向量写入Milvus，在SQLite中持久化任务状态，并支持手动重试。
## Requirements
### Requirement: Manual document index task creation
系统 SHALL 允许经过身份验证的 user 为其拥有的文档手动创建文档索引任务。

#### Scenario: User starts indexing own document
- **WHEN** 已认证的 user 请求对其知识库中的文档进行索引
- **THEN** 系统 MUST 创建一个持久化的索引任务，状态为 `pending` 或 `running`，并通过统一的成功封装返回，状态码为 HTTP 202。

#### Scenario: 用户开始对另一个 user 的文档进行索引
- **WHEN** 一个经过身份验证的 user 请求对其 tenant 范围外的文档进行索引
- **THEN** 系统 MUST 以统一的授权错误拒绝该请求，并且 MUST NOT 创建一个索引任务。

### Requirement: Non-blocking indexing execution
文档索引 SHALL 作为持久化 `document_index` 后台任务执行，请求 MUST 立即返回，服务重启后 queued 或租约过期的索引 MUST 恢复。

#### Scenario: Indexing task is accepted
- **WHEN** 用户创建或重试文档索引任务
- **THEN** API MUST 同时创建业务索引记录和 durable background job，并返回 202。

### Requirement: Document chunking
系统 SHALL 在嵌入之前将可索引文档文本拆分为确定性 chunk。

#### Scenario: Document text is split into chunks
- **WHEN** 一个索引任务针对包含可索引文本的文档运行
- **THEN** 索引器 MUST 使用一个或多个 chunk 创建具有稳定 chunk ID、按 chunk 排序的索引、内容文本以及包含 chunk 边界或排序的元数据。

#### Scenario: Empty document text fails indexing
- **WHEN** 一个索引任务对没有可索引文本的文档运行  
- **THEN** 该任务 MUST 被标记为 `failed` ，并带有安全失败原因，且文档索引状态 MUST 被标记为 `failed` 。

### Requirement: Embedding generation
系统 SHALL 调用配置的 OpenAI-compatible 嵌入模型，为每个 chunk 生成一个向量。

#### Scenario: Embeddings are generated for chunks
- **WHEN** 索引器已创建文档 chunks
- **THEN** 它 MUST 使用 chunk 内容调用嵌入服务提供商，并在写入 Milvus 之前为每个 chunk 接收一个向量。

#### Scenario: Embedding failure is recorded
- **WHEN** 嵌入提供方失败  
- **THEN** 该任务 MUST 应使用安全的失败原因标记 `failed`，并且 MUST 应可用于手动重试。

### Requirement: Milvus vector insertion
系统在确保目标集合和索引存在后，通过向量存储边界将 SHALL 写入 Milvus、元数据和向量。

#### Scenario: Vector store is initialized before writes
- **WHEN** 为文档索引任务生成嵌入成功
- **THEN** 索引器 MUST 在删除现有的 chunk 或插入新的 chunk 之前，初始化向量存储集合和索引。

#### Scenario: Chunks are inserted with vectors
- **WHEN** 嵌入生成成功
- **THEN** 索引器 MUST 将所有 chunk 记录插入到 Milvus 中，包含 chunk 内容、向量、来源、创建时间戳和元数据。

#### Scenario: Milvus insertion failure is recorded
- **WHEN** Milvus 插入失败
- **THEN** 该任务 MUST 应使用安全的失败原因标记 `failed`，并且文档索引状态 MUST 应标记 `failed`。

### Requirement: Index task state persistence
系统 SHALL 会保留 `pending`、`running`、`succeeded` 和 `failed` 的索引任务状态转换。

#### Scenario: Successful indexing updates task and document
- **WHEN** 生成、嵌入和 Milvus 插入全部成功
- **THEN** 任务必须被标记为 `succeeded`，文档索引状态必须被标记为 `indexed`，完成时间戳必须被持久化。

#### Scenario: Failed indexing updates task and document
- **WHEN** 任何索引步骤失败
- **THEN** 任务 MUST 应被标记为 `failed`，文档索引状态 MUST 应被标记为 `failed`，并且应保存一个安全的失败原因 MUST。

### Requirement: Manual retry
系统 SHALL 允许一个 user 手动重试失败的文档索引任务，通过为同一拥有文档创建新的尝试。

#### Scenario: Failed task is retried
- **WHEN** 一个经过身份验证的 user 会重试具有失败任务的文档的索引
- **THEN** 系统 MUST 会创建一个与之前失败任务相关联的新索引任务并安排其进行处理。

#### Scenario: Retry is tenant scoped
- **WHEN** 已认证的 user 尝试在其 tenant 范围外重试任务
- **THEN** 系统 MUST 以统一的授权错误拒绝该请求。

### Requirement: Strategy-aware document indexing
异步索引服务 SHALL 读取每个文档的持久化 chunking 配置，并在嵌入和 Milvus 插入之前使用共享的 chunking 服务。

#### Scenario: Index task uses document strategy
- **WHEN** 一个索引任务在具有存储的 chunk 配置的文档上运行
- **THEN** 服务 MUST 从该配置生成的 chunk 中生成向量，而不是使用全局固定的策略。

#### Scenario: Vector metadata records chunking strategy
- **WHEN** 服务将 chunk 向量插入到 Milvus 中
- **THEN** 每个 chunk 元数据记录 MUST 包括所选的 chunk 策略和参数，以及现有的 owner 和 tenant 元数据。
