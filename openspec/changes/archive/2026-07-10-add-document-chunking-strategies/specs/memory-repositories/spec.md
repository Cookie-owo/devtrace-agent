## ADDED Requirements

### Requirement: Persisted document chunking configuration
文档仓库 SHALL 保留并返回经过验证的 chunking 配置作为文档元数据，同时保留现有的 owner 和知识库作用域边界。

#### Scenario: 返回已存储的已拥有文档的配置
- **WHEN** 一个经过身份验证的 user 在上传后读取其拥有的文档
- **THEN** 仓库支持的响应 MUST 返回文档的持久化 chunking 配置。
