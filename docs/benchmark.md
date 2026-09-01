# DevPilot Benchmark

## 已验证结果

以下数字来自当前仓库实际运行记录：

| 项目 | 结果 |
|---|---:|
| Frontend Test Files | 22 passed |
| Frontend Tests | 79 passed |
| Pyright | 0 errors |
| Ruff | passed |
| Contracts Typecheck | passed |
| Evaluation Unit Tests | 3 passed |
| Evaluation Integration Tests | passed |
| Safe Test Runner Tests | 3 passed |
| Repair / Patch Tests | passed |
| Golden Path E2E | passed |
| CI Workflow Tests | passed |
| Security Regression Tests | passed |

## 已覆盖场景

- Golden Case：`user_id` → `uid` DTO 契约变更。
- 证据不足时保持 hypothesis。
- Tool failure / timeout。
- Safe Test Runner 非法命令、越权路径和测试失败。
- Structured Patch 应用、冲突和 allowlist。
- Isolated Workspace 原始仓库不变。
- BackgroundJob cancellation、retry 和幂等相关测试。

## 尚无真实统计的数据

以下数据当前没有足够的长期或压力测试样本，不能伪造数值：

- 线上 Root Cause Accuracy 长期均值：待补充。
- 真实模型 Token Usage：部分 Provider 未提供，待补充。
- 并发 Diagnosis 吞吐、P95/P99 延迟：待补充。
- 并发 Evaluation Run 吞吐：待补充。
- SSE 长连接稳定时长和断线重放压力结果：待补充。
- Worker crash recovery 统计：待补充。

## 一次可复现的 20 Case Workflow Run

执行方式：在本地 SQLite 临时数据库中，使用 `builtin-v1` 数据集和受控
`golden-order-service` Fixture，逐个进入现有 `CiDiagnosisWorkflow`，再由确定性
指标计算器聚合结果。该实验不是线上数据评测，也不代表真实 LLM 的稳定性。

| 指标 | 实际结果 |
|---|---:|
| Case 数量 | 20 |
| Root Cause Accuracy | 10% (2/20) |
| Confirmation Accuracy | 20% (4/20) |
| Tool Selection Accuracy | 100% (20/20) |
| Evidence Coverage | 20% (4/20) |
| Evidence Groundedness | 100% (20/20) |
| Tool Success Rate | 75% |
| Average Steps | 4.0 |
| Average Tool Calls | 4.0 |
| Failure Rate | 0% |
| Average Latency | 0.316 秒 |
| Token Usage | null（当前 Provider/Runner 未提供） |

结果说明：该结果暴露出当前内置 Dataset 与诊断输出之间存在明显语义不匹配，
同时 ToolCall 状态和延迟字段尚未完整接入 Evaluation 聚合，不能将其包装成生产
准确率。它可作为后续修复 Dataset Fixture、Trace 字段和评测口径的基线。

## 解释口径

当前测试证明的是 Workflow、工具边界、证据约束、任务持久化和隔离修复的工程正确性；Fake/Deterministic 测试不等价于真实 LLM 稳定性评测。
