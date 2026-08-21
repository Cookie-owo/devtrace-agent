## ADDED Requirements

### Requirement: Authenticated live frontend acceptance verification
在此更改最终确定之前，必须通过浏览器交互验证本地托管的前端 SHALL 的已实现操作符工作流程。

#### Scenario: Operator uses the frontend
- **WHEN** 在打开后端时，本地前端 MCP、Milvus 和 Alertmanager 可用
- **THEN** 经过身份验证的操作员 MUST 应能够验证导航、运行时 readiness、流式聊天和会话持久化、知识文档管理、主动警报条目以及流式 AIOps 证据/报告展示，而不会出现前端错误状态。
