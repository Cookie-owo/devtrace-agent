## ADDED Requirements

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
