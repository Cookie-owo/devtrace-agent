# DevPilot：面向软件研发与测试的 AI Agent 工作台

## 项目定位

DevPilot 是一个面向软件研发、测试与运维场景的本地优先 AI Agent 工作台。它将传统 AIOps 的日志诊断能力扩展到 CI/Test Failure Diagnosis：Agent 读取测试日志、Git 变更和源码，构建可追溯证据链，输出根因报告，并在用户明确触发后，在隔离工作区中生成受控 Patch、运行白名单测试完成验证。

项目解决的核心痛点是：研发故障信息分散在 CI 日志、提交记录、源码和知识库中；人工排查耗时且结论难以复现；普通 LLM Agent 容易无证据下结论、重复调用工具或执行越权命令。

## 技术架构

```text
Vue 3 / TypeScript
        ↓ HTTP / SSE
FastAPI API + Auth/Tenant
        ↓
BackgroundJobRuntime
        ↓
LangGraph CI Diagnosis Workflow
        ↓
Read-only Tools / MCP / RAG / Evidence
        ↓
Safe Test Runner
        ↓
Isolated Workspace + Structured Patch
        ↓
SQLite / SQLAlchemy / Alembic Persistence
```

## Diagnosis → Verification → Repair

1. 用户提交 repository path、failure summary 和 test log。
2. BackgroundJobRuntime 创建并执行诊断任务。
3. Failure Analyzer 先用 deterministic parser 提取测试名、HTTP 状态码和字段信息。
4. Planner 规划读取测试日志、Git Diff、Git Log、源码和代码搜索等只读工具调用。
5. Evidence Collector 持久化结构化 Evidence。
6. Verifier 只允许被多个独立 Evidence 支持的结论成为 confirmed，否则保持 hypothesis。
7. 用户明确触发 Repair 后，系统在临时隔离 Workspace 应用结构化 Patch。
8. Safe Test Runner 只执行白名单测试命令，并受 Workspace、Timeout、输出截断和取消约束。
9. 最终 Report 记录 Root Cause、Verification、Repair Status、Patch、Attempts 和 Evidence。

## Evaluation

Evaluation 使用固定 Dataset 批量执行真实 CI Diagnosis Workflow，持久化 EvaluationRun 和 EvaluationCaseResult，并聚合：根因准确率、确认准确率、工具选择、证据覆盖、证据关联性、工具成功率、平均步骤、平均工具调用、失败率、验证成功率和修复相关指标。

## 安全与可靠性

- WorkspaceGuard 限制仓库和文件路径。
- Developer Tools 只读，禁止任意 Bash。
- Safe Test Runner 只允许 `pytest` / `python`。
- Patch 使用结构化替换和 allowlist 文件范围。
- Repair 只发生在临时 Workspace，原始仓库不写入。
- BackgroundJobRuntime 提供 lease、retry、cancel 和幂等保护。
- Task、Evidence、ToolCall、Job 查询遵循 owner/tenant scope。
- Trace、ToolCall、Evidence、RepairOutcome 可审计。

## Golden Demo

Golden Case：DTO 从 `user_id` 变为 `uid`，测试代码未同步，接口返回 422。Agent 通过 Test Log、Git Diff 和 Source/Code Search 建立证据链，确认根因；用户触发 Repair 后，系统只在隔离 Workspace 将测试字段更新为 `uid`，执行 Safe Test Runner，输出验证通过结果。

## 已知限制

- 当前 Benchmark 仍以已有自动化测试结果为主，缺少长期线上样本。
- Token Usage 受 Provider 能力影响，部分记录为 null。
- SSE 长连接压力测试和 Worker 进程级 crash recovery 仍需补充专门基准。
- app.py 尚未完成渐进式拆分。
- 当前 Repair Generator 以受控 Golden Case 为主，尚未覆盖通用代码修复。
