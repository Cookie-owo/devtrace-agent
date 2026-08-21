## ADDED Requirements

### Requirement: Plan-Execute-Replan diagnostic graph
后端 SHALL 通过带有命名的 LangGraph 工作流，对每个经过身份验证的 AIOps 诊断进行执行，其中包括 `Planner`、`Executor`、`Replanner` 和 `Report` 节点。

#### Scenario: Diagnostic follows the graph lifecycle
- **WHEN** 已认证的 user 启动诊断任务  
- **THEN** 后端 MUST 将任务保存为运行中，并在终端成功或失败前执行 Planner、Executor、Replanner 和 Report 节点。

#### Scenario: Replanner continues only when warranted
- **WHEN** Executor 返回需要进行其他限定诊断步骤的证据
- **THEN** Replanner MUST 调整计划并返回到 Executor；否则它 MUST 返回到 Report。

### Requirement: SOP-first diagnostic planning
在创建诊断计划之前，Planner SHALL 必须检索 tenant 授权的 SOP 或事件文档证据。

#### Scenario: Matching SOP informs plan
- **WHEN** 知识检索返回一个或多个 SOP 结果  
- **THEN** 计划和报告 MUST 识别检索到的证据并优先推荐诊断操作。

#### Scenario: No SOP match is explicit
- **WHEN** 知识检索返回无结果
- **THEN** 诊断 SSE 生命周期和最终报告 MUST 明确指出没有 SOP 匹配，并且该计划是通用的。

### Requirement: Evidence-based execution and reporting
Executor SHALL 仅调用真实注册的 MCP 工具，tenant 范围的知识检索工具，或本地确定性工具，并且 Report 节点 SHALL 仅基于返回的证据得出结论。

#### Scenario: Real MCP evidence is used
- **WHEN** 诊断计划调用 CLS MCP 工具
- **THEN** Executor MUST 调用本地 MCP 服务器，并在其诊断证据中包含其实际结果或显式失败。

#### Scenario: 不支持的证据无法得出结论
- **WHEN** 执行没有支持工具或检索证据来得出可能的结论
- **THEN** 报告 MUST 将该结论标记为未验证，而不是凭空捏造。

### Requirement: Diagnostic persistence and ownership
后端 SHALL 通过 owner 范围的仓库边界保留诊断状态、计划、执行证据、节点 checkpoints、报告和工具审核。

#### Scenario: Diagnostic artifacts are owner scoped
- **WHEN** 一个 user 读取或流式传输诊断任务
- **THEN** 后端 MUST 仅公开该 user 拥有的任务、checkpoint、报告和审计记录

#### Scenario: Terminal task is persisted
- **WHEN** 诊断完成或失败  
- **THEN** 任务状态、结果负载、完成时间戳以及任何报告 MUST 应在 SQLite 中持久化。

### Requirement: Diagnostic SSE lifecycle
经过身份验证的诊断流 SHALL 按照执行顺序发出共享任务状态、工具调用、参考源、报告、完成和错误事件。

#### Scenario: Progress is streamed
- **WHEN** Planner，Executor，Replanner 或 Report 会推进诊断
- **THEN** 客户端 MUST 会接收到一个任务状态事件，描述当前的图阶段。

#### Scenario: Report is streamed before completion
- **WHEN** Report 生成最终的诊断报告
- **THEN** 客户端 MUST 收到一个报告事件，随后收到一个包含已保存诊断结果的完整事件。
