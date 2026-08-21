## ADDED Requirements

### Requirement: Authenticated knowledge document workspace
前端 SHALL 提供一个经过身份验证的 `/knowledge` 工作区，该工作区仅使用共享 API 合同列出已登录 user 的基于服务器的知识库和文档。

#### Scenario: User opens their knowledge workspace
- **WHEN** 已认证的 user 打开 `/knowledge`
- **THEN** 前端 MUST 从后端加载 user 的可访问知识库和所选基础的文档，而不将浏览器存储视为文档目录。

#### Scenario: User changes the knowledge base selection
- **WHEN** 一个 user 选择一个可访问的知识库  
- **THEN** 前端 MUST 加载并仅显示为该选定知识库返回的文档

#### Scenario: Workspace has no documents
- **WHEN** 所选的知识库没有文档  
- **THEN** 工作区 MUST 显示一个清晰的空状态和可用的上传操作。

### Requirement: Policy-aware document upload
前端 SHALL 会在发送请求前强制执行并显示共享上传策略，让 user 上传文档到选定的知识库。

#### Scenario: 用户上传支持的文档
- **WHEN** 一个 user 选择或拖放一个符合允许的扩展名、MIME 类型和大小策略的文件
- **THEN** 前端 MUST 通过类型化的 API 边界上传它，并立即显示其持久化元数据和索引状态。

#### Scenario: User selects an invalid document
- **WHEN** 文件超过共享大小限制或具有不受支持的扩展名或 MIME 类型
- **THEN** 前端 MUST 在上传前应拒绝该文件并显示明确的基于策略的消息。

#### Scenario: Upload duplicates an existing document
- **WHEN** 后端报告没有覆盖权限的重复文档
- **THEN** 前端 MUST 保留所选文件，解释冲突，并在再次尝试时要求明确的 user 操作，同时启用覆盖功能。

### Requirement: Document index lifecycle visibility
前端 SHALL 使异步文档索引状态、失败、重试和手动重建可见，而不会阻塞工作区。

#### Scenario: An index task is active
- **WHEN** 上传或重建的文档有一个挂起或运行中的索引任务
- **THEN** 前端 MUST 显示该状态，并仅在任务达到终止状态或工作区被离开时轮询相应的任务。

#### Scenario: Indexing fails
- **WHEN** 索引任务报告失败状态和失败原因  
- **THEN** 前端 MUST 显示失败原因并提供一个使用现有重试任务端点的重试命令。

#### Scenario: User rebuilds an indexed document
- **WHEN** 一个 user 选择重新生成文档的索引
- **THEN** 前端 MUST 为该文档创建一个新的索引任务并反映其返回的生命周期状态。

### Requirement: Document inspection and deletion
前端 SHALL 会显示持久化的文档元数据，并允许 user 在明确确认后删除可访问的文档。

#### Scenario: User opens a document detail
- **WHEN** 一个 user 从工作区中选择一个文档
- **THEN** 前端 MUST 显示其文件名、源类型、哈希值、大小、上传时间、文档状态和索引状态，这些信息来自服务器后端的元数据。

#### Scenario: User deletes a document
- **WHEN** 一个 user 确认可访问文档的删除
- **THEN** 前端 MUST 调用文档删除端点，并在后端确认删除后，仅删除文档及其显示的任务状态。

#### Scenario: A document request is rejected
- **WHEN** 后端在上传、索引或删除操作中返回规范化的授权、验证或系统错误
- **THEN** 前端 MUST 显示规范化的安全错误，MUST NOT 为该失败操作显示成功本地状态。

### Requirement: Responsive knowledge operations
知识工作区 SHALL 在桌面和窄视口宽度下仍可用于上传、基础选择、元数据审查、索引控制和删除。

#### Scenario: User views the workspace on a narrow screen
- **WHEN** 在窄视口上显示知识工作区
- **THEN** 其文档元数据、状态和操作 MUST 在不出现水平页面溢出的情况下仍可读且可操作。
