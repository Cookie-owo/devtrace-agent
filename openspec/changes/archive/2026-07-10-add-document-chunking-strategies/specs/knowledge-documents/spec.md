## ADDED Requirements

### Requirement: Document upload chunking selection and preview
知识文档工作流 SHALL 接受一个由 user 选择的有效 chunk 配置，将其与所拥有的文档一起保存，并在上传后公开一个受保护的预览。

#### Scenario: Upload persists selected configuration
- **WHEN** 已认证的 user 上传一个允许的文档，并带有有效的 chunking 配置
- **THEN** 系统在创建或运行索引任务之前，将该配置与文档元数据一起存储。

#### Scenario: User reads chunk preview
- **WHEN** 该文档对当前 user 可用  
- **THEN** 的 API MUST 使用共享的 chunking 服务，从持久化配置和可索引文本生成其预览。
