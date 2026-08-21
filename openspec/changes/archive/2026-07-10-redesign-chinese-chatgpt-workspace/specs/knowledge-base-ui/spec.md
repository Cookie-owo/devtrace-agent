## MODIFIED Requirements

### Requirement: Policy-aware document upload
前端 SHALL 在发送请求前，将让 user 上传文档到选定的知识库，并强制执行并显示共享上传策略的中文说明。

#### Scenario: 用户上传支持的文档
- **WHEN** 一个 user 选择或拖放一个符合允许的文件扩展名、MIME 类型和大小策略的文件
- **THEN** 前端 MUST 通过指定的 API 边界上传它，立即显示其持久化的元数据，并在中文中明显标识上传或索引工作。

#### Scenario: User selects an invalid document
- **WHEN** 文件超过共享大小限制或具有不受支持的扩展名或 MIME 类型
- **THEN** 前端 MUST 在上传前应拒绝该文件，并显示基于政策的清晰中文提示信息。

#### Scenario: Upload duplicates an existing document
- **WHEN** 后端报告没有覆盖权限的重复文档
- **THEN** 前端 MUST 保留所选文件，用中文解释冲突，并在再次尝试时要求明确的 user 操作，同时启用覆盖功能。

### Requirement: Document index lifecycle visibility
前端 SHALL 使异步文档索引状态、失败、重试和手动重建在中文中可见，而不会阻止工作区。

#### Scenario: An index task is active
- **WHEN** 上传或重建的文档有挂起或运行中的索引任务
- **THEN** 前端 MUST 识别是否正在等待或被索引，在文档行和详细上下文中显示该状态，并仅轮询相应的任务直到达到终止状态或离开工作区。

#### Scenario: Indexing fails
- **WHEN** 索引任务报告失败状态和失败原因  
- **THEN** 前端 MUST 显示失败原因并提供一个使用现有重试任务端点的中文重试命令

#### Scenario: User rebuilds an indexed document
- **WHEN** 一个 user 选择重新生成文档的索引
- **THEN** 前端 MUST 为该文档创建一个新的索引任务，并将其返回的生命周期状态反映为中文。

### Requirement: Document inspection and deletion
前端 SHALL 显示持久化的文档元数据，并允许 user 通过显式的中文确认删除可访问的文档。

#### Scenario: User opens a document detail
- **WHEN** 一个 user 从工作区中选择一个文档
- **THEN** 前端 MUST 显示其文件名、源类型、哈希值、大小、上传时间、文档状态和索引状态，这些信息来自服务器支持的元数据。

#### Scenario: User deletes a document
- **WHEN** 一个 user 确认可访问文档的删除
- **THEN** 前端 MUST 调用文档删除端点，并在后端确认删除后，仅移除文档及其显示的任务状态。
