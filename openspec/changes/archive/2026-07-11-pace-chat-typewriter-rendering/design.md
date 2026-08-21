## Context

后端每个 `content.delta` 已经只有一个字符，但 StreamingResponse、TCP、fetch ReadableStream 和 Vue 更新调度都可能在一个渲染帧内处理多个事件。单字符协议并不等于用户能看到单字符动画。

## Goals / Non-Goals

**Goals:**

- 无论网络多快，模型正文都以稳定、肉眼可见的节奏逐字追加。
- 流完成前排空正文显示队列，避免最终持久化消息提前覆盖动画。
- 保持其他 SSE 事件即时处理。

**Non-Goals:**

- 不人为延迟工具调用、知识引用、推理或错误状态。
- 不修改后端流式协议和模型推理速度。

## Decisions

- 在 Vue store 的 `content.delta` 消费分支按字符迭代，并在每个字符后等待 28ms。`await` 会让出事件循环，使 Vue 至少有机会完成一次 DOM flush。
- 即使上游意外发送多字符 delta，前端仍会拆分，作为显示层的防御性保证。
- 流循环自然等待队列完成后再处理 `complete` 和重新加载会话，无需额外并发队列或取消控制器。

## Risks / Trade-offs

- [长答案的视觉完成时间增加] → 28ms 约为每秒 36 个字符，能感知但不会像逐词动画一样过慢。
- [测试耗时增加] → 使用 fake timers 验证节奏，不让单元测试真实等待。
