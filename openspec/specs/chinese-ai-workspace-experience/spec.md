# Chinese AI Workspace Experience Specification

## Purpose

定义由所有已认证的前端体验共享的中文视觉语言、响应式工作区布局和可访问的异步任务反馈。

## Requirements

### Requirement: Chinese AI workspace visual language
经过身份验证的前端 SHALL 会渲染一个以中文语言显示的AI工作区，包含一个持久化的桌面导航栏、一个专注的主要工作表面、语义状态颜色以及响应式的移动导航模式。面向用户的文本 MUST 应为中文，除非是必要的技术术语、模型名称、MCP、SSE 以及由工具原样返回的数据。

#### Scenario: Authenticated user enters a workspace
- **WHEN** 已认证的 user 在桌面视口上打开聊天、知识或 AIOps  
- **THEN** 前端 MUST 以统一的视觉语言展示稳定的导航栏、当前工作区上下文、账户控制以及不重叠的主要工作区域。

#### Scenario: User opens a narrow viewport
- **WHEN** 已认证的 user 在窄视口下打开工作区
- **THEN** 主导航、路由内容、标题、操作和长中文标签 MUST 在不出现水平页面溢出的情况下仍可访问。

### Requirement: Visible asynchronous task lifecycle
前端 SHALL 使用共享的中文状态处理来表示等待、准备、运行中、已完成和失败状态，而无需发明后端进度或结论。

#### Scenario: Background work has not started or is waiting
- **WHEN** 现有文档索引任务或诊断任务报告 `pending` 或 `accepted`
- **THEN** 前端 MUST 可视化地将任务标识为等待或准备状态，并保留对相关上下文内容的访问权限。

#### Scenario: Background work is active
- **WHEN** 一个聊天流、文档索引任务、警报刷新或 AIOps 诊断正在运行
- **THEN** 前端 MUST 显示中文进行中的状态，防止在适用时重复提交，并保持当前操作可识别。

#### Scenario: Background work reaches a terminal state
- **WHEN** 任务或流报告完成或失败
- **THEN** 前端 MUST 在存在重试或恢复操作时，显示中文的完成或失败状态并提供现有的重试或恢复操作。

### Requirement: Accessible operation feedback
前端 SHALL 通过可访问的反馈公开异步状态和标准化错误，而不依赖颜色单独进行。

#### Scenario: User receives a status update or error
- **WHEN** 一个工作区从等待状态变为运行中、完成，或返回标准化错误
- **THEN** 前端 MUST 渲染基于文本的状态，为动态反馈使用适当的生活区域，并保留可见的键盘焦点指示器。
