# DevPilot Engineering Hardening

## Golden Path

CI Failure 进入 CI Diagnosis Workflow，经过只读 Git/Code/Test Log 工具建立 Evidence；必要时通过 Safe Test Runner 验证。用户显式触发 Repair 后，系统创建 `ci_repair` BackgroundJob，在临时隔离 Workspace 中应用结构化 Patch，再执行白名单测试命令。原始仓库不会被写入，不会自动 Commit、Push 或创建 PR。

## 安全边界

- Developer Tools 和 Safe Test Runner 受 WorkspaceGuard 约束。
- 测试命令仅允许 `pytest` / `python`，禁止 Shell、Bash 和任意命令。
- Patch 仅允许结构化替换，并限制到 allowlist 文件。
- `.env`、项目凭据和用户配置不可读取。
- Task、Evidence、ToolCall 和 Job 查询沿用 owner/tenant scope。

## 可观测性

Task Result 保存 diagnosis trace、tool calls、evidence、verification 和 repair outcome；Repair outcome 包含 patch、changed files、attempts、test result 和失败原因。

## 可靠性

BackgroundJobRuntime 提供 lease、retry、cancel 和幂等保护；SSE 事件从持久化 Job Event 读取，客户端可通过 task snapshot 恢复状态。已知 SSE 长连接和 Worker crash 的压力测试属于后续运维增强，不影响本地 Golden Path。

## 演示步骤

1. 启动后端与前端并登录。
2. 在 `/ci-diagnosis` 提交 repository path、failure summary 和 test log。
3. 查看 Plan、Tool Calls、Evidence、Root Cause 与 Verification。
4. 对已完成任务调用 Repair，查看 Proposed Patch、Repair Attempts 与 Test Result。
5. 在 `/evaluation` 查看 Dataset、Run、Case Results 和指标。
