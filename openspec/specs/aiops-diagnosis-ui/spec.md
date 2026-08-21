# AIOps Diagnosis UI Specification

## Purpose

为启动真实流式Vue诊断并检查其服务器持久化报告和证据链定义经过身份验证的Vue工作区。
## Requirements
### Requirement: Authenticated AIOps diagnosis entry
前端 SHALL 提供一个经过身份验证的中文 `/aiops` 工作区，该工作区通过共享的 AIOps 合同从必需的事件查询和可选的结构化警报对象创建 API 诊断。

#### Scenario: Operator starts a diagnosis
- **WHEN** 已认证的操作员输入一个非空的诊断查询并提交表单
- **THEN** 前端 MUST 通过后端创建诊断，选择返回的任务，启动其类型的 SSE 执行流，并显示中文的准备中或运行中状态。

#### Scenario: Operator includes alert context
- **WHEN** 一个操作符提供可选的警报上下文作为 JSON 对象
- **THEN** 前端 MUST 在创建任务之前将其解析为共享请求格式。

#### Scenario: Alert context is invalid
- **WHEN** 可选的警报上下文无效 JSON 或不是对象
- **THEN** 前端 MUST 阻止提交并显示清晰的中文本地验证消息。

### Requirement: Live evidence-backed diagnostic progress
AIOps 工作区 SHALL 将后端的通用 SSE 诊断事件作为有序的实时中文活动流呈现，而不添加步骤、工具、证据、进展或结论。

#### Scenario: Diagnostic phase advances
- **WHEN** 后端在规划、执行、重新规划或报告时会发出 `task.status` 事件  
- **THEN** 前端 MUST 按照时间顺序显示返回的状态、存在的进度以及消息，并带有中文生命周期标签。

#### Scenario: Backend invokes a tool or retrieves a source
- **WHEN** 后端会发出 `tool.call` 或 `reference.source` 事件
- **THEN** 前端 MUST 使用返回内容在可展开的上下文区域中显示工具生命周期或源引用。

#### Scenario: Backend produces a report or error
- **WHEN** 后端发出 `report`、`complete` 或 `error` 事件  
- **THEN** 前端 MUST 显示返回的报告或规范化的中文错误，并将所选任务与其持久化的证据链进行协调。

### Requirement: Diagnostic history and evidence chain
AIOps 工作区 SHALL 列出当前 user 的持久化诊断历史，并为选定任务公开完整的、由服务器支持的证据链。

#### Scenario: Operator selects a prior diagnostic
- **WHEN** 一个操作员从历史记录中选择一个诊断
- **THEN** 前端 MUST 通过后端加载其证据链，并渲染其任务状态、报告、执行步骤、工具审计、证据和源引用。

#### Scenario: Report links to evidence
- **WHEN** 选定的诊断报告包含证据链接  
- **THEN** 前端 MUST 会将报告和相应的持久化证据标识符一起显示。

#### Scenario: History request fails
- **WHEN** 一个历史或证据链请求返回标准化的后端错误
- **THEN** 前端 MUST 显示安全错误，MUST NOT 作为成功当前结果显示过时数据。

### Requirement: Responsive operational diagnosis workspace
AIOps 工作区 SHALL 保持中文事件条目、历史记录、实时进展、报告和证据控制在桌面和窄视口宽度下可读且可操作。

#### Scenario: Operator uses a narrow screen
- **WHEN** 在窄视口上显示工作区
- **THEN** 其任务控件、中文状态标签、时间线、报告和证据链 MUST 会重新布局，而不会出现水平页面溢出。

### Requirement: Professional Chinese AIOps console presentation
AIOps 工作区 SHALL 使用专业的中文 AI 运维诊断控制台布局，突出任务输入、实时诊断、证据链、最终报告和历史任务，并保持与 ChatGPT 网页式对话工作台一致的克制视觉语言。

#### Scenario: Operator opens the diagnosis workspace
- **WHEN** 已认证的 operator 打开 `/aiops`
- **THEN** 前端 MUST 显示中文的诊断输入区、实时诊断时间线、证据/报告区和历史/告警入口，并以清晰状态标签区分等待中、执行中、成功和失败。

#### Scenario: Diagnostic task is running
- **WHEN** AIOps 诊断任务正在等待、规划、执行、重规划或生成报告
- **THEN** 前端 MUST 在主工作区显示可见的运行状态，而不是只依赖按钮禁用或空白区域表达进度。

