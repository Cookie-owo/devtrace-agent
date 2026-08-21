## ADDED Requirements

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
- **THEN** 后端 MUST 仅返回该 user 的任务，并按最近创建时间排序

#### Scenario: User reads complete evidence chain
- **WHEN** 已认证的 user 请求他们拥有的诊断证据链
- **THEN** 后端 MUST 返回任务、输入、有序步骤、工具调用、类型化证据、报告来源和最终报告。

#### Scenario: Cross-tenant evidence access is denied
- **WHEN** 请求另一个 user 的诊断历史或证据链
- **THEN** 后端 MUST 返回统一的授权错误，而不暴露诊断工件。
