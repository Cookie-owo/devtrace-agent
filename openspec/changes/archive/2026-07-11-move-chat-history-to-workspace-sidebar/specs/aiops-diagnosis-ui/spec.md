## ADDED Requirements

### Requirement: Long reports scroll inside the fixed diagnosis workspace
智能诊断桌面工作区 SHALL 保持受桌面视口约束的固定高度，最终报告过长时 MUST 在报告正文区域内部纵向滚动，不得继续撑高整个浏览器页面。

#### Scenario: Persisted report exceeds the available center height
- **WHEN** user 打开内容高度超过最终报告可用区域的历史诊断报告
- **THEN** AIOps 工作区外框 MUST 保持固定高度，报告标题和元信息 MUST 保持可见，Markdown 正文 MUST 提供独立纵向滚动条

#### Scenario: Other diagnosis columns contain long content
- **WHEN** 左侧历史、诊断过程或右侧执行链超过各自可用高度
- **THEN** 对应栏 MUST 在工作区内部滚动且 MUST NOT 增加页面文档高度
