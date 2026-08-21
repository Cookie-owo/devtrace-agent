## MODIFIED Requirements

### Requirement: Tenant-aware chunk records
后端 SHALL 要求在每次将记录插入 Milvus 以及对 Milvus 执行每次检索搜索时，都需提供 tenant ownership 元数据。

#### Scenario: Chunk insert includes ownership fields
- **WHEN** chunk 记录由文档索引准备插入
- **THEN** 每条记录 MUST 都包含 `ownerUserId`、`tenantId`、`knowledgeBaseId`、`documentId` 和 `chunkId`，既作为标量字段，也作为检索使用的元数据契约。

#### Scenario: Retrieval applies tenant filter
- **WHEN** 对可访问的知识库执行向量搜索
- **THEN** 搜索 MUST 包含一个作用于当前 tenant 和允许的知识库 ID 的 Milvus 过滤表达式。

#### Scenario: 检索返回结构化的搜索结果
- **WHEN** 检索工具搜索 Milvus
- **THEN** 向量存储 MUST 返回 chunk id、文档 id、知识库 id、owner user id、tenant id、内容、来源、创建时间戳、元数据和每个匹配结果的得分。

#### Scenario: Empty accessible knowledge base list skips Milvus search
- **WHEN** 授权过滤后检索请求没有可访问的知识库
- **THEN** 向量存储边界 MUST 在不发起非作用域搜索的情况下返回空结果。
