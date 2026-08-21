## ADDED Requirements

### Requirement: Configuration refresh preserves prompt disclosure state
系统提示词的展开或收起状态 SHALL 由组件局部交互控制，配置保存产生的服务端数据刷新 MUST NOT 重置该状态。

#### Scenario: User saves selected Skills after collapsing a prompt
- **WHEN** user 收起正在使用的系统提示词后点击“保存使用的 Skill”并收到更新后的配置
- **THEN** 该系统提示词 MUST 保持收起，MUST NOT 因配置对象替换而自动展开

#### Scenario: Prompt configuration loads for the first time
- **WHEN** 系统提示词配置首次从 null 变为可用
- **THEN** 前端 MAY 展开当前使用的提示词一次，之后的配置刷新 MUST 保持 user 的展开选择
