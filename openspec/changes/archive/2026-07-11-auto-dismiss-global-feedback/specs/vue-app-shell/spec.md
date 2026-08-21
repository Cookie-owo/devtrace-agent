## ADDED Requirements

### Requirement: Global operation feedback auto-dismisses
应用 shell 的全局操作提示 MUST 在显示 3 秒后自动关闭，同时 MUST 保留用户手动关闭能力。

#### Scenario: 操作成功提示自动关闭
- **WHEN** 页面显示“反馈已保存”“MCP 连接已保存”或其他全局操作提示
- **THEN** 提示 MUST 在 3 秒后自动从页面移除。

#### Scenario: 新提示替换旧提示
- **WHEN** 旧提示的 3 秒计时结束前出现新提示
- **THEN** 旧计时 MUST 被取消，并且新提示 MUST 从替换时刻起获得完整的 3 秒显示时间。
