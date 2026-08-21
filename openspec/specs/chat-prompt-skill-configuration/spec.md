# chat-prompt-skill-configuration Specification

## Purpose
定义聊天系统提示词与技能装配配置，使每个 user 可以在受控目录内选择提示预设和技能，并让聊天流持久化真实的工具调用与 reasoning 上下文。
## Requirements
### Requirement: User chat assembly configuration
系统 SHALL 提供一个 user 范围的聊天组件配置，包含一个有效的用户系统提示词和零个或多个由当前 user 上传的有效 Skill 标识符。系统 SHALL 对 Skill 上传执行 Agent Skills 标准的文件名、大小、编码、YAML frontmatter、`name` 和 `description` 校验。

#### Scenario: 首次配置读取创建默认值
- **WHEN** 一个已认证的 user 读取聊天组装配置，且之前没有保存的记录
- **THEN** 系统 MUST 创建并持久化该 user 的默认系统提示词，返回该默认提示词以及空 Skill 选择。

#### Scenario: User creates and edits prompts
- **WHEN** 已认证的 user 创建或修改系统提示词
- **THEN** 系统 MUST 将提示词名称、内容和更新时间保存到当前 user 范围内，并在后续配置读取中展示。

#### Scenario: User uploads standard Skill files
- **WHEN** 已认证的 user 上传名为 `SKILL.md`、UTF-8 编码、非空、不超过 64KB，并包含有效 `name` 与 `description` frontmatter 的 Markdown 文件
- **THEN** 系统 MUST 将 Skill 标准名称、描述、文件内容、大小和更新时间保存到当前 user 范围内，并在后续配置读取中展示

#### Scenario: Invalid Skill file is rejected
- **WHEN** 上传文件名不是 `SKILL.md`、文件为空、内容不是 UTF-8、超过 64KB、frontmatter 无效或缺少合法 `name`/`description`
- **THEN** 系统 MUST 使用统一的参数错误拒绝请求，错误消息 MUST 指出违反的 Skill 规范，并且 MUST NOT 保存该 Skill

#### Scenario: User saves valid selections
- **WHEN** 已认证的 user 选择自己的一个系统提示词和零个或多个自己上传的 Skill，并确认配置
- **THEN** 系统 MUST 验证标识符属于当前 user，仅对该 user 保留选择，并返回保存的配置。

#### Scenario: Invalid or cross-user selection is rejected
- **WHEN** 请求包含未知的提示词 ID、未知 Skill ID 或另一个 user 的资产 ID
- **THEN** 系统 MUST 会以统一的验证错误拒绝它，并保留 user 之前的配置。

#### Scenario: Deleted selected assets are removed safely
- **WHEN** user 删除当前选中的 Skill 或系统提示词
- **THEN** 系统 MUST 从该 user 的选择中移除被删除 Skill，删除当前提示词时 MUST 回退到该 user 的默认提示词。

### Requirement: Server-side chat assembly
流式聊天服务 SHALL 从当前 Agent 的保存配置中构建后续的 user 系统提示，并将所选标准 Skill 作为独立运行时输入交给 LangChain `load_skill` Tool，同时保留强制性的系统安全、引用、MCP 和当前时间指令。

#### Scenario: Saved user prompt affects a later chat request
- **WHEN** 一个 user 保存并选择自己的系统提示词后发送新的聊天消息
- **THEN** 这个 Agent MUST 在服务器端 system prompt 中接收该系统提示词正文。

#### Scenario: Selected Skill is available through progressive disclosure
- **WHEN** 一个 user 上传并选择自己的 `SKILL.md` 后发送新的聊天消息
- **THEN** 后端 MUST 通过 Repository 加载该 Skill，在 system prompt 中只暴露 name 和 description，并注册只能读取所选 Skill 的 `load_skill` Tool，完整正文 MUST NOT 被预先拼入 system prompt

#### Scenario: Existing conversations remain intact
- **WHEN** 一个 user 在对话已包含消息后更改其配置
- **THEN** 系统 MUST 仅对后续的 Agent 执行应用新配置，并且 MUST NOT 修改已持久化的消息或工具审计。

### Requirement: Truthful reasoning context
系统 SHALL 只有在模型事件流实际提供推理内容时，才会发出并持久化深度思考的上下文。

#### Scenario: 模型返回推理内容
- **WHEN** 一个 OpenAI-compatible 模型 chunk 包含支持的推理内容
- **THEN** 聊天流 MUST 将发出有序的推理增量，并将累积的推理与完成的助手消息元数据一起保存。

#### Scenario: 模型未返回推理内容
- **WHEN** 模型未返回推理内容
- **THEN** 系统 MUST NOT 生成推理事件或合成思维文本。

### Requirement: Uploadable Skill verification samples
仓库 SHALL 提供 5 个可供开发人员手动上传验证的独立标准 Skill 样例，每个样例位于 `<skill-name>/SKILL.md`，并满足当前上传契约。

#### Scenario: Developer inspects Skill samples
- **WHEN** developer 查看仓库中的 Skill 示例目录
- **THEN** 目录 MUST 包含恰好 5 个 Skill 子目录，每个目录 MUST 包含一个 UTF-8、非空、小于 64KB 且具有合法 name 和 description frontmatter 的 `SKILL.md`

#### Scenario: Developer uploads a sample
- **WHEN** developer 在“Skill 设置”中选择任一示例子目录中的 `SKILL.md`
- **THEN** 前端和后端校验 MUST 接受该文件，显示标准 name 和 description，并允许 user 后续多选启用

#### Scenario: Samples remain opt-in
- **WHEN** 项目启动或 user 尚未上传示例
- **THEN** 系统 MUST NOT 自动创建、上传或启用任何示例 Skill

### Requirement: Configuration refresh preserves prompt disclosure state
系统提示词的展开或收起状态 SHALL 由组件局部交互控制，配置保存产生的服务端数据刷新 MUST NOT 重置该状态。

#### Scenario: User saves selected Skills after collapsing a prompt
- **WHEN** user 收起正在使用的系统提示词后点击“保存使用的 Skill”并收到更新后的配置
- **THEN** 该系统提示词 MUST 保持收起，MUST NOT 因配置对象替换而自动展开

#### Scenario: Prompt configuration loads for the first time
- **WHEN** 系统提示词配置首次从 null 变为可用
- **THEN** 前端 MAY 展开当前使用的提示词一次，之后的配置刷新 MUST 保持 user 的展开选择
