## ADDED Requirements

### Requirement: Authenticated AIOps diagnosis entry
前端 SHALL 提供一个经过身份验证的 `/aiops` 工作区，该工作区通过共享的 AIOps 合同，从必需的事件查询和可选的结构化警报对象创建 API 诊断。

#### Scenario: Operator starts a diagnosis
- **WHEN** 已认证的操作员输入一个非空的诊断查询并提交表单
- **THEN** 前端 MUST 通过后端创建诊断，选择返回的任务，并启动其类型的 SSE 执行流

#### Scenario: Operator includes alert context
- **WHEN** 操作符提供可选的警报上下文作为 JSON 对象
- **THEN** 前端 MUST 在创建任务之前将其解析为共享请求格式。

#### Scenario: Alert context is invalid
- **WHEN** 可选的警报上下文无效 JSON 或不是对象
- **THEN** 前端 MUST 阻止提交并显示清晰的本地验证消息。

### Requirement: Live evidence-backed diagnostic progress
AIOps 工作区 SHALL 将后端的通用 SSE 诊断事件作为有序的实时活动流呈现，而不会虚构步骤、工具、证据或结论。

#### Scenario: Diagnostic phase advances
- **WHEN** 后端在规划、执行、重新规划或报告时会发出 `task.status` 事件
- **THEN** 前端 MUST 按时间顺序显示返回的状态、存在的进度和消息

#### Scenario: Backend invokes a tool or retrieves a source
- **WHEN** 后端会发出 `tool.call` 或 `reference.source` 事件
- **THEN** 前端 MUST 使用返回的内容显示工具生命周期或源引用

#### Scenario: Backend produces a report or error
- **WHEN** 后端发出 `report`、`complete` 或 `error` 事件
- **THEN** 前端 MUST 显示返回的报告或标准化错误，并将所选任务与其持久化的证据链进行协调。

### Requirement: Diagnostic history and evidence chain
AIOps 工作区 SHALL 列出当前 user 的持久化诊断历史，并为选定的任务提供完整的、由服务器支持的证据链。

#### Scenario: Operator selects a prior diagnostic
- **WHEN** 一名操作员从历史记录中选择一个诊断
- **THEN** 前端通过后端加载其证据链，并渲染其任务状态、报告、执行步骤、工具审计、证据和源引用。

#### Scenario: Report links to evidence
- **WHEN** 选定的诊断报告包含证据链接  
- **THEN** 前端 MUST 将报告和相应的持久化证据标识符一起显示。

#### Scenario: History request fails
- **WHEN** 历史记录或证据链请求返回标准化的后端错误
- **THEN** 前端 MUST 显示安全错误，MUST NOT 作为成功当前结果显示过时数据。

### Requirement: Responsive operational diagnosis workspace
AIOps 工作区 SHALL 在桌面和窄视口宽度下，应保持事件条目、历史记录、实时进展、报告和证据控制的可读性和可操作性。

#### Scenario: Operator uses a narrow screen
- **WHEN** 在窄视口上显示工作区
- **THEN** 其任务控件、时间线、报告和证据链 MUST 会重新排列，而不会出现水平页面溢出。
