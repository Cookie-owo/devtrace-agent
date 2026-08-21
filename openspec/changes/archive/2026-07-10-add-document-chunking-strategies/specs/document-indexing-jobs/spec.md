## ADDED Requirements

### Requirement: Strategy-aware document indexing
异步索引服务 SHALL 读取每个文档的持久化 chunking 配置，并在嵌入和 Milvus 插入之前使用共享的 chunking 服务。

#### Scenario: Index task uses document strategy
- **WHEN** 一个索引任务针对具有存储的 chunk 配置的文档运行
- **THEN** 服务 MUST 从该配置生成的 chunk 中生成向量，而不是使用全局固定的策略。

#### Scenario: Vector metadata records chunking strategy
- **WHEN** 服务将 chunk 向量插入到 Milvus
- **THEN** 每个 chunk 元数据记录 MUST 包括所选的 chunking 策略和参数，以及现有的 owner 和 tenant 元数据。
