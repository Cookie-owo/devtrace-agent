## ADDED Requirements

### Requirement: Document-scoped vector deletion
后端 Milvus 向量存储 SHALL 提供一个文档范围的删除操作，用于删除当前 tenant 和知识库中属于某文档的所有 chunk 向量。

#### Scenario: Document delete uses tenant filter
- **WHEN** 清理文档删除请求向量
- **THEN** 向量存储 MUST 调用 Milvus 删除操作，并包含当前 tenant ID、知识库 ID 和文档 ID 的过滤条件。

#### Scenario: Missing document id is not deleted globally
- **WHEN** 调用者提供空的文档 id、tenant id 或知识库 id 进行向量删除
- **THEN** 向量存储 MUST 在调用 Milvus 之前拒绝该操作
