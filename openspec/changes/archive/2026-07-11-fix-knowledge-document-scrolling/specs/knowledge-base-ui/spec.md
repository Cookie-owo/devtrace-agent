## ADDED Requirements

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
