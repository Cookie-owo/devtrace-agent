## Why

后端已经以单字符 SSE 输出模型正文，但没有字符间隔，浏览器网络读取和 Vue 批量渲染会把多个字符合并到同一视觉帧，用户仍然感觉答案一次性出现。

## What Changes

- 在前端聊天 store 消费 `content.delta` 时加入稳定的逐字符显示节奏。
- 每次正文更新后等待跨过渲染帧，再消费下一个字符。
- 仅影响模型正文；工具调用、知识库引用、推理和完成事件继续即时处理。
- 增加 fake timer 测试，验证正文不会在计时器推进前一次性显示。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `chat-experience`: 将逐字符事件进一步约束为视觉上可感知的打字机节奏。

## Impact

影响 Vue chat store 与前端测试；不修改后端 SSE、共享契约、Agent 或持久化数据。
