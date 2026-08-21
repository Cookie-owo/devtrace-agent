## MODIFIED Requirements

### Requirement: Scoped vector metadata
系统 SHALL 在向量 chunk 元数据中包含 owner、user 和 tenant 信息，用于 Milvus 索引和检索。

#### Scenario: 创建块元数据
- **WHEN** 一个文档 chunk 被准备用于向量索引
- **THEN** 其元数据 MUST 包括 `ownerUserId`、`tenantId`、`knowledgeBaseId`、`documentId` 和 `chunkId`。

#### Scenario: Retrieval applies tenant filter
- **WHEN** 是一个检索工具，用于搜索向量 chunks
- **THEN** 它会根据当前 tenant 的作用域进行过滤，并且只包含 user 可以访问的知识库。

#### Scenario: Retrieval rejects unauthorized filters
- **WHEN** 检索工具调用请求了一个超出当前 user 的 tenant 范围的知识库
- **THEN** 系统 MUST 以统一的授权错误拒绝该调用，并 MUST NOT 搜索 Milvus。

#### Scenario: Retrieval omits inaccessible data
- **WHEN** 检索工具调用成功完成
- **THEN** 每个返回的命中结果和引用来源 MUST 都属于当前 tenant 范围内且可访问的知识库。
