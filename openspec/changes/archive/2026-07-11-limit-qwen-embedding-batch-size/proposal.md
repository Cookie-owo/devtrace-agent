## Why

阿里云百炼 `text-embedding-v4` 的 OpenAI-compatible 接口限制单次请求最多包含 10 条文本。当前索引服务会把文档的全部 chunk 交给默认 Embedding 客户端，较大文档因此在向量生成阶段返回 HTTP 400 并导致索引失败。

## What Changes

- 将 Qwen Embedding 客户端的单批文本数量限制为 10。
- 对超过 10 个 chunk 的文档自动分批生成向量，并保持输入与输出顺序一致。
- 增加超过接口批量上限的回归测试，防止文档索引再次触发 `batch size is invalid`。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `qwen-openai-provider`: 明确 `text-embedding-v4` 请求必须遵守单次最多 10 条文本的提供商限制，并自动处理更大的输入集合。

## Impact

- 后端 Qwen/OpenAI-compatible Embedding 客户端构造配置。
- LLM Provider 单元测试和文档索引回归测试。
- 不修改 HTTP API、SSE 契约、Milvus schema 或前端行为。
