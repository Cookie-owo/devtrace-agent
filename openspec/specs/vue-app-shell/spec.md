# Vue App Shell Specification

## Purpose

定义具有类型、响应式和经过身份验证的 Vue 应用程序外壳，为产品体验提供稳定的前端传输、路由、状态和反馈边界。
## Requirements
### Requirement: Route-based application shell
认证后的应用 SHALL 提供 `/chat`、`/knowledge`、`/aiops` 和 `/mcp` 工作区，并在桌面侧栏与移动导航中提供一致入口。

#### Scenario: 用户打开 MCP 管理
- **WHEN** 已认证用户访问 `/mcp`
- **THEN** 应用 MUST 在共享工作区框架中显示 MCP 连接管理页面。

### Requirement: Shared typed frontend transport
前端 SHALL 通过共享的类型化客户端边界访问后端 JSON 端点和 SSE 流，并且仅消费 `@agent-py/api-contracts` 定义。

#### Scenario: Typed API request succeeds
- **WHEN** 前端功能通过 API 客户端发送经过身份验证的请求
- **THEN** 客户端 MUST 附加活动的承载令牌，解码共享响应信封，并返回类型化的响应数据。

#### Scenario: Typed API request fails
- **WHEN** 后端请求返回统一的错误响应或格式错误的 JSON 正文
- **THEN** 客户端 MUST 会暴露一个标准化的前端错误，带有安全的 user 面消息和 MUST NOT 抛出未处理的 JSON 解析错误。

#### Scenario: SSE stream is consumed
- **WHEN** 前端功能打开 SSE 流
- **THEN** SSE 客户端 MUST 将流事件解析为共享的区分 `SseEvent` 合同，并对无效事件有效负载显示错误。

### Requirement: Frontend state and authentication guard
前端 SHALL 在应用状态中维护身份验证和临时请求反馈，同时在重新加载时仅保留承载令牌。

#### Scenario: Authentication is restored
- **WHEN** 浏览器使用持久化的承载令牌重新加载
- **THEN** 身份验证存储 MUST 在将 user 视为已认证之前查询当前-user 端点。

#### Scenario: Invalid token is cleared
- **WHEN** 恢复当前 user 失败，因为令牌无效或已被撤销
- **THEN** 前端 MUST 清除持久化的令牌并渲染公共路由。

#### Scenario: Feature reports an API error
- **WHEN** 路由级操作报告规范化的 API 错误
- **THEN** shell MUST 通过一致的可关闭反馈展示暴露安全消息。

### Requirement: Reusable async feedback states
前端 SHALL 为所有工作区路由体验提供可重用的中文加载、空状态、错误和任务状态展示组件。

#### Scenario: Route is loading
- **WHEN** 一个路由等待数据或初始化
- **THEN** 它 MUST 在路由内容区域中呈现一个可访问的中文加载状态。

#### Scenario: Route has no data
- **WHEN** 路由已成功加载，但没有要显示的项目
- **THEN** 它 MUST 应渲染一个可访问的中文空状态，并带有上下文相关的下一步操作文本。

#### Scenario: Route cannot load
- **WHEN** 路由请求失败
- **THEN** 它会显示规范化的错误信息和中文重试提示，当路由操作可重复时。

#### Scenario: Task state changes
- **WHEN** 一个工作区接收到现有的异步任务状态
- **THEN** 它 MUST 将渲染共享的基于文本的中文生命周期处理，而不是单独的未翻译原始状态。

### Requirement: Chat sessions live in the workspace sidebar
工作区 SHALL 在桌面对话路由的全局左侧栏中提供会话创建和历史会话导航，并使用聊天 store 作为唯一会话状态来源。

#### Scenario: User opens the chat workspace on desktop
- **WHEN** 已登录 user 进入对话路由且桌面左侧栏可见
- **THEN** “对话”导航项之后 MUST 显示新建对话入口和按时间倒序排列的历史会话，聊天主区域 MUST NOT 再显示独立历史列

#### Scenario: User creates a conversation from the rail
- **WHEN** user 点击左侧栏中的新建对话按钮
- **THEN** 前端 MUST 通过现有 chat store 创建并选中新会话，主对话区域 MUST 切换到该会话

#### Scenario: User selects or deletes rail history
- **WHEN** user 在左侧栏选择或删除一项历史会话
- **THEN** 前端 MUST 调用现有会话操作并让左侧栏和主对话区域反映同一状态

### Requirement: Routed workspaces fill the desktop application surface
工作区 SHALL 将全局 header 以下、左侧栏右侧的全部可用桌面空间交给当前路由视图，不得使用居中最大宽度或通用外层留白缩小业务界面。

#### Scenario: User opens a primary workspace
- **WHEN** user 打开对话、知识库或智能诊断任一桌面 Web 路由
- **THEN** 对应根视图 MUST 紧贴路由内容区边界并占满可用宽度和高度，MUST NOT 暴露外围 canvas 留白

#### Scenario: Workspace content is longer than its surface
- **WHEN** 当前业务视图内容超过可用高度
- **THEN** 业务视图 MUST 在自身定义的区域内滚动，MUST NOT 通过全局内容 padding 或文档滚动制造额外留白

### Requirement: Global operation feedback auto-dismisses
应用 shell 的全局操作提示 MUST 在显示 3 秒后自动关闭，同时 MUST 保留用户手动关闭能力。

#### Scenario: 操作成功提示自动关闭
- **WHEN** 页面显示“反馈已保存”“MCP 连接已保存”或其他全局操作提示
- **THEN** 提示 MUST 在 3 秒后自动从页面移除。

#### Scenario: 新提示替换旧提示
- **WHEN** 旧提示的 3 秒计时结束前出现新提示
- **THEN** 旧计时 MUST 被取消，并且新提示 MUST 从替换时刻起获得完整的 3 秒显示时间。
