# Knowledge Base UI Specification

## Purpose

为管理当前 user 的知识文档、异步索引生命周期和持久化源元数据定义经过身份验证的 Vue 工作区。
## Requirements
### Requirement: Authenticated knowledge document workspace
前端 SHALL 提供一个经过身份验证的 `/knowledge` 工作区，该工作区仅使用共享 API 合同列出已登录的 user 的后端服务器知识库和文档。当 user 可以从多个可访问的知识库中进行选择时，它 MUST 仅显示知识库选择控件。

#### Scenario: User opens their knowledge workspace
- **WHEN** 已认证的 user 打开 `/knowledge`
- **THEN** 前端 MUST 从后端加载 user 的可访问知识库和所选基础的文档，而不将浏览器存储视为文档目录。

#### Scenario: User changes the knowledge base selection
- **WHEN** 一个 user 从显示的多知识库控件中选择一个可访问的知识库
- **THEN** 前端 MUST 仅加载并显示为该选定知识库返回的文档

#### Scenario: Workspace has one knowledge base
- **WHEN** 该 user 拥有且仅有一个可访问的知识库
- **THEN** 工作区 MUST 忽略不可操作的知识库选择控件。

#### Scenario: Workspace has no documents
- **WHEN** 选定的知识库没有文档
- **THEN** 工作区 MUST 显示一个清晰的空白状态和可用的上传操作。

### Requirement: Policy-aware document upload
前端 SHALL 使 user 在将文档上传到选定的知识库时，强制执行并以中文显示共享上传策略，然后再发送请求。

#### Scenario: 用户上传支持的文档
- **WHEN** 一个 user 选择或拖放一个符合允许的扩展名、MIME 类型和大小策略的文件
- **THEN** 前端 MUST 通过类型化的 API 边界上传它，立即显示其持久化元数据，并在中文中明显标识上传或索引工作。

#### Scenario: User selects an invalid document
- **WHEN** 文件超过共享大小限制或具有不受支持的扩展名或 MIME 类型
- **THEN** 前端 MUST 在上传前应拒绝该文件，并显示基于政策的清晰中文提示信息。

#### Scenario: Upload duplicates an existing document
- **WHEN** 后端在没有覆盖权限的情况下报告重复文档  
- **THEN** 前端 MUST 保留所选文件，用中文解释冲突，并在再次尝试时要求明确的 user 操作，同时启用覆盖功能。

### Requirement: Document index lifecycle visibility
前端 SHALL 使异步文档索引状态、故障、重试和手动重建在中文中可见，而不会阻塞工作区。

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
前端 SHALL 在其对应文档行下方以内联、默认折叠的披露方式显示持久化文档元数据，并允许 user 通过显式的中文确认删除可访问的文档。

#### Scenario: User opens a document detail
- **WHEN** 一个 user 会从工作区展开文档的内联披露
- **THEN** 前端 MUST 使用服务器支持的元数据在该文档行下方显示其文件名、源类型、哈希值、大小、上传时间、文档状态、索引状态、保存的 chunk 策略以及 chunk 预览

#### Scenario: Document detail starts collapsed
- **WHEN** 工作区最初会渲染一个文档行
- **THEN** 其元数据和 chunk 预览披露 MUST 应该在 user 展开之前保持折叠状态。

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

### Requirement: Chunking selection and preview UI
经过身份验证的知识工作区 SHALL 提供中文控件，用于在上传期间选择文档 chunking 策略，并用于在文档的内联披露中查看持久化文档的 chunk 预览。

#### Scenario: User selects a strategy before upload
- **WHEN** 一个 user 选择要上传的文件
- **THEN** 前端 MUST 以可见的选中状态展示固定字符、Markdown 标题和段落策略及其相关参数。

#### Scenario: User reviews uploaded chunks
- **WHEN** 一个 user 在上传后或从文档列表中展开已拥有文档的内联披露
- **THEN** 前端 MUST 请求并显示保存的策略、总 chunk 数量以及在该文档行下方绑定的 chunk 引用片段

### Requirement: Scrollable knowledge document workspace
知识库工作区 SHALL 允许 user 访问任意数量的文档以及展开后的完整详情和分片预览。

#### Scenario: Document list exceeds available height
- **WHEN** 文档条目总高度超过桌面工作区剩余高度
- **THEN** 文档列表 MUST 提供可见的纵向滚动，并保持文档区标题和后续条目可访问

#### Scenario: Expanded preview exceeds its bound
- **WHEN** 展开的文档详情或分片预览超过可用高度
- **THEN** 详情区域 MUST 提供独立纵向滚动，MUST NOT 裁切预览或遮挡后续文档

#### Scenario: Narrow viewport displays documents
- **WHEN** user 在窄屏设备查看长列表或展开预览
- **THEN** 页面 MUST 使用自然纵向滚动，内容 MUST NOT 因桌面固定高度约束而不可访问
