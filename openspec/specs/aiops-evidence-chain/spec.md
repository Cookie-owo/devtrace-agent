# aiops-evidence-chain Specification

## Purpose

定义持久化、owner 范围内的 AIOps 诊断证据、执行制品、报告来源和查询行为。
## Requirements
### Requirement: Typed diagnostic evidence is persisted
后端 SHALL 会保留每个 AIOps 诊断的 owner 范围内的证据记录，包括当这些证据源生成时的日志、指标、警报、工单和知识库引用。

#### Scenario: Tool log evidence is stored
- **WHEN** 诊断 Executor 接收真实的 CLS 日志结果
- **THEN** 后端 MUST 使用诊断任务 ID、生成步骤、工具调用关联、源元数据、摘要和原始结果负载存储日志证据记录。

#### Scenario: Knowledge evidence is stored
- **WHEN** Planner 获取一个 SOP 或事件文档引用
- **THEN** 后端 MUST 存储一个包含稳定 chunk、文档和知识库身份的知识引用证据记录。

#### Scenario: Alert input is stored as evidence
- **WHEN** 创建一个诊断，使用警报输入
- **THEN** 后端 MUST 在任务 owner 范围内存储一个保留原始警报有效负载的警报证据记录。

### Requirement: Diagnostic execution steps are persisted
后端 SHALL 保留有序的 Planner、Executor、Replanner 和 Report 步骤记录，每个诊断任务的状态和结构化负载。

#### Scenario: Plan and execution steps can be read
- **WHEN** 诊断完成或失败
- **THEN** 授权调用者 MUST 能够按时间顺序读取持久化的计划和执行步骤序列。

### Requirement: Report provenance is durable
后端 SHALL 会保留每个最终诊断报告与该报告所使用的证据记录之间的显式链接。

#### Scenario: Report evidence is resolvable
- **WHEN** 授权调用者读取诊断报告的来源
- **THEN** 每个关联的证据 ID MUST 都必须解析为由同一 user 和诊断任务拥有的证据记录。

### Requirement: Diagnostic history and evidence chain are owner scoped
后端 SHALL 提供经过身份验证的历史记录和完整的证据链查询，可根据当前 user 过滤所有任务、步骤、审计、证据、报告、链接和 checkpoint。

#### Scenario: User lists diagnostic history
- **WHEN** 已认证的 user 请求诊断历史记录，可选时间范围
- **THEN** 后端 MUST 仅返回该 user 的任务，并按最近创建时间排序。

#### Scenario: User reads complete evidence chain
- **WHEN** 身份验证过的 user 请求他们拥有的诊断证据链
- **THEN** 后端 MUST 返回任务、输入、有序步骤、工具调用、类型化证据、报告来源和最终报告。

#### Scenario: Cross-tenant evidence access is denied
- **WHEN** 请求另一个 user 的诊断历史或证据链
- **THEN** 后端 MUST 返回统一的授权错误，不暴露诊断工件。

### Requirement: Evidence sidebar avoids duplicate report body
右侧证据链 SHALL 聚焦最终报告的来源关系、真实证据、工具调用和诊断案例，并 MUST NOT 与中间主区域重复渲染完整报告正文。

#### Scenario: Persisted report has linked evidence
- **WHEN** 选中诊断的报告关联一个或多个证据记录
- **THEN** 右侧 MUST 展示报告标题、生成时间和关联证据标识，同时将完整报告正文保留在中间主区域

#### Scenario: No report has been persisted
- **WHEN** 选中任务尚未生成报告
- **THEN** 右侧 MUST 明确显示报告尚未生成，并继续展示已经存在的证据和工具调用

### Requirement: Operator-facing evidence is an execution trace
前端 SHALL 将 operator 可见的诊断证据链限定为 Planner、Executor、Replanner 的持久化执行步骤以及关联工具调用审计，而后端仍可保留完整原始 evidence 供持久化和报告追溯。

#### Scenario: Operator reviews the right sidebar
- **WHEN** operator 查看一个已有完整证据链的诊断任务
- **THEN** 界面 MUST 聚焦执行步骤标题、步骤输出、工具名和工具结果摘要，MUST NOT 渲染原始 evidence summary、payload、记录 ID 或报告证据链接

#### Scenario: Tool details are collapsed
- **WHEN** operator 尚未主动展开某个工具调用
- **THEN** 该工具的参数和结果内容 MUST 保持隐藏，仅显示工具名称和状态

#### Scenario: Operator expands a tool
- **WHEN** operator 展开某个工具调用
- **THEN** 界面 MUST 在缩进容器中展示经过长度限制和语义格式化的结果，并保持页面无水平溢出
