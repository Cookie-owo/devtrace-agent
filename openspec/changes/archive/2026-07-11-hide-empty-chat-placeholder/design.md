## Context

`ChatTranscript` 在 `messages.length === 0` 时渲染通用 `AppEmptyState`。该组件同时生成标题、说明和一个使用 accent 颜色的 `.empty-state__mark`，这正是空会话中绿色矩形的来源。

## Goals / Non-Goals

**Goals:**

- 空会话消息区域完全留白。
- 删除聊天对通用空状态组件的依赖。
- 不影响加载状态和已有消息。

**Non-Goals:**

- 不删除或修改通用 `AppEmptyState`，其他工作区仍可使用。
- 不修改新建会话、消息发送或持久化流程。

## Decisions

- 删除 `ChatTranscript` 对 `AppEmptyState` 的 import 和空消息模板分支。`v-if` 继续负责加载状态，消息列表使用 `v-else-if="messages.length > 0"`，两者都不满足时不渲染消息内容。
- 测试直接挂载空消息 transcript，断言文案和 `.empty-state__mark` 均不存在。

## Risks / Trade-offs

- [空区域可能缺少引导] → 产品明确要求保持空白，输入框 placeholder 仍提供必要提示。
