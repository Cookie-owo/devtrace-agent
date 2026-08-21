## ADDED Requirements

### Requirement: Chunking selection and preview UI
经过身份验证的知识工作区 SHALL 提供中文控件，用于在上传期间选择文档 chunking 策略，并用于查看已保存文档的 chunk 预览。

#### Scenario: User selects a strategy before upload
- **WHEN** 一个 user 选择要上传的文件
- **THEN** 前端 MUST 以可见的选中状态展示固定字符、Markdown 标题和段落策略及其相关参数。

#### Scenario: User reviews uploaded chunks
- **WHEN** 上传成功或 user 打开一个已拥有文档详情
- **THEN** 前端 MUST 请求并显示保存的策略、总 chunk 数量以及绑定的可展开 chunk 中文摘录
