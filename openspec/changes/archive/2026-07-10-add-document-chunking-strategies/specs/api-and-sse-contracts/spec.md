## ADDED Requirements

### Requirement: Document chunking HTTP contracts
共享的 API 合同 SHALL 定义了在文档上传时支持的 chunk 配置，并为已保存的文档提供受保护的 chunk 预览响应。

#### Scenario: Upload includes chunking configuration
- **WHEN** 前端上传一个带有选定的 chunking 配置的知识文档
- **THEN** 类型的多部分请求 MUST 应包含配置和响应文档的元数据 MUST 以公开接受的策略。

#### Scenario: Detail preview is requested
- **WHEN** 前端请求拥有文档的 chunk 预览
- **THEN** 合同 MUST 仅通过统一的 HTTP 响应封装返回一个有限类型预览。
