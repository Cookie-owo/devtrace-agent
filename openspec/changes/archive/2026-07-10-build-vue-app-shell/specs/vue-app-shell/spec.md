## ADDED Requirements

### Requirement: Route-based application shell
前端 SHALL 通过 Vue Router 暴露公共的登录和注册路由以及经过身份验证的聊天、知识和 AIOps 工作区路由。

#### Scenario: Anonymous user opens protected route
- **WHEN** 未经过身份验证的访客直接导航到工作区路由
- **THEN** 路由器 MUST 重定向到登录路由，并保留预期的目标以供身份验证后导航。

#### Scenario: Authenticated user opens public route
- **WHEN** 已认证的 user 导航到登录或注册页面
- **THEN** 路由器 MUST 将 user 重定向到聊天工作区路由

#### Scenario: Authenticated workspace is responsive
- **WHEN** 已认证的 user 在桌面或窄视口上打开工作区路由
- **THEN** 前端 MUST 渲染导航、当前路由上下文、账户控制和路由内容出口，且不会重叠或裁剪控件。

### Requirement: Shared typed frontend transport
前端 SHALL 通过共享类型客户端边界访问后端 JSON 端点和 SSE 流，并且仅消费 `@agent-py/api-contracts` 定义。

#### Scenario: Typed API request succeeds
- **WHEN** 前端功能通过 API 客户端发送经过身份验证的请求
- **THEN** 客户端 MUST 附加活动的承载令牌，解码共享响应信封，并返回类型化的响应数据。

#### Scenario: Typed API request fails
- **WHEN** 后端请求返回统一的错误响应或格式错误的 JSON 正文
- **THEN** 客户端 MUST 会暴露一个规范化的前端错误，并带有安全的 user 面消息和 MUST NOT 抛出未处理的 JSON 解析错误。

#### Scenario: SSE stream is consumed
- **WHEN** 前端功能打开 SSE 流
- **THEN** SSE 客户端 MUST 将流事件解析为共享的区分型 `SseEvent` 合同，并对无效事件有效载荷显示错误。

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
- **THEN** shell MUST 通过一致的可关闭反馈展示公开安全消息。

### Requirement: Reusable async feedback states
前端 SHALL 为所有工作区路由体验提供可重用的加载、空状态和错误展示组件。

#### Scenario: Route is loading
- **WHEN** 一个路由等待数据或初始化
- **THEN** 它在路由内容区域 MUST 渲染一个可访问的加载状态。

#### Scenario: Route has no data
- **WHEN** 路由已成功加载，但没有要显示的项目
- **THEN** 它 MUST 应使用带有上下文的下一步操作文本来呈现可访问的空状态。

#### Scenario: Route cannot load
- **WHEN** 路由请求失败
- **THEN** 它应渲染规范化的错误信息和重试提示，其中路由操作是可重复的。
