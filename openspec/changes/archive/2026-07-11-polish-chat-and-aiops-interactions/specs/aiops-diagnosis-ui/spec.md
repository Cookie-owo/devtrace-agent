## ADDED Requirements

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
