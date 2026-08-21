## MODIFIED Requirements

### Requirement: Frontend document management
前端 SHALL 为上传、列表、状态显示、详细元数据、删除、上传后自动首次索引以及手动索引重建提供经过身份验证的文档管理界面。

#### Scenario: Authenticated user views documents
- **WHEN** 加载已认证的工作区
- **THEN** 前端 MUST 使用存储的 bearer 令牌请求当前 user 的知识库文档，并显示文件名、状态、索引状态、大小和上传时间。

#### Scenario: User uploads selected file
- **WHEN** 一个 user 选择文件并提交上传表单  
- **THEN** 前端 MUST 通过共享文档上传 API 发送文件，为上传的文档创建索引任务，在任务运行时显示文档正在索引，并在成功后刷新文档列表。

#### Scenario: User deletes a document
- **WHEN** 一个 user 从文档列表中删除文档
- **THEN** 前端 MUST 调用受保护的删除 API 并在成功后从可见列表中移除文档

#### Scenario: User rebuilds a document index
- **WHEN** 一个 user 触发已拥有文档的索引或重新索引
- **THEN** 前端 MUST 调用受保护的文档索引任务 API 并从经过身份验证的 API 响应中刷新可见文档/任务状态。
