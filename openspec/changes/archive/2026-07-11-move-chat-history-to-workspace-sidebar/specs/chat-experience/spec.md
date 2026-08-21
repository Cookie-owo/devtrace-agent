## ADDED Requirements

### Requirement: Conversation-first chat workspace layout
聊天工作区 SHALL 将侧栏右侧的主要可用空间用于对话正文和对话配置，桌面端不得重复渲染历史会话列。

#### Scenario: Desktop conversation is displayed
- **WHEN** user 在桌面视口打开对话工作区
- **THEN** 对话区 MUST 使用移除历史列后释放的宽度，消息、输入框和配置区域 MUST 保持无水平溢出

#### Scenario: Chat view owns no duplicate session list
- **WHEN** user 打开桌面 Web 对话工作区
- **THEN** `ChatView` MUST NOT 渲染第二份历史会话列表或移动端专用会话入口

### Requirement: Neutral chat focus treatment
聊天界面的输入框和可聚焦控件 SHALL 不显示额外的焦点矩形，不得显示绿色或灰色 outline、边框变化或焦点光晕。

#### Scenario: User focuses the chat composer
- **WHEN** user 点击聊天输入框或通过键盘将焦点移入输入框
- **THEN** 输入容器 MUST 保持未聚焦时的边框和阴影，MUST NOT 显示绿色或灰色矩形框

#### Scenario: Keyboard focus moves across chat controls
- **WHEN** keyboard user 在聊天界面的按钮、链接和表单控件间移动焦点
- **THEN** 控件 MUST NOT 显示浏览器或应用注入的矩形 outline

## MODIFIED Requirements

### Requirement: Content-sized user message bubbles
聊天工作区 SHALL 让 user 与 assistant 消息使用相同的透明正文容器和内容宽度，不得为 user 消息添加独立气泡视觉，同时 MUST 保留 user 靠右、assistant 靠左的对话分流。

#### Scenario: User sends a short message
- **WHEN** user 消息只包含短文本
- **THEN** 消息 MUST 与 assistant 消息使用相同背景和间距，但 MUST 靠右显示并通过角色标签标识“你”

#### Scenario: User sends a long unbroken message
- **WHEN** user 消息包含长文本或连续字符串
- **THEN** 消息 MUST 在共享正文最大宽度内换行且 MUST NOT 导致页面水平溢出
