## MODIFIED Requirements

### Requirement: Chat assembly controls
经过身份验证的 Chat 工作区 SHALL 让 user 可以在中文中查看、选择、确认和恢复其基于服务器的系统提示和多选技能配置，并 SHALL 将系统提示词和 Skill 设置呈现为两个独立侧边栏。

#### Scenario: User opens split chat configuration sidebars
- **WHEN** 已认证的 user 打开 Chat 工作区
- **THEN** 前端 MUST 通过共享合约加载当前配置，并显示“对话系统提示词设置”和“skill设置”两个独立侧边栏，而不以 localStorage 作为事实来源。

#### Scenario: User manages collapsible system prompts
- **WHEN** user 在“对话系统提示词设置”侧边栏查看提示词
- **THEN** 每个提示词 MUST 可折叠和展开，展开后可以编辑名称和正文、保存、删除，并且界面 MUST 只允许单选一个后续对话使用的系统提示词。

#### Scenario: User manages multi-select skills
- **WHEN** user 在“skill设置”侧边栏查看 Skill
- **THEN** 界面 MUST 显示 Skill 上传规范，允许上传、删除，并允许多选零个或多个 Skill 供后续对话 Agent 使用。

#### Scenario: User confirms an updated assembly
- **WHEN** 选择提示或技能并确认
- **THEN** 前端 MUST 通过类型化 API 客户端保存配置，显示保存的装配摘要，并用于后续消息。

#### Scenario: Configuration action fails
- **WHEN** 提示词或 Skill 的创建、保存、删除、上传或配置保存失败
- **THEN** 前端 MUST 在相关侧边栏中显示中文错误，说明可恢复动作，MUST NOT 静默保留一个看似已保存的状态。
