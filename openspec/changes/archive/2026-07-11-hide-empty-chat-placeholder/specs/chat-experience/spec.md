## ADDED Requirements

### Requirement: Empty chat transcript remains blank
聊天工作区 SHALL 在当前会话没有消息且不处于加载状态时保持消息记录区域空白，不得渲染通用空状态标题、说明或装饰标记。

#### Scenario: User opens a new empty conversation
- **WHEN** 当前会话消息数组为空且加载已经完成
- **THEN** transcript MUST NOT 显示“从一个问题开始”或“可以询问系统状态、排障建议或知识库中的内容”，MUST NOT 渲染 `.empty-state__mark`

#### Scenario: Conversation is loading
- **WHEN** 当前会话仍在加载
- **THEN** transcript MUST 继续显示加载状态，不得用空白状态替代加载反馈
