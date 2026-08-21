# Chat Experience Specification

## Purpose

定义经过身份验证的、后端持久化的 Vue 聊天工作区，包括安全的流式助理输出、引用展示和工具调用活动。
## Requirements
### Requirement: Persisted conversation workspace
前端 SHALL 通过共享的后端 API 合同提供经过身份验证的中文聊天工作区，该工作区创建、列出、选择和删除当前 user 的聊天会话。工作区 SHALL 优先处理活动对话，同时保持会话控制紧凑且易于访问。

#### Scenario: User opens the Chat workspace
- **WHEN** 已认证的 user 打开 `/chat`
- **THEN** 前端 MUST 仅从后端加载该 user 的会话，并用中文会话控制渲染最近更新的会话。

#### Scenario: User starts and switches conversations
- **WHEN** 一个 user 开始对话或选择现有会话
- **THEN** 前端 MUST 通过后端创建或获取会话，并在聚焦的对话界面上渲染其持久化的消息历史。

#### Scenario: User deletes a conversation
- **WHEN** 一个 user 删除选定的聊天会话
- **THEN** 前端 MUST 通过后端删除它，并从可见的会话列表中移除，而不依赖 localStorage。

### Requirement: Streaming chat interaction
前端 SHALL 通过输入的聊天流式客户端发送提示，并将共享的 SSE 事件渲染为可见的中文对话进度。

#### Scenario: Assistant draft streams
- **WHEN** 流媒体端点会发出 `content.delta` 事件
- **THEN** 前端 MUST 将每个增量追加到当前的助手草稿中，并明显标识出正在生成响应，同时发送仍在进行中。

#### Scenario: Streaming completes or fails
- **WHEN** 该端点会发出 `complete` 或 `error` 事件，或者请求失败
- **THEN** 前端 MUST 重新协调已保存的会话，或显示规范化的中文错误，并且 MUST NOT 作为已保存的答案显示未完成的草稿。

### Requirement: Answer context presentation
聊天工作区 SHALL 渲染安全的 Markdown 答案，并从共享消息和 SSE 合同中暴露源和工具调用上下文。

#### Scenario: Assistant answer contains Markdown
- **WHEN** 一个助手消息包含 Markdown 语法
- **THEN** 前端 MUST 在移除不可信的原始 HTML 的同时渲染支持的格式

#### Scenario: Answer uses knowledge references
- **WHEN** 一个流或持久化消息包含引用参考
- **THEN** 前端 MUST 显示源标题，并将其与工具调用活动区分开来。

#### Scenario: Tool call progresses
- **WHEN** 一个流发出 `tool.call` 事件，或者活动会话有工具调用审计
- **THEN** 前端 MUST 显示每个工具名称、生命周期状态以及可用的绑定结果或错误摘要。

### Requirement: Responsive chat feedback states
聊天工作区 SHALL 在桌面和窄版布局中提供中文的会话空状态、历史加载中状态、发送进行中状态、来源、工具活动和错误状态。在桌面布局中，对话外壳 SHALL 会使用可用的视口高度，并将消息滚动限制在转录区域，同时保持会话控制和创作器可用。

#### Scenario: User has no conversations
- **WHEN** 后端返回一个空的会话集合
- **THEN** 工作区 MUST 渲染一个空的对话状态，并提供一个可用的命令以开始新的对话。

#### Scenario: Send is in progress
- **WHEN** 一个聊天发送正在进行中
- **THEN** 作者 MUST 防止重复发送并显示响应正在流式传输。

#### Scenario: Long desktop conversation remains contained
- **WHEN** 一个桌面对话的消息足够多，以至于超过了可见的工作区高度  
- **THEN** 会话列表、对话头和创作者 MUST 在仅对话区域垂直滚动且页面 MUST NOT 随消息列表增长时仍保持可用。

#### Scenario: Narrow screen renders chat controls
- **WHEN** 在窄视口下查看工作区
- **THEN** 会话选择、传记、创作器、源列表和工具活动控件 MUST 在不出现水平溢出的情况下仍可读且可操作。

### Requirement: Chat assembly controls
经过身份验证的 Chat 工作区 SHALL 让 user 可以在中文中查看、选择、确认和恢复其基于服务器的系统提示和多选标准 Skill 配置，并 SHALL 将系统提示词和 Skill 设置呈现为两个独立侧边栏。

#### Scenario: User opens split chat configuration sidebars
- **WHEN** 已认证的 user 打开 Chat 工作区
- **THEN** 前端 MUST 通过共享合约加载当前配置，并显示“对话系统提示词设置”和“Skill 设置”两个独立侧边栏，而不以 localStorage 作为事实来源

#### Scenario: User manages collapsible system prompts
- **WHEN** user 在“对话系统提示词设置”侧边栏查看提示词
- **THEN** 每个提示词 MUST 可折叠和展开，展开后可以编辑名称和正文、保存、删除，并且界面 MUST 只允许单选一个后续对话使用的系统提示词。

