## Why

空会话当前渲染通用 `AppEmptyState`，导致出现用户不需要的引导文案和绿色 `.empty-state__mark` 装饰。聊天主区域在没有消息时应保持干净空白。

## What Changes

- 空会话不再渲染“从一个问题开始”标题和说明文字。
- 空会话不再实例化 `AppEmptyState`，从根源移除绿色 `.empty-state__mark`。
- 保留加载状态、已有消息、输入框和其他聊天功能。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `chat-experience`: 空聊天记录区域保持空白，不展示通用空状态文案或装饰标记。

## Impact

仅影响 `ChatTranscript` 及聊天组件测试；不影响通用 `AppEmptyState` 在知识库等其他页面的使用。
