## ADDED Requirements

### Requirement: User feedback API contracts
共享契约 SHALL 定义反馈 upsert、列表和删除 API，以及 targetType、rating、reason、comment、correction 和时间字段。

#### Scenario: 客户端提交反馈
- **WHEN** 前端提交反馈
- **THEN** 后端 MUST 返回统一 envelope 中的规范化反馈对象。