#### Scenario: User manages multi-select standard Skills
- **WHEN** user 在“Skill 设置”侧边栏查看 Skill
- **THEN** 界面 MUST 显示标准 `SKILL.md` 上传规范、每个 Skill 的 name 和 description，允许上传、删除，并允许多选零个或多个 Skill 供后续对话 Agent 按需加载

#### Scenario: User confirms an updated assembly
- **WHEN** 选择提示或技能并确认
- **THEN** 前端 MUST 通过类型化 API 客户端保存配置，显示保存的装配摘要，并用于后续消息。

#### Scenario: Configuration action fails
- **WHEN** 提示词或 Skill 的创建、保存、删除、上传或配置保存失败
- **THEN** 前端 MUST 在相关侧边栏中显示中文错误，说明可恢复动作，MUST NOT 静默保留一个看似已保存的状态。

### Requirement: Collapsible assistant execution context
聊天工作区 SHALL 会将每个助手消息的可用工具调用和模型提供的深度思考内容作为单独的中文、可使用键盘操作的、初始折叠的详细信息显示在该消息下方。

#### Scenario: Assistant used tools
- **WHEN** 流式或持久化的助手响应包含工具审计记录
- **THEN** 前端 MUST 在相应的助手消息下方显示一个折叠的工具调用摘要，并在 user 展开后才显示有限的详细信息。

#### Scenario: Assistant has reasoning content
- **WHEN** 流式或持久化助手响应包含模型提供的推理元数据
- **THEN** 前端 MUST 在该消息下方显示一个折叠的深度思考摘要，而不将推理作为最终答案文本展示。

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
聊天工作区 SHALL 让 user 与 assistant 消息使用相同的透明正文容器和内容宽度，不得为 user 消息添加独立气泡视觉，同时 MUST 保留 user 靠右、assistant 靠左的对话分流。

#### Scenario: User sends a short message
- **WHEN** user 消息只包含短文本
- **THEN** 消息 MUST 与 assistant 消息使用相同背景和间距，但 MUST 靠右显示并通过角色标签标识“你”

#### Scenario: User sends a long unbroken message
- **WHEN** user 消息包含长文本或连续字符串
- **THEN** 消息 MUST 在共享正文最大宽度内换行且 MUST NOT 导致页面水平溢出

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

### Requirement: Empty chat transcript remains blank
聊天工作区 SHALL 在当前会话没有消息且不处于加载状态时保持消息记录区域空白，不得渲染通用空状态标题、说明或装饰标记。

#### Scenario: User opens a new empty conversation
- **WHEN** 当前会话消息数组为空且加载已经完成
- **THEN** transcript MUST NOT 显示“从一个问题开始”或“可以询问系统状态、排障建议或知识库中的内容”，MUST NOT 渲染 `.empty-state__mark`

#### Scenario: Conversation is loading
- **WHEN** 当前会话仍在加载
- **THEN** transcript MUST 继续显示加载状态，不得用空白状态替代加载反馈

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

### Requirement: Reranked citation presentation
聊天工作区 SHALL 将本次回答引用按精排分数降序展示，最多展示 5 条，并明确区分精排分数与向量召回分数。

#### Scenario: 本次回答包含引用
- **WHEN** 流式回答收到一个或多个带有精排分数的引用事件
- **THEN** “本次回答引用”列表 MUST 按 `rerankScore` 从高到低显示最多 5 条，并 MUST 将其标记为精排分数

#### Scenario: User opens citation detail
- **WHEN** user 查看某个知识引用详情
- **THEN** 前端 MUST 显示可用的精排分数和向量召回分数，并保持来源、文档及 metadata 可追溯

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

### Requirement: Perceptible model typewriter pacing
聊天工作区 SHALL 以稳定、可感知的时间间隔逐字显示模型最终回答，而不是在同一渲染帧批量显示多个字符。

#### Scenario: Network delivers content faster than rendering
- **WHEN** SSE 客户端快速收到多个正文字符或一个多字符正文增量
- **THEN** 前端 MUST 将正文拆为字符并在相邻字符之间等待显示节奏，MUST NOT 在一个同步更新中追加整段文本

#### Scenario: Content queue reaches completion
- **WHEN** 后端已经发出 `complete` 事件
- **THEN** 前端 MUST 先按顺序显示此前收到的全部正文字符，再用持久化 assistant 消息完成会话协调

#### Scenario: Non-content event is received
- **WHEN** 前端收到工具调用、知识引用、推理、状态或错误事件
- **THEN** 该事件 MUST 保持原有处理方式，不得进入正文打字机延迟队列

### Requirement: Chat answer and citation feedback
聊天工作区 SHALL 允许用户评价助手消息和具体引用，并在重新打开会话时恢复当前用户已提交的反馈状态。

#### Scenario: 用户评价引用
- **WHEN** 用户在引用详情中提交反馈
- **THEN** 反馈 MUST 关联助手消息与 citation id。
