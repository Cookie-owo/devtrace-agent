## 上下文

后端已经具有基于 SQLite 的内存仓库和作用域为 tenant 的帮助程序，用于向量 chunk 元数据和 Milvus 过滤表达式。Docker Compose 已经可以独立启动带有 etcd、MinIO 和 Attu 的服务，并向后端服务暴露 `MILVUS_URI`。缺少的是应用端的向量存储边界，该边界定义了 Milvus 集合，显式地对其进行初始化，并通过 tenant 元数据保持检索范围。

Milvus 在集合中存储向量嵌入和标量字段。租户过滤器必须使用索引的标量字段，而不是仅依赖于自由格式的 JSON 元数据，而 JSON 元数据对于非过滤的扩展数据仍然有用。

## Goals / Non-Goals

**目标：**
- 添加一个后端 `super_ai.vector_store` 包，包含配置、集合模式、连接管理器和仓库风格的 Milvus 向量存储抽象。
- 定义一个知识 chunk 集合，包含 chunk/文档/源内容字段，tenant owner 之间的关系字段，向量字段，JSON 元数据，以及创建时间戳。
- 使用显式初始化来连接到 Milvus，创建集合，创建索引，并加载集合。
- 提供 health 和 readiness 检查，这些检查可以由应用程序启动或配置检查调用。
- 保持导入时的行为无副作用。

**非目标：**
- 不实现文档解析、chunk处理、嵌入生成或自动文档上传。
- 不替换SQLite内存仓库。
- 不从 Python 启动Milvus；启动仍由`infra/compose.yaml`负责。
- 不在现有的已认证-user tenant范围内实现组织级tenant建模。

## 决策

1. **使用专用的向量存储包，而不是将Milvus混入内存仓库中。**
   SQLite 内存层负责聊天、AIOps、认证和审计持久化。Milvus 负责相似性搜索。将`super_ai.vector_store` 保持独立可以保留更换Milvus 或存储后端的能力，而无需更改内存仓库契约。

2. **使用标量 owner 字段以及 JSON 元数据。**
   该集合包括标量 `ownerUserId`、`tenantId`、`knowledgeBaseId`、`documentId` 和 `chunkId` 字段，以便访问过滤器可以针对稳定字段进行筛选。`metadata` JSON 字段存储可扩展的每个 chunk 属性，但不是授权数据的唯一来源。

3. **默认使用 1024 维的 FLOAT_VECTOR 嵌入。**
   配置的默认值与配置的 Qwen `text-embedding-v4` 嵌入模型相匹配。该维度仍可配置，以便在未来引入新的嵌入模型时无需重写模块。

4. **默认使用 COSINE + HNSW 并带显式搜索参数。**
   COSINE 适用于归一化文本嵌入，HNSW 是一个广泛支持的 ANN 索引，用于低延迟检索。索引类型、度量类型和搜索参数仍可配置。

5. **使所有 Milvus 客户端访问显式且可注入。**
   导入该包仅定义数据类和函数。运行时代码必须调用 `connect()`、`initialize()`、`health_check()` 或仓库方法。测试可以注入一个假客户端而无需运行 Milvus 实例。

## Risks / Trade-offs

- [风险] Embedding 模型维度可能会发生变化。 -> 缓解措施：在 `MilvusVectorStoreSettings` 中存储维度，并从设置中推导出模式/索引设置。
- [风险] 如果未对授权字段建立索引，租户过滤可能会变慢。 -> 缓解措施：在初始化期间为 tenant、知识库、文档、owner 和时间戳字段创建标量索引。
- [风险] Compose 服务启动时 Milvus 可能暂时不可用。 -> 缓解措施：health 检查返回结构化的未healthy 结果，而不是引发通用的启动错误。
- [风险] PyMilvus API 在主要版本之间会发生变化。 -> 缓解措施：将客户端使用封装在一个小适配器中，并通过假客户端测试覆盖这些调用。

## 迁移计划

1. 添加 Milvus 客户端依赖和向量存储包。
2. 为 Milvus URI、集合、向量维度、索引类型、度量类型和搜索参数添加设置和环境示例值。
3. 添加用于模式、初始化调用、health 检查、tenant 过滤器和导入时连接安全性的测试。
4. 将后端应用程序连接到以暴露 Milvus readiness，而不会阻塞模块导入。
5. 通过禁用启动初始化并保留现有的 SQLite 支持功能进行回滚。

## 开放问题

此更改无需内容。未来的摄入和检索工具将决定批处理策略、嵌入生成和重新排序集成。
