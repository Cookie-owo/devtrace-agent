## Why

当前 AIOps 最终报告虽已持久化，但完整内容被放在右侧证据栏，并且后端只拼接固定英文摘要，没有使用模型基于真实告警与工具证据生成可读的中文诊断报告。运维人员难以在主工作区找到正式结论，也无法快速扫描告警清单、根因、处置建议和风险。

## What Changes

- Report 节点使用 LLM 根据诊断输入、告警上下文、SOP、执行计划和真实工具证据生成纯 Markdown 中文报告。
- 报告严格采用“活跃告警清单、逐告警根因分析、处理方案执行、结论与风险评估”的固定结构。
- 明确禁止编造；工具失败、无告警、无 SOP 或证据不足时必须在对应章节如实说明。
- LLM 报告生成失败时使用中文结构化 Markdown 回退报告，仍保留已有证据和失败情况。
- 将选中任务的持久化最终报告放到 AIOps 中间主区域，右侧保留证据、工具调用和案例，不再重复渲染完整报告。
- 增强 Markdown 标题、列表、分隔线和表格样式，保证桌面与窄屏可读。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `aiops-diagnosis-tasks`: Report 节点生成证据约束的统一中文 Markdown 告警分析报告。
- `aiops-diagnosis-ui`: 最终报告在中间主区域沉淀并以适合长文阅读的格式展示。
- `aiops-evidence-chain`: 右侧证据链聚焦报告来源、证据与工具调用，不重复展示完整报告正文。

## Impact

- 后端 AIOps LangGraph Report 节点、Prompt 和安全回退逻辑。
- 前端 AIOps 主布局、报告组件、证据链组件与 Markdown 样式。
- 后端与前端测试；不改变现有 API 和 SSE 事件结构。
