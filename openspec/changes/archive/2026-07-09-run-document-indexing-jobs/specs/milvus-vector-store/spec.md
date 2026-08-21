## MODIFIED Requirements

### Requirement: Tenant-aware chunk records
后端 SHALL 要求在每次向 Milvus 插入记录时都需提供 tenant ownership 元数据。

#### Scenario: Chunk insert includes ownership fields
- **WHEN** chunk 记录通过文档索引准备插入
- **THEN** 每条记录 MUST 均包含 `ownerUserId`、`tenantId`、`knowledgeBaseId`、`documentId` 和 `chunkId`，既作为标量字段，也作为检索使用的元数据契约。

#### Scenario: Retrieval applies tenant filter
- **WHEN** 对可访问的知识库执行向量搜索
- **THEN** 搜索 MUST 包含一个作用于当前 tenant 和允许的知识库 ID 的 Milvus 过滤表达式。

## ADDED Requirements

### Requirement: Document indexing batch insert
后端 Milvus 向量存储 SHALL 支持在一个显式操作中插入文档索引任务生成的所有 chunk。

#### Scenario: Index task inserts chunk batch
- **WHEN** 文档索引任务生成 chunk 向量
- **THEN** 向量存储 MUST 接收一批 chunk 记录，包含 chunk id、文档 id、知识库 id、owner user id、tenant id、内容、向量、元数据、来源和创建时间戳。

#### Scenario: Index task rejects dimension mismatch
- **WHEN** 索引的 chunk 向量与配置的向量维度不匹配  
- **THEN** 向量存储 MUST 在写入无效数据之前会拒绝插入
