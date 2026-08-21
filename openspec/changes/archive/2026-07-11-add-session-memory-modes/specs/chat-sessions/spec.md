## ADDED Requirements

### Requirement: Chat session memory state lifecycle
系统 SHALL 将会话记忆状态作为当前 user 聊天会话生命周期的一部分持久化和返回。

#### Scenario: Session responses include memory state
- **WHEN** 已认证 user 创建、列出或读取自己的会话
- **THEN** 每个会话 DTO MUST 包含该会话的模式、上下文占用、压缩消息数和最后压缩时间

#### Scenario: Clearing history resets compression
- **WHEN** user 清空一个聊天会话的消息
- **THEN** 后端 MUST 清空摘要、将压缩消息数重置为零并清除最后压缩时间，同时保留该会话选择的记忆模式
