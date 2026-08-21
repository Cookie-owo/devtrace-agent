## Why

聊天界面的“本次回答引用”会跨轮次残留，并且 Qwen/Agent 返回较大文本 chunk 时，虽然底层使用 SSE，用户仍会看到整段答案一次出现。这两项行为破坏了“本次回答”的语义和流式阅读体验。

## What Changes

- 新一轮发送开始时立即清空上一轮引用，流式阶段只展示当前轮引用。
- 会话重新加载时仅使用最新 assistant 回答的引用，不聚合整个历史。
- 只把模型最终回答的 `content.delta` 拆成逐字符 SSE 事件；推理、工具调用、引用和完成事件保持原有结构与时序。
- 补充跨轮引用隔离和逐字符正文流的回归测试。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `chat-experience`: 明确“本次回答引用”的轮次隔离和模型正文逐字符展示。
- `stream-rag-chat`: 明确模型正文使用逐字符 `content.delta`，其他事件不拆分。

## Impact

影响 Vue chat store、聊天 SSE 编排服务及其前后端测试；不修改共享事件类型、工具调用、知识引用结构或数据库模型。
