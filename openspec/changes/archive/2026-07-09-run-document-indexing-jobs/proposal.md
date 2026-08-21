## Why

上传的知识文档当前仅处理元数据和向量删除。用户需要一个显式的、非阻塞的索引路径，chunk 文档内容，对其进行嵌入，并将 tenant 拥有的向量写入 Milvus，同时在不冻结 API 服务的情况下公开可重试的任务状态。

## 什么更改

- 使用 `pending`、`running`、`succeeded` 和 `failed` 状态向 SQLite 中添加文档索引任务。
- 添加一个后端索引服务，该服务 chunk 文档文本，调用配置的 OpenAI-compatible 嵌入模型，并将 chunk 元数据和向量写入 Milvus。
- 为已认证的API添加受保护的API，用于手动触发文档索引/reindexing并读取作业状态。  
- 为已认证的user添加前端控制，以重建文档索引并观察任务/index状态。
- 扩展共享契约，使前端和后端使用相同的索引任务 DTO 和 OpenAPI 路径。
- 通过在每个索引的chunk和作用域仓库/vector操作上要求owner/user/tenant元数据，保留tenant隔离。

## 功能

### 新功能
- `document-indexing-jobs`：定义非阻塞、可重试的文档索引任务，用于chunking、嵌入、Milvus写入以及SQLite任务状态持久化。

### 修改后的功能
- `api-and-sse-contracts`: 添加共享文档索引任务 DTO 和受保护的 OpenAPI 操作以用于触发/状态。
- `knowledge-documents`: 添加显式的手动重新索引行为和文档索引状态更新。
- `memory-repositories`: 添加文档索引任务历史记录和重试状态的存储库契约和 SQLite 架构。
- `milvus-vector-store`: 为文档索引添加批量块插入预期。
- `authorization-and-tenant-isolation`: 要求文档索引和向量写入保持在当前用户租户范围内。

## 影响

- 后端：FastAPI 文档端点，文档索引服务，嵌入提供者，内存仓库协议/SQLite 实现，Alembic 迁移，Milvus 向量存储边界。
- 前端：文档列表状态/client 和已认证的工作区控件，用于重新构建索引。
- 合同：`packages/api-contracts` DTOs/OpenAPI 用于索引任务创建和状态。
- 运行时：索引作为后台任务安排；它不会在应用程序启动时开始，也不会阻塞请求处理。
