## Context

前端 `references` 当前由全部历史消息聚合，新一轮发送前不清空，完成后又将流式引用与历史引用合并。后端已经使用 SSE，但将 LangChain 的模型 chunk 原样作为一个 `content.delta` 发出，因此 chunk 较大时表现为整段出现。

## Goals / Non-Goals

**Goals:**

- “本次回答引用”严格对应最新一轮 assistant 回答。
- 模型正文按单个 Unicode 字符发出独立 `content.delta`。
- 保持最终持久化正文、事件序列和其他事件类型不变。

**Non-Goals:**

- 不拆分 reasoning、tool、reference 或 complete 事件。
- 不改变 LangChain Agent、SSE 契约或数据库结构。

## Decisions

- 前端发送开始即清空引用；会话加载只读取最后一条 assistant 消息的 citations，完成后不再合并历史引用。
- 在 `ChatStreamingService` 边界拆分 `ChatAgentContentDelta.delta`，因为该层能保证只有最终回答正文被处理，且无论上游 token 粒度如何都输出一致。
- 每个字符递增 sequence，`answer_parts` 仍按原始 chunk 追加，避免持久化内容发生变化。

## Risks / Trade-offs

- [SSE 事件数量增加] → 仅拆分最终正文，不拆分推理和工具负载。
- [Unicode 组合字符可能由多个 code point 组成] → 当前产品以 Python 字符粒度输出，中文、字母、标点均满足逐字体验；不增加新依赖。
