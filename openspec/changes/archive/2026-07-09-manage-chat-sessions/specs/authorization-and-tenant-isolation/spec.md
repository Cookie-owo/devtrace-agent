## ADDED Requirements

### Requirement: Chat session operation isolation
系统 SHALL 将每个聊天会话管理操作的作用域限定为已认证的 user 的 tenant 作用域。

#### Scenario: Chat list is scoped
- **WHEN** 一个 user 列出聊天会话
- **THEN** 后端 MUST 仅返回属于该 user 的 tenant 范围的会话

#### Scenario: Chat history is scoped
- **WHEN** 一个 user 读取、追加、清除或删除聊天会话
- **THEN** 后端 MUST 将当前 user 的 tenant 范围应用于仓库操作。

#### Scenario: Cross-tenant chat mutation is forbidden
- **WHEN** 一个经过身份验证的 user 尝试读取、追加到、清空或删除另一个 user 的聊天会话
- **THEN** 后端 MUST 返回统一的授权错误，并且 MUST NOT 不更改其他 user 的聊天数据。
