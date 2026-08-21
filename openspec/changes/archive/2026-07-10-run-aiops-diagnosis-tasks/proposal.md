## Why

该项目可以持久化 AIOps 诊断记录并描述 API 表面，但尚未运行基于证据的诊断工作流。操作员需要一个持久的、tenant 范围内的诊断，将警报和真实的 CLS 证据转化为透明报告，而不是接受一个没有执行的任务。

## 什么更改

- 在经过身份验证的AIOps APIs后面添加一个LangGraph `Planner -> Executor -> Replanner -> Report`诊断流程。
- 要求Planner在规划之前检索相关的知识库SOPs；当没有SOP匹配时，明确显示并报告回退情况。
- 仅执行已注册的本地工具和真实的MCP工具，通过共享的SSE合同流式传输计划和执行进度，并持久化任务状态、证据、工具审计、checkpoints和报告。
- 通过共享的API合同暴露诊断流和报告数据，同时保留tenant隔离和显式的集成失败。

## 功能

### 新功能
- `aiops-diagnosis-tasks`: 基于证据的、tenant 范围内的计划-执行-重规划诊断和最终报告。

### 修改的功能
- `api-and-sse-contracts`: 定义AIOps诊断请求、持久化结果和流式处理生命周期契约。
- `agent-tool-call-audits`: 将持久化工具调用审核扩展到AIOps诊断执行。
- `real-mcp-tools`: 允许AIOps执行器显式调用发现的真实MCP工具。

## 影响

影响的区域包括 FastAPI AIOps 端点、共享的 API 合同、LangGraph 和 LangChain 依赖项、SQLite 诊断存储库、MCP 工具适配器、检索集成、SSE 序列化、后端测试以及 Vue 受保护数据客户端状态。
