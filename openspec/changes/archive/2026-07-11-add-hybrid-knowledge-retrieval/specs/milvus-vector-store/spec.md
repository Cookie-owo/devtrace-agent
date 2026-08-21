## ADDED Requirements

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
