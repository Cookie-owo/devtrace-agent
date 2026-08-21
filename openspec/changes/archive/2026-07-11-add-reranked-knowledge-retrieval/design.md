## Context

当前知识检索只执行 Milvus 向量搜索，并直接将向量距离转换后的分数作为最终相关度。虽然项目已经配置 `qwen3-vl-rerank`，但后端没有 rerank provider、依赖装配或双分数契约，前端也无法区分粗召回与精排结果。该改动横跨配置、LLM provider、检索工具、聊天/AIOps 引用、共享契约和 Vue 展示。

## Goals / Non-Goals

**Goals:**

- 用真实阿里云 `qwen3-vl-rerank` 对 tenant 过滤后的 Milvus 候选进行精排。
- 最终结果按精排分数降序且最多 5 条，并同时保留向量分和精排分。
- 让聊天 SSE、持久化消息及前端引用详情使用同一份分数语义。
- 通过现有项目配置系统加载 rerank endpoint、模型和模型能力。

**Non-Goals:**

- 不新增最低相关度阈值；精排分数是本次请求内的相对分数。
- 不更换 Milvus 索引、Embedding 模型或权限过滤方式。
- 不引入 DashScope SDK，也不让业务层直接依赖厂商客户端。

## Decisions

### 使用 provider 协议封装阿里云 rerank HTTP API

新增异步 `RerankModel` 协议及 `QwenVlRerankModel` 实现，由 `QwenOpenAIProvider` 创建。实现使用现有 `httpx` 依赖调用阿里云百炼文本排序 endpoint，并复用 provider 的 API key、timeout 和 retry 配置。这样检索业务只依赖稳定协议，后续可替换其他兼容排序模型。

未选择 DashScope SDK，因为项目约束要求业务不依赖模型厂商私有 SDK；也不复用 `ChatOpenAI`，因为文本排序不是 OpenAI Chat Completions 协议。

### 先权限过滤再精排

Milvus 最多粗召回 20 条候选，后端先应用 owner、tenant、知识库、文档和 metadata 过滤，再把允许访问的候选内容发送给 rerank。最终按 `relevance_score` 降序取调用方请求数量，且硬上限为 5。

这能避免将无权限内容发送给外部模型，也比只召回 5 条后再精排保留更多候选空间。

### `score` 兼容字段代表最终精排分

检索命中和引用增加 `vectorScore` 与 `rerankScore`；现有 `score` 保留，但统一等于 `rerankScore`。前端以精排分排序和展示，同时在详情中展示向量召回分。历史消息缺少新字段时，前端仍可读取旧 `score`。

### 精排失败显式失败

精排遇到网络、限流、上游服务或响应校验错误时，经有限重试后抛出安全的统一系统错误，不回退到向量排序。否则调用方无法判断展示的是哪一种分数。

### 用户配置承载模型能力

从 `config/project.json` 删除 `llm.modelCapabilities`，写入 `config/user.project.json` 并通过现有深度合并加载。rerank endpoint 也由配置提供，代码不读取本机环境变量。

## Risks / Trade-offs

- [每次检索增加一次网络请求和延迟] → 仅发送最多 20 条候选，沿用 timeout 和有限重试，并在错误中明确上游不可用。
- [文档过长导致 rerank 请求变大] → 只发送已切分 chunk 内容，并限制候选数量。
- [旧消息没有双分数字段] → 前端读取 `rerankScore ?? score`，新消息完整写入两个分数。
- [精排分数不适合作为跨请求绝对阈值] → 本次不设置最低阈值，只用于单次候选排序和展示。

## Migration Plan

1. 更新配置和 provider，并通过真实 endpoint 连通性测试。
2. 更新检索、引用转换和应用依赖装配。
3. 更新共享 TypeScript/OpenAPI 契约和前端展示。
4. 运行后端、前端、契约与 OpenSpec 全量检查。
5. 回滚时可整体回退该提交；不涉及数据库迁移。

## Open Questions

无。
