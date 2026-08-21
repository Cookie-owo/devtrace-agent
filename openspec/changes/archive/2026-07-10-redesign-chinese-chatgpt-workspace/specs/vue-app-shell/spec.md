## MODIFIED Requirements

### Requirement: Route-based application shell
前端 SHALL 通过 Vue Router 暴露公开的登录和注册路由以及经过身份验证的聊天、知识和 AIOps 工作区路由。经过身份验证的路由 SHALL 将渲染中文导航、中文路由上下文、账户控制以及专注的 AI- 工作区外壳。

#### Scenario: Anonymous user opens protected route
- **WHEN** 未认证的访客直接导航到工作区路由  
- **THEN** 路由器 MUST 重定向到登录路由，并保留预期的目标以供认证后导航。

#### Scenario: Authenticated user opens public route
- **WHEN** 已认证的 user 导航到登录或注册页面
- **THEN** 路由器 MUST 将 user 重定向到聊天工作区路由

#### Scenario: Authenticated workspace is responsive
- **WHEN** 已认证的 user 在桌面或窄视口上打开工作区路由
- **THEN** 前端 MUST 渲染中文导航、活动路由上下文、账户控制和路由内容出口，且不重叠、裁剪或出现水平页面溢出。

### Requirement: Reusable async feedback states
前端 SHALL 为所有工作区路由体验提供可重用的中文加载、空状态、错误和任务状态展示组件。

#### Scenario: Route is loading
- **WHEN** 一个路由等待数据或初始化
- **THEN** 它 MUST 在路由内容区域中呈现可访问的中文加载状态。

#### Scenario: Route has no data
- **WHEN** 路由已成功加载，但没有要显示的项目
- **THEN** 它 MUST 应渲染一个可访问的中文空状态，并带有上下文相关的下一步操作文本。

#### Scenario: Route cannot load
- **WHEN** 路由请求失败  
- **THEN** 它应渲染规范化的错误信息和中文重试提示，其中路由操作是可重复的。

#### Scenario: Task state changes
- **WHEN** 一个工作区接收到现有的异步任务状态
- **THEN** 它 MUST 将渲染共享的基于文本的中文生命周期处理，而不是单独的未翻译原始状态。
