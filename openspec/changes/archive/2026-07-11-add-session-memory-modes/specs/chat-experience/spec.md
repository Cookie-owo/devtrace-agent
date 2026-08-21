## ADDED Requirements

### Requirement: Session memory controls beside composer
桌面 Web 聊天工作区 SHALL 在输入框右侧展示当前会话上下文占比和会话级记忆模式控件。

#### Scenario: User views memory state
- **WHEN** user 打开或切换聊天会话
- **THEN** 输入框右侧 MUST 展示后端返回的上下文占比和该会话当前记忆模式

#### Scenario: User applies a memory mode
- **WHEN** user 选择三种模式之一并点击应用
- **THEN** 前端 MUST 调用类型化后端 API、显示执行中状态并使用返回值刷新当前会话

#### Scenario: Manual mode is applied
- **WHEN** user 选择“手动压缩”并点击应用
- **THEN** 前端 MUST 明确显示后端正在主动压缩，完成后刷新上下文占比

### Requirement: Composer context limit feedback
聊天输入区 SHALL 根据后端会话状态执行 95% 上下文硬上限反馈。

#### Scenario: Context reaches hard limit
- **WHEN** 当前会话上下文占比达到或超过 95%
- **THEN** 输入框和发送按钮 MUST 被禁用，并显示“上下文已达到 95%，请执行手动压缩”的中文提示
