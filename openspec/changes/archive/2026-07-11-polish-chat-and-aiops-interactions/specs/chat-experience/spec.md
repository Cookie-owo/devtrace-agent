## ADDED Requirements

### Requirement: Compact keyboard-first chat composer
聊天工作区 SHALL 提供不可拖拽缩放的紧凑消息输入框，并支持高效键盘发送与显式换行。

#### Scenario: User presses Enter
- **WHEN** 输入框包含非空文本且 user 在非 IME 组合状态下按 Enter 且未按 Shift
- **THEN** 前端 MUST 阻止默认换行、发送去除首尾空白后的消息并清空输入框

#### Scenario: User presses Shift Enter
- **WHEN** user 在输入框中按 Shift+Enter
- **THEN** 前端 MUST 保留换行行为且 MUST NOT 发送消息

#### Scenario: User attempts to resize the composer
- **WHEN** 聊天输入框显示在桌面或窄视口
- **THEN** 浏览器 MUST NOT 显示 textarea 拖拽缩放控制，输入区域 MUST 保持稳定布局

### Requirement: Content-sized user message bubbles
聊天工作区 SHALL 让 user 消息气泡根据内容占用必要宽度，并限制长消息的最大阅读宽度。

#### Scenario: User sends a short message
- **WHEN** user 消息只包含短文本
- **THEN** 气泡 MUST 收缩到接近文本宽度，MUST NOT 占据会话主区域的大部分宽度

#### Scenario: User sends a long unbroken message
- **WHEN** user 消息包含长文本或连续字符串
- **THEN** 气泡 MUST 在最大宽度内换行且 MUST NOT 导致页面水平溢出
