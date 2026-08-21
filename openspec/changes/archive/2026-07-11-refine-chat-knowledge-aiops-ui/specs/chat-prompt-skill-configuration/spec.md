## MODIFIED Requirements

### Requirement: User chat assembly configuration
系统 SHALL 提供一个 user 范围的聊天组件配置，包含一个有效的用户系统提示词和零个或多个由当前 user 上传的有效 Skill 标识符。系统 SHALL 对 Skill 上传执行明确的文件名、大小、编码和内容校验。

#### Scenario: 首次配置读取创建默认值
- **WHEN** 一个已认证的 user 读取聊天组装配置，且之前没有保存的记录
- **THEN** 系统 MUST 创建并持久化该 user 的默认系统提示词，返回该默认提示词以及空 Skill 选择。

#### Scenario: User creates and edits prompts
- **WHEN** 已认证的 user 创建或修改系统提示词
- **THEN** 系统 MUST 将提示词名称、内容和更新时间保存到当前 user 范围内，并在后续配置读取中展示。

#### Scenario: User uploads Skill files
- **WHEN** 已认证的 user 上传文件名匹配 `*SKILL.md`、UTF-8 编码、非空且不超过 64KB 的 Markdown 文件
- **THEN** 系统 MUST 将 Skill 文件名、内容、大小和更新时间保存到当前 user 范围内，并在后续配置读取中展示。

#### Scenario: Invalid Skill file is rejected
- **WHEN** 上传文件名不匹配 `*SKILL.md`、文件为空、内容不是 UTF-8 文本或大小超过 64KB
- **THEN** 系统 MUST 使用统一的参数错误拒绝请求，错误消息 MUST 能指出违反的 Skill 规范，并且 MUST NOT 保存该 Skill。

#### Scenario: User saves valid selections
- **WHEN** 已认证的 user 选择自己的一个系统提示词和零个或多个自己上传的 Skill，并确认配置
- **THEN** 系统 MUST 验证标识符属于当前 user，仅对该 user 保留选择，并返回保存的配置。

#### Scenario: Invalid or cross-user selection is rejected
- **WHEN** 请求包含未知的提示词 ID、未知 Skill ID 或另一个 user 的资产 ID
- **THEN** 系统 MUST 会以统一的验证错误拒绝它，并保留 user 之前的配置。

#### Scenario: Deleted selected assets are removed safely
- **WHEN** user 删除当前选中的 Skill 或系统提示词
- **THEN** 系统 MUST 从该 user 的选择中移除被删除 Skill，删除当前提示词时 MUST 回退到该 user 的默认提示词。
