## Why

当前 `knowledge_retrieval` 没有最低召回分数阈值，默认返回 5 条、允许调用方请求最多 20 条，并直接把 Milvus 向量分数作为最终相关度，未使用已配置的阿里云 `qwen3-vl-rerank`。这会让引用顺序依赖粗召回结果，也无法向 user 说明精排后的真实相对相关度。

## What Changes

- 将知识检索改为“两阶段”：Milvus 向量粗召回最多 20 条候选，再调用真实阿里云 `qwen3-vl-rerank` 精排。
- 最终结果和“本次回答引用”按精排分数从高到低排序，最多返回 5 条；不新增最低分阈值过滤。
- 在检索结果、引用 DTO、SSE 引用事件和消息元数据中同时保留 `vectorScore` 与 `rerankScore`，并让兼容字段 `score` 表示最终精排分数。
- 在聊天引用列表和来源详情中明确展示精排分数，并可同时查看向量召回分数。
- 为 Qwen provider 增加独立 rerank HTTP client、endpoint 配置、超时、重试和安全错误处理，不引入 DashScope SDK。
- 将 `llm.modelCapabilities` 从公共 `config/project.json` 移到 `config/user.project.json`，由现有项目配置合并机制加载。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `knowledge-retrieval-tool`: 增加向量候选粗召回、真实模型精排、最多 5 条降序结果及双分数字段。
- `api-and-sse-contracts`: 扩展检索和引用事件契约以区分向量分与精排分。
- `qwen-openai-provider`: 增加 `qwen3-vl-rerank` HTTP provider 和 user 项目配置要求。
- `chat-experience`: 本次回答引用列表及来源详情展示精排分数并保持降序。

## Impact

影响后端 LLM provider、检索工具、聊天/AIOps 引用转换、应用依赖装配、项目配置与测试；影响共享 TypeScript/OpenAPI/SSE 契约以及 Vue 聊天引用组件。外部依赖为阿里云百炼真实 rerank HTTP API，沿用现有 API Key。
