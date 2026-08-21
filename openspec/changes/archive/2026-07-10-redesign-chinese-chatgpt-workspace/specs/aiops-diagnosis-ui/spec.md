## MODIFIED Requirements

### Requirement: Authenticated AIOps diagnosis entry
前端 SHALL 提供一个经过身份验证的中文 `/aiops` 工作区，该工作区通过从必需的事件查询和可选的结构化警报对象共享的 AIOps 合同创建 API 诊断。

#### Scenario: Operator starts a diagnosis
- **WHEN** 已认证的操作员输入非空的诊断查询并提交表单
- **THEN** 前端 MUST 通过后端创建诊断，选择返回的任务，启动其类型的 SSE 执行流，并显示中文的准备中或运行中状态。

#### Scenario: Operator includes alert context
- **WHEN** 操作符提供可选的警报上下文作为 JSON 对象
- **THEN** 前端 MUST 在创建任务之前将其解析为共享请求结构。

#### Scenario: Alert context is invalid
- **WHEN** 可选的警报上下文无效 JSON 或不是对象
- **THEN** 前端 MUST 阻止提交并显示清晰的中文本地验证消息。

### Requirement: Live evidence-backed diagnostic progress
AIOps 工作区 SHALL 将后端的通用 SSE 诊断事件作为有序的实时中文活动流呈现，而不添加步骤、工具、证据、进展或结论。

#### Scenario: Diagnostic phase advances
- **WHEN** 后端在规划、执行、重新规划或报告时会发出 `task.status` 事件
- **THEN** 前端 MUST 按照时间顺序显示返回的状态、进度（如果存在）和消息，并带有中文生命周期标签。

#### Scenario: Backend invokes a tool or retrieves a source
- **WHEN** 后端会发出 `tool.call` 或 `reference.source` 事件
- **THEN** 前端 MUST 使用返回内容在可展开的上下文区域中显示工具生命周期或来源引用。

#### Scenario: Backend produces a report or error
- **WHEN** 后端发出 `report`、`complete` 或 `error` 事件
- **THEN** 前端 MUST 显示返回的报告或规范化的中文错误，并将所选任务与其持久化的证据链进行协调

### Requirement: Responsive operational diagnosis workspace
AIOps 工作区 SHALL 保持中文事件条目、历史记录、实时进展、报告和证据控制在桌面和窄视口宽度下可读且可操作。

#### Scenario: Operator uses a narrow screen
- **WHEN** 在窄视口上显示工作区
- **THEN** 其任务控件、中文状态标签、时间线、报告和证据链 MUST 会重新排列，而不会出现水平页面溢出。
