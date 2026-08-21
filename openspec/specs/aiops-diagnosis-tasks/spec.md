# aiops-diagnosis-tasks Specification

## Purpose

使用基于证据的、tenant 范围的 AIOps 诊断，通过 LangGraph 计划-执行-重新计划工作流和共享流式协议。
## Requirements
### Requirement: Plan-Execute-Replan diagnostic graph
后端 SHALL 通过具有命名 `Planner`、`Executor`、`Replanner` 和 `Report` 节点的 LangGraph 工作流执行每个经过身份验证的 AIOps 诊断。

#### Scenario: Diagnostic follows the graph lifecycle
- **WHEN** 已认证的 user 启动诊断任务  
- **THEN** 后端 MUST 将任务保存为运行中，并在终端成功或失败前执行 Planner、Executor、Replanner 和 Report 节点。

#### Scenario: Replanner continues only when warranted
- **WHEN** Executor 返回需要其他限定诊断步骤的证据
- **THEN** Replanner MUST 调整计划并返回到 Executor；否则它 MUST 返回到 Report。

### Requirement: SOP-first diagnostic planning
在创建诊断计划之前，Planner SHALL 需要检索 tenant 授权的 SOP 或事件文档证据。

#### Scenario: Matching SOP informs plan
- **WHEN** 知识检索返回一个或多个 SOP 结果  
- **THEN** 计划和报告 MUST 识别已检索到的证据并优先推荐诊断操作。

#### Scenario: No SOP match is explicit
- **WHEN** 知识检索未返回任何结果  
- **THEN** 诊断 SSE 生命周期和最终报告 MUST 明确指出没有 SOP 匹配，并且该计划是通用的。

### Requirement: Evidence-based execution and reporting
Executor SHALL 仅调用真实注册的 MCP 工具、tenant 范围的知识检索工具或本地确定性工具，并且 Report 节点 SHALL 仅基于返回的证据得出结论。

#### Scenario: Real MCP evidence is used
- **WHEN** 诊断计划调用 CLS MCP 工具
- **THEN** Executor MUST 调用本地 MCP 服务器，并在其诊断证据中包含实际结果或明确的失败信息。

#### Scenario: 不支持的证据无法得出结论
- **WHEN** 执行没有用于可能结论的支持工具或检索证据
- **THEN** 报告 MUST 将该结论标记为未验证，而不是编造它。

### Requirement: Diagnostic persistence and ownership
后端 SHALL 通过 owner 范围的存储库边界保留诊断状态、计划、执行证据、节点 checkpoints、报告和工具审计。

#### Scenario: Diagnostic artifacts are owner scoped
- **WHEN** 一个 user 读取或流式传输诊断任务
- **THEN** 后端 MUST 仅公开该 user 拥有的任务、checkpoint、报告和审计。

#### Scenario: Terminal task is persisted
- **WHEN** 诊断完成或失败  
- **THEN** 任务状态、结果负载、完成时间戳以及任何报告 MUST 必须在 SQLite 中持久化。

### Requirement: Diagnostic SSE lifecycle
AIOps 诊断 SHALL 由持久化后台任务执行，并将计划、步骤、工具、重规划、报告、完成和错误事件持久化后通过 SSE 订阅返回。

#### Scenario: Diagnostic stream disconnects
- **WHEN** 用户在诊断期间关闭或刷新页面
- **THEN** 诊断 MUST 继续执行，重新打开任务 MUST 能恢复事件和最终证据链。

### Requirement: Diagnostic workflow writes evidence-chain records
LangGraph Planner、Executor、Replanner 和 Report 节点 SHALL 通过诊断证据链存储库边界持续保留其计划、执行、证据和报告的来源信息。

#### Scenario: Workflow persists node artifacts
- **WHEN** 诊断在图节点中进行
- **THEN** 节点 MUST 存储有序的步骤记录以及在最终报告发出前生成的任何证据。

### Requirement: Alert provenance is retained by a diagnostic task
后端 SHALL 保留从活动警报源中选择的警报的标准化源身份和原始上下文，这些警报来自持久化诊断输入、证据链、流式生命周期和最终报告输入。

#### Scenario: Operator diagnoses an alert from a configured source
- **WHEN** 已认证的操作员从标准化的主动警报中启动 AIOps 诊断
- **THEN** 持久化的诊断输入和初始警报证据 MUST 包括所选的源身份和原始提供者上下文，以及标准化的警报字段。

### Requirement: Structured Chinese alert analysis report
Report 节点 SHALL 基于诊断输入、告警上下文、SOP、执行计划和真实工具证据生成纯 Markdown 中文告警分析报告，并按照活跃告警清单、逐告警根因分析、处理方案执行、整体结论和风险评估的顺序组织内容。

#### Scenario: Evidence supports one or more active alerts
- **WHEN** Report 节点收到一个或多个真实活跃告警及对应工具证据
- **THEN** 最终报告 MUST 包含告警清单表格，并为每个告警分别展示详情、症状、日志证据、根因结论、排查步骤、处理建议和预期效果

#### Scenario: Evidence is missing or a tool fails
- **WHEN** 某个字段、SOP、日志证据或工具结果缺失或失败
- **THEN** 报告 MUST 在对应章节明确写出“未获取”“证据不足”或失败原因，MUST NOT 编造告警、日志、根因或执行结果

#### Scenario: Report model invocation fails
- **WHEN** LLM 报告生成调用失败、返回空内容或返回非 Markdown 结构
- **THEN** Report 节点 MUST 生成并持久化结构化中文 Markdown 回退报告，并如实保留已有证据和失败状态

#### Scenario: Report output remains plain Markdown
- **WHEN** Report 节点完成报告生成
- **THEN** 持久化内容和 SSE `report` 事件 MUST 包含纯 Markdown 文本，MUST NOT 包含 JSON 报告对象或包裹全文的代码围栏
