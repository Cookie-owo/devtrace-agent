## ADDED Requirements

### Requirement: Manual document index task creation
系统 SHALL 允许经过身份验证的 user 为其拥有的文档手动创建文档索引任务。

#### Scenario: User starts indexing own document
- **WHEN** 已认证的 user 请求在其自己的知识库中对文档进行索引
- **THEN** 系统 MUST 创建一个持久化的索引任务，状态为 `pending` 或 `running`，并通过统一的成功封装返回，状态码为 HTTP 202。

#### Scenario: 用户开始索引另一个 user 的文档
- **WHEN** 一个经过身份验证的 user 请求索引其 tenant 范围外的文档
- **THEN** 系统 MUST 拒绝该请求，并返回统一的授权错误，MUST NOT 创建一个索引任务。

### Requirement: Non-blocking indexing execution
系统 SHALL 在不阻塞后端 API 响应周期的情况下执行文档索引。

#### Scenario: 索引任务请求在处理完成前返回
- **WHEN** 一个 user 创建一个文档索引任务
- **THEN** 的 API MUST 保存任务并返回 HTTP 202，而在 chunking、嵌入或 Milvus 插入完成之前。

#### Scenario: Backend remains able to serve other requests
- **WHEN** 一个索引任务正在运行  
- **THEN** 后端 MUST 在不等待该任务完成的情况下继续独立处理 API 请求。

### Requirement: Document chunking
系统 SHALL 在嵌入之前将可索引的文档文本拆分为确定性的 chunk。

#### Scenario: Document text is split into chunks
- **WHEN** 一个索引任务针对包含可索引文本的文档运行
- **THEN** 索引器 MUST 使用一个或多个 chunk 创建具有稳定 chunk ID、按 chunk 排序的索引、内容文本以及包含 chunk 边界或排序的元数据。

#### Scenario: Empty document text fails indexing
- **WHEN** 一个索引任务针对没有可索引文本的文档运行  
- **THEN** 该任务 MUST 应使用安全失败原因标记，并且文档索引状态 MUST 应被标记 `failed`。

### Requirement: Embedding generation
系统 SHALL 调用配置的 OpenAI-compatible 嵌入模型，为每个 chunk 生成一个向量。

#### Scenario: Embeddings are generated for chunks
- **WHEN** 索引器已创建文档 chunks
- **THEN** 它 MUST 使用 chunk 的内容调用嵌入服务提供者，并在写入 Milvus 之前为每个 chunk 接收一个向量。

#### Scenario: Embedding failure is recorded
- **WHEN** 嵌入提供者失败  
- **THEN** 任务 MUST 必须使用安全的失败原因标记 `failed`，并且 MUST 必须可用于手动重试。

### Requirement: Milvus vector insertion
系统通过向量存储边界将 SHALL 写入 Milvus、元数据和向量。

#### Scenario: Chunks are inserted with vectors
- **WHEN** 嵌入生成成功
- **THEN** 索引器 MUST 将所有 chunk 记录插入到 Milvus 中，包含 chunk 内容、向量、来源、创建时间戳和元数据。

#### Scenario: Milvus insertion failure is recorded
- **WHEN** Milvus 插入失败
- **THEN** 该任务 MUST 应使用安全的失败原因标记 `failed`，并且文档索引状态 MUST 应标记为 `failed`。

### Requirement: Index task state persistence
系统 SHALL 会保留 `pending`、`running`、`succeeded` 和 `failed` 的索引任务状态转换。

#### Scenario: Successful indexing updates task and document
- **WHEN** 生成、嵌入和 Milvus 插入全部成功
- **THEN** 任务 MUST 被标记为 `succeeded`，文档索引状态 MUST 被标记为 `indexed`，完成时间戳 MUST 被保存。

#### Scenario: Failed indexing updates task and document
- **WHEN** 任何索引步骤失败
- **THEN** 任务 MUST 应标记为 `failed`，文档索引状态 MUST 应标记为 `failed`，并且应持久化一个安全的失败原因 MUST。

### Requirement: Manual retry
系统 SHALL 允许一个 user 手动重试失败的文档索引任务，通过为同一受控文档创建新的尝试。

#### Scenario: Failed task is retried
- **WHEN** 已认证的 user 重新尝试对具有失败任务的文档进行索引
- **THEN** 系统 MUST 创建一个与之前失败任务相关联的新索引任务并安排其进行处理

#### Scenario: Retry is tenant scoped
- **WHEN** 已认证的 user 尝试在其 tenant 范围外重试任务
- **THEN** 系统 MUST 以统一的授权错误拒绝该请求。
