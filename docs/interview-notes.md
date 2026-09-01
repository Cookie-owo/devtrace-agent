# DevPilot Interview Notes

## 高频问题与回答思路

1. **为什么用 Agent？** 研发故障排查需要动态决定先看日志、提交还是源码，固定规则难以覆盖上下文组合；Agent 负责规划，工具负责可控执行。
2. **为什么用 LangGraph？** 需要显式状态、节点边界、重规划、预算和可观测 Trace，LangGraph 比单轮 ReAct 更适合长流程。
3. **ReAct 与 Plan-Execute-Replan 的区别？** ReAct 边想边做；本项目先形成计划，执行后根据 Evidence 缺口重规划，更容易限制预算和审计。
4. **如何做 Tool Calling？** Tool 使用统一 DeveloperTool Protocol 和 ToolResult，Executor 负责超时、错误规范化、审计和预算。
5. **MCP 的作用？** MCP 接入外部工具能力；真实连接由用户启用，应用保留超时、重试、同名保护和审计。
6. **RAG 在哪里？** Knowledge 场景沿用 Milvus、BM25/RRF/rerank；Golden CI Case 第一版刻意不引入 Knowledge Retrieval，减少变量。
7. **什么是 Evidence Grounding？** confirmed 结论必须绑定真实 Evidence IDs，并通过多个独立类型和一致性 Verifier。
8. **如何避免死循环？** max steps、max tool calls、重复调用限制、单工具 timeout、总 timeout 和 Replanner 边界。
9. **Timeout 怎么处理？** Tool 层统一转为 ToolResult error，Workflow 记录失败并安全结束或有限重规划。
10. **Retry 与 Idempotency？** BackgroundJob 有 lease/retry；已完成 Task 不重复执行，Case/Evidence/Report 按持久化状态跳过。
11. **Context 与 Memory？** Task State 保存当前诊断上下文；持久层保存 Task、Step、ToolCall、Evidence、Report，避免只依赖内存上下文。
12. **如何评测 Agent？** 固定 Dataset 批量执行真实 Workflow，规则优先计算根因、确认、工具、证据、延迟和失败率。
13. **Fault Injection 做什么？** 注入 tool failure、timeout、empty result、budget exhaustion，验证 Agent 是否克制、安全结束。
14. **为什么 Safe Test Runner 不允许 Bash？** 任意 Shell 会带来任意代码执行和数据访问风险，第一版只允许白名单测试入口。
15. **如何保证测试路径安全？** WorkspaceGuard 校验仓库和相对测试路径，禁止绝对路径和目录穿越。
16. **Patch 如何保证安全？** Patch 是结构化替换，不接受任意写文件；文件必须在 allowlist，应用在临时副本。
17. **为什么不直接改真实仓库？** 诊断和修复必须可回滚、可审计，用户应先查看 Patch 再决定是否应用。
18. **BackgroundJob 为什么必要？** Agent 诊断、Evaluation 和 Repair 都可能超时，后台任务支持 lease、恢复、取消和重试。
19. **SSE 解决什么问题？** 将持久化任务进展实时推送到前端；先保存状态再发事件，避免前端看到不可查询的数据。
20. **多租户如何隔离？** 身份来自认证上下文，查询同时使用 owner/tenant scope，不信任客户端提交的 owner/tenant。
21. **项目最难的问题？** 不是调用模型，而是把结论、工具、证据、预算和后台任务做成可追踪系统。
22. **为什么先做具体 CI Domain？** AIOps 与 CI 的真实实现不同，先跑通垂直闭环，再根据共性抽象，避免过早 Universal Diagnosis。
23. **为什么 Failure Analyzer 先用规则？** HTTP 状态码、字段缺失和测试名结构稳定，规则可解释；LLM 只作为结构化解析失败时的 fallback。
24. **如何判断证据冲突？** Verifier 分离 supporting/contradicting Evidence，不把冲突数据直接升级为 confirmed。
25. **如何控制成本？** 记录 tool calls、steps、latency、token usage（可用时），并通过 Evaluation 比较 Prompt/Workflow 版本。
26. **MCP 与本地 Tool 如何统一？** 两者都适配到受控工具边界，统一超时、错误、审计和结果结构。
27. **为什么不让 Agent 自动 Commit/PR？** 代码修改属于高风险外部状态变化，Milestone 4 只输出可审计 Patch，不自动提交。
28. **如何处理 Worker 崩溃？** Job 状态、lease 和持久化结果让恢复逻辑可以重新 claim；已完成任务通过幂等检查跳过。
29. **当前 Trade-off？** 牺牲部分通用修复能力换取可解释、安全和可测试；牺牲即时复杂 Dashboard 换取稳定的核心闭环。
30. **项目还有什么限制？** 线上真实数据、并发压力、P95/P99、长期模型稳定性和完整 crash recovery 基准仍需持续补充。
