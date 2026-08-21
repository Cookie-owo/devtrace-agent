## ADDED Requirements

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
