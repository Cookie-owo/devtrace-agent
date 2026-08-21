## MODIFIED Requirements

### Requirement: Milvus vector insertion
系统 SHALL 在确保目标集合和索引存在后，通过向量存储边界将 chunks、元数据和向量写入 Milvus。

#### Scenario: Vector store is initialized before writes
- **WHEN** 对于文档索引任务，嵌入生成成功
- **THEN** 索引器 MUST 在删除现有的 chunk 或插入新的 chunk 之前，初始化向量存储集合和索引。

#### Scenario: Chunks are inserted with vectors
- **WHEN** 嵌入生成成功
- **THEN** 索引器 MUST 将所有 chunk 记录插入到 Milvus 中，包含 chunk 内容、向量、来源、创建时间戳和元数据。

#### Scenario: Milvus insertion failure is recorded
- **WHEN** Milvus 插入失败
- **THEN** 任务 MUST 应使用安全的失败原因标记 `failed`，并且文档索引状态 MUST 应标记 `failed`。
