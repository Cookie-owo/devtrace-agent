## Context

文档索引服务会把文档拆分后的全部 chunk 一次传给 `EmbeddingModel.aembed_documents`。默认 `OpenAIEmbeddings` 的批量大小大于阿里云百炼 `text-embedding-v4` 的单次 10 条限制，因此包含 11 个及以上 chunk 的文档会收到 HTTP 400。

## Goals / Non-Goals

**Goals:**

- 保证默认 Qwen Embedding 客户端发出的每个请求不超过 10 条文本。
- 允许索引服务继续一次提交完整 chunk 列表，由 LangChain 客户端透明分批并保持向量顺序。
- 通过配置级单元测试和大文档索引测试覆盖回归。

**Non-Goals:**

- 不改变文档 chunking 策略或默认 chunk 大小。
- 不改变 Milvus 写入格式、索引任务 API 或前端交互。
- 不为其他 Embedding 提供商引入动态限流系统。

## Decisions

- 在 `OpenAIEmbeddings` 构造时设置 `chunk_size=10`。批处理限制属于模型 Provider 约束，放在 Provider 层可以让索引、检索和未来调用方共享同一安全行为。
- 保留索引服务一次调用 `aembed_documents` 的抽象。LangChain 负责把输入拆成多个提供商请求并按原顺序合并响应，业务代码无需了解厂商批量上限。
- 增加索引服务对 11 个以上 chunk 的测试，并增加默认客户端 `chunk_size` 配置断言。前者验证业务结果完整，后者直接锁定真实客户端的请求上限。

## Risks / Trade-offs

- [较大文档会产生更多 HTTP 请求，索引耗时增加] -> 索引任务本身异步执行，优先保证兼容性和正确性。
- [提供商未来放宽批量上限后仍使用 10] -> 10 是当前稳定兼容值，只影响吞吐，不影响结果；后续可将其提升为项目配置项。
