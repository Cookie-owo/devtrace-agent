## ADDED Requirements

### Requirement: Aggregate secret-safe readiness check
后端 SHALL 暴露一个类型化的 `/readiness` 端点，该端点报告 Milvus、LLM 提供商和本地 MCP 的可用性，而不会暴露凭据。

#### Scenario: All required dependencies are ready
- **WHEN** Milvus，配置的 LLM 提供商以及配置的 MCP 服务器可用
- **THEN** `/readiness` MUST 在可用时返回成功的 ready 结果，并包含安全组件元数据和延迟或工具计数信息

#### Scenario: A dependency is unavailable
- **WHEN** 一个或多个必需的依赖项无法完成其 readiness 检查  
- **THEN** `/readiness` MUST 将返回降级结果，每个受影响的组件返回一个安全错误，并且 HTTP 状态不为成功

#### Scenario: 结果包含提供者配置上下文
- **WHEN** `/readiness` 包含 LLM 配置上下文
- **THEN** 它 MUST 仅包含安全的提供者/模型/基础 URL 信息，而 MUST NOT 包含一个 API 键或其他密钥。

### Requirement: Live lightweight workspace connectivity
前端 SHALL 在工作区挂载时获取轻量级后端 health，并从该结果中渲染标题栏的连接状态。

#### Scenario: Backend health succeeds
- **WHEN** 前端可以检索轻量级 health 端点
- **THEN** 工作区标题 MUST 渲染连接状态。

#### Scenario: Backend health fails
- **WHEN** 前端无法获取成功的轻量级 health 响应
- **THEN** 工作区标题 MUST 在渲染降级状态时不会阻止已认证的工作区路由加载。
