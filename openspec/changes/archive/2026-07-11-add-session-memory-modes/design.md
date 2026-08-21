## Context

聊天服务当前从 SQLite 读取会话的完整消息历史并全部交给 LangChain Agent。会话记录没有上下文预算、压缩策略或摘要边界，前端也无法预知模型窗口是否接近耗尽。本变更跨越数据库、Repository、聊天服务、共享契约和 Vue 输入区，并且必须保留用户可回看的完整历史。

## Goals / Non-Goals

**Goals:**
- 为每个会话独立保存记忆策略和压缩状态。
- 使用同一套确定性 token 估算在后端执行策略，并把占用信息返回前端。
- 通过 LLM 生成可继续对话的结构化摘要，模型仅接收摘要和未压缩消息。
- 对 70% 自动压缩和 95% 硬上限提供服务端保证。
- 让用户在输入框右侧查看并调整当前会话的记忆模式。

**Non-Goals:**
- 不删除或改写历史聊天消息。
- 不实现跨会话共享记忆或用户级长期记忆。
- 不追求与模型服务端 tokenizer 完全一致的 token 数；占用值是稳定的近似预算。
- 不改变 LangChain Agent 的工具调用和 SSE 增量协议。

## Decisions

### 在会话表持久化压缩边界和摘要

`chat_sessions` 增加 `memory_mode`、`memory_summary`、`compacted_message_count` 和 `last_compacted_at`。`compacted_message_count` 指向完整消息列表中已被摘要覆盖的前缀，因此历史仍可完整展示，而 Agent 请求只加载边界之后的消息。相比把摘要伪装成聊天消息，此结构不会污染用户历史或改变角色语义。

### 统一使用近似 token 计量和配置窗口

后端使用 LangChain Core 的 `count_tokens_approximately` 对系统提示、摘要和未压缩消息进行计量。OpenAI-compatible Chat Completions 响应只提供本次 `usage`，不会可靠返回模型最大上下文；因此窗口大小从受跟踪项目配置 `llm.modelCapabilities[chatModel].contextWindowTokens` 精确解析，模型没有能力条目时配置检查失败。所有 API 返回值和策略判断都使用同一算法；前端只展示后端结果，不自行估算。

### 压缩由独立服务协调

新增会话记忆服务负责读取消息、判断策略、调用 `LlmProvider` 生成摘要、更新 Repository 和计算状态。30 轮按“边界之后已完成的 assistant 消息数”判断；70% 策略按发送候选消息后的占用判断。自动压缩保留当前待发送 user 消息之外的最新上下文，手动压缩则压缩当前所有未压缩历史。

### 先检查预算再持久化新消息

流式发送在追加 user 消息前构造候选上下文。必要时先执行自动压缩并重新计量；若仍达到 95%，返回统一的 `CHAT_CONTEXT_LIMIT_REACHED` SSE 错误且不保存消息。HTTP 追加消息接口执行同样限制，避免绕过流式入口。

### 手动模式应用即执行压缩

`PUT /chat/sessions/{sessionId}/memory` 更新模式；当选择 `manual` 时，同一请求立即压缩现有未压缩消息。另提供 `POST /chat/sessions/{sessionId}/memory:compact` 供已处于手动模式的会话再次压缩。两者都返回刷新后的会话 DTO。

### 清空会话重置压缩状态

清空消息时 Repository 同时清空摘要、压缩边界和最后压缩时间，但保留用户选定的记忆模式。删除会话仍由级联关系删除全部状态。

## Risks / Trade-offs

- [近似 token 与供应商真实计数存在偏差] -> 使用 70% 自动阈值和 95% 硬阈值留出安全余量，并在 UI 标记为上下文占用而非精确账单 token。
- [摘要调用失败导致发送受阻] -> 自动压缩失败返回明确系统错误，不更新压缩边界；原始历史保持完整。
- [摘要本身随多次压缩增长] -> 新摘要提示要求合并旧摘要并限制长度，避免摘要无限扩张。
- [迁移后的旧会话缺少状态] -> 数据库列使用非空默认模式和边界，旧会话自动采用每 30 轮策略。

## Migration Plan

1. 先运行 Alembic 为已有会话补齐默认记忆状态。
2. 发布支持新字段的 Repository、服务和 API。
3. 发布共享契约与前端控件。
4. 回滚应用时可保留新增列；若需要完全回滚，Alembic downgrade 删除这些列，历史消息不受影响。

## Open Questions

无。
