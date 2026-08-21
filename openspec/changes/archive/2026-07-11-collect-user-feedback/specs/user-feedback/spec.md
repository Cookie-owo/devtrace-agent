## ADDED Requirements

### Requirement: Owner-scoped unified feedback
系统 SHALL 保存当前用户对 chat_message、citation、diagnostic_step 和 diagnostic_report 的反馈，包括 rating、可选原因、评论与纠正内容。

#### Scenario: 用户重复评价同一目标
- **WHEN** 同一用户再次提交同一 target 与 subject 的反馈
- **THEN** 系统 MUST 更新原反馈而不是创建重复记录。

#### Scenario: 用户评价其他用户目标
- **WHEN** 目标不属于当前用户
- **THEN** API MUST 返回统一权限错误且 MUST NOT 创建反馈。

### Requirement: Feedback lifecycle
用户 SHALL 能读取、修改和删除自己的反馈。

#### Scenario: 用户删除反馈
- **WHEN** 用户删除自己的反馈
- **THEN** 反馈 MUST 不再出现在目标反馈查询中。

### Requirement: Compact feedback interaction
前端 SHALL 在聊天回答、引用详情、诊断步骤和报告中提供不干扰正文的反馈入口，并显示提交中、成功和错误状态。

#### Scenario: 用户选择反对
- **WHEN** 用户点击反对
- **THEN** 前端 MUST 提供原因、评论或纠正内容的渐进输入并允许提交。
