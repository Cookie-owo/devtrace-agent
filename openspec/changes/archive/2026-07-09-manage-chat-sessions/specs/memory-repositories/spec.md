## ADDED Requirements

### Requirement: Chat session lifecycle repositories
后端 SHALL 在 owner 范围内公开用于更新聊天会话标题、清除聊天消息和删除聊天会话的仓库操作。

#### Scenario: Session title can be updated by owner
- **WHEN** 业务代码使用 owner user ID 和会话 ID 更新聊天会话标题
- **THEN** 仓库 MUST 仅对属于该 user 的会话保存新标题

#### Scenario: Session messages can be cleared by owner
- **WHEN** 业务代码清除具有 owner user ID 和会话 ID 的聊天消息
- **THEN** 仓库 MUST 仅删除属于该 user 会话的消息，并保持会话记录完整。

#### Scenario: Session can be deleted by owner
- **WHEN** 业务代码根据 owner user ID 和会话 ID 删除聊天会话
- **THEN** 仓库 MUST 仅删除该 user 的会话及其消息

#### Scenario: Cross-tenant lifecycle mutation is denied
- **WHEN** 调用者在提供的 owner 范围外更新、清除或删除聊天会话
- **THEN** 仓库 MUST 拒绝或返回无变更，而不是更改另一个 user 的数据。