#### Scenario: Operator reviews evidence and report
- **WHEN** 一个诊断任务包含证据链、工具调用、引用或最终报告
- **THEN** 前端 MUST 将证据和报告放在可扫描的中文区域中展示，并保留来源、时间和状态信息。

#### Scenario: Responsive diagnosis workspace
- **WHEN** AIOps 工作区在窄视口中显示
- **THEN** 输入、时间线、证据、报告和历史区域 MUST 重新排列为单列或可读的纵向结构，MUST NOT 出现横向页面溢出。

### Requirement: Centered persistent diagnostic report
AIOps 工作区 SHALL 在中间主区域将实时诊断过程和最终持久化报告组织为连续的诊断主叙事，并在任务完成后将报告作为主要阅读内容展示。

#### Scenario: Diagnosis is still running
- **WHEN** Planner、Executor、Replanner 或 Report 节点仍在执行
- **THEN** 中间区域 MUST 显示当前过程和报告等待/生成状态，MUST NOT 留下无法解释的空白区域

#### Scenario: Live report arrives
- **WHEN** SSE 流收到 `report` 事件但持久化证据链尚未回载
- **THEN** 中间区域 MUST 立即显示该 Markdown 报告

#### Scenario: Persisted diagnosis is selected
- **WHEN** 操作员选择包含一个或多个持久化报告的历史诊断
- **THEN** 中间区域 MUST 显示最新报告的标题、生成时间和完整 Markdown 正文

### Requirement: Readable long-form Markdown report
最终诊断报告 SHALL 使用适合中文长文阅读的层级、间距和数据表格样式，并限制溢出范围。

#### Scenario: Report contains headings, lists and tables
- **WHEN** Markdown 报告包含多级标题、分隔线、列表、代码或表格
- **THEN** 前端 MUST 以清晰层级和足够对比度渲染内容，且表格 MUST 在自身区域滚动而不导致页面水平溢出

#### Scenario: Report is viewed on a narrow screen
- **WHEN** 报告在窄视口中展示
- **THEN** 报告正文、元数据和操作区域 MUST 纵向重排并保持可读，页面 MUST NOT 水平溢出

### Requirement: Compact AIOps execution chain presentation
AIOps 工作区右栏 SHALL 以持久化 Planner、Executor 和 Replanner 步骤构成紧凑执行链，并将工具调用作为独立的可折叠列表展示。

#### Scenario: Persisted steps are available
- **WHEN** 选中诊断包含 Planner、Executor 或 Replanner 步骤
- **THEN** 右栏 MUST 按执行顺序显示每一步的一句话中文标题和缩进输出，MUST NOT 显示独立原始 evidence 列表

#### Scenario: Tool calls are available
- **WHEN** 选中诊断包含工具调用审计
- **THEN** 右栏 MUST 默认只显示工具名和状态，工具输出 MUST 位于默认收起的缩进详情框中

#### Scenario: Tool output contains structured records
- **WHEN** 工具结果摘要包含 SearchLog records、知识检索结果或其他 JSON 结构
- **THEN** 前端 MUST 将其转换为有限的可读文本摘要，MUST NOT 直接展示 JSON 字符串、原始 payload 或证据 ID

#### Scenario: Live tool event arrives
- **WHEN** 实时时间线收到包含 output 的 `tool.call` 事件
- **THEN** 时间线 MUST 只展示工具生命周期和状态，MUST NOT 重复展示工具输出正文

### Requirement: Long reports scroll inside the fixed diagnosis workspace
智能诊断桌面工作区 SHALL 保持受桌面视口约束的固定高度，最终报告过长时 MUST 在报告正文区域内部纵向滚动，不得继续撑高整个浏览器页面。

#### Scenario: Persisted report exceeds the available center height
- **WHEN** user 打开内容高度超过最终报告可用区域的历史诊断报告
- **THEN** AIOps 工作区外框 MUST 保持固定高度，报告标题和元信息 MUST 保持可见，Markdown 正文 MUST 提供独立纵向滚动条

#### Scenario: Other diagnosis columns contain long content
- **WHEN** 左侧历史、诊断过程或右侧执行链超过各自可用高度
- **THEN** 对应栏 MUST 在工作区内部滚动且 MUST NOT 增加页面文档高度

### Requirement: Diagnostic step and report feedback
AIOps 工作区 SHALL 允许用户评价执行步骤和最终报告，并支持附加问题说明或纠正内容。

#### Scenario: 用户评价报告
- **WHEN** 用户提交报告反馈
- **THEN** 状态 MUST 立即显示为已保存且历史任务重新打开后仍可恢复。
