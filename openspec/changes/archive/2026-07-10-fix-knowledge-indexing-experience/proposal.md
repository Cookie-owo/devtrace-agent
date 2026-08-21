## Why

知识文档上传在前端显示为 `pending`，因为上传仅创建了元数据，并未启动索引任务。本地索引也暴露了运行时的缺陷：Qwen `text-embedding-v4` 拒绝了 LangChain 的分词嵌入输入，且当 chunk 集合尚未初始化时，Milvus 写入失败。

## 什么更改

- 在前端成功上传文档后，自动启动文档索引任务。
- 在前端等待索引任务达到终端状态的短时间内，将已上传的文档显示为`indexing`，然后刷新文档状态。
- 保留手动 `Index/Reindex` 行为，以供现有或失败的文档使用。
- 使用显式的 1024 维度和原始字符串输入行为来配置 Qwen OpenAI-compatible 嵌入模型。
- 在文档索引删除或插入 chunk 向量之前，初始化 Milvus 集合和索引。
- 将 Compose Milvus 镜像标签与本地可用的 Milvus 独立镜像对齐，用于知识库测试。

## 功能

### 新功能

无。

### 修改的功能

- `knowledge-documents`: 前端上传现在开始进行索引并更新可见的文档状态，而不是将新上传的文件留在`pending`。
- `document-indexing-jobs`：索引执行必须在写入之前初始化向量存储，前端上传可能会自动创建第一个索引任务。
- `qwen-openai-provider`：Embedding 配置必须包含维度并保留 Qwen OpenAI-compatible 嵌入的原始字符串输入。
- `docker-compose-startup`：Milvus Compose 镜像必须是一个可拉取的独立镜像，与本地堆栈兼容。

## 影响

- 后端 LLM 提供商配置和测试。
- 后端文档索引服务和向量存储协议类型定义。
- 前端受保护数据状态、文档操作文本和测试。
- 根项目配置文件和后端文档。
- Docker Compose Milvus 镜像标签和 OpenSpec 规范。
