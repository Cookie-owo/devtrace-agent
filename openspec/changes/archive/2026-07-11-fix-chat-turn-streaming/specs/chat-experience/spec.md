## ADDED Requirements

### Requirement: Current-turn citation isolation
聊天工作区 SHALL 只在“本次回答引用”区域展示当前发送轮次或最新 assistant 回答的引用。

#### Scenario: User starts a new turn after a cited answer
- **WHEN** 上一轮存在引用且 user 再次发送消息
- **THEN** 前端 MUST 在发送开始时立即清空上一轮引用，并仅追加新一轮收到的引用事件

#### Scenario: Latest answer has no citations
- **WHEN** 最新 assistant 回答不包含引用
- **THEN** “本次回答引用”区域 MUST 保持隐藏，即使更早的历史回答包含引用

### Requirement: Character-by-character answer rendering
聊天工作区 SHALL 按后端 `content.delta` 的单字符增量逐步渲染模型最终回答。

#### Scenario: Model returns a multi-character chunk
- **WHEN** 后端模型输出包含多个字符的正文 chunk
- **THEN** 前端 MUST 通过连续的单字符 SSE 增量逐字追加正文，而不是一次替换成整段答案
