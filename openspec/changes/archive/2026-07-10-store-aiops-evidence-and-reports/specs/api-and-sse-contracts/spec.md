## ADDED Requirements

### Requirement: Diagnostic history and evidence-chain API contracts
共享的 API-contract 包 SHALL 定义了经过身份验证的响应类型和 OpenAPI 路径，用于列出 AIOps 诊断历史记录和读取完整的诊断证据链。

#### Scenario: History and evidence-chain paths are described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它 MUST 用统一的成功和授权错误响应描述受保护的 `GET /aiops/diagnostics` 和 `GET /aiops/diagnostics/{diagnosticId}/evidence-chain` 操作。

#### Scenario: Evidence-chain response is typed
- **WHEN** 前端或后端代码使用诊断证据链
- **THEN** 它 MUST 对任务输入、步骤、工具调用、类型证据、报告、报告证据链接和 checkpoints 使用共享类型。
