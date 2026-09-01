# DevPilot Evolution Story

## 1. AIOps 原始项目

项目最初是本地优先的 AIOps 工作台，具备 Chat、Knowledge、MCP 和诊断能力。问题是能力分散，研发测试故障还需要人工在 CI、Git 和源码之间切换。

## 2. CI Diagnosis

新增 CI/Test Failure Diagnosis 垂直场景。先支持一个 Golden Case，通过 Test Log、Git Diff 和 Source Code 建立证据链。这样可以先证明 Agent 在真实研发问题上能完成闭环，而不是先做抽象框架。

## 3. Agent Evaluation

诊断能运行并不代表有效，因此建立固定 Dataset、真实 Workflow Runner、CaseResult、Metrics 和 Compare。重点从“演示成功”转为“可以量化修改 Prompt/Workflow 后是否退化”。

## 4. Safe Verification

仅有根因报告仍可能错误，因此新增 Safe Test Runner。它采用命令白名单、Workspace 限制、Timeout、输出截断和统一 ToolResult，验证诊断结论但不允许任意 Shell。

## 5. Controlled Repair

验证之后再引入受控修复。Patch 结构化表达，应用在临时隔离 Workspace，测试失败只允许有限尝试，原始仓库不写入，不自动 Commit/Push/PR。

## 6. Engineering Hardening

最后围绕可观测性、Job 可靠性、权限、安全边界、前端演示和文档收口。项目重点从“增加功能”转为“可运行、可解释、可回归、可面试讲清楚”。
