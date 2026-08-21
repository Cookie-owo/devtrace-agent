## Context

聊天服务目前保存任意 `*SKILL.md` 文本，并在每次请求中把所选文件完整拼入 system prompt。示例文件没有 YAML frontmatter，API 也没有标准 `name`、`description` 元数据。LangChain 官方 Skills 文档给出了 `create_agent + load_skill` Tool 的渐进式披露模式；Deep Agents 的 SkillsMiddleware 源码也采用“先暴露元数据、相关时再读正文”的原则。

## Goals / Non-Goals

**Goals:**

- 使用 `langchain.agents.create_agent` 和标准 `load_skill` LangChain Tool。
- 仅向模型初始上下文提供 Skill 名称和描述，由模型按相关性调用工具读取完整 `SKILL.md`。
- 上传、持久化、API 和前端统一使用标准 Skill 元数据。
- 保持 user scope、聊天 SSE、工具审计、知识库与 MCP 工具能力。
- 用真实前端工作流验证上传、选择和按需加载。

**Non-Goals:**

- 不自动启用仓库示例 Skill。
- 不让用户上传 Skill 附属脚本或可执行资产；本次仍只接收单个 `SKILL.md`。
- 不把普通聊天改造成自定义 LangGraph 状态图。

## Decisions

### 使用请求级 LangChain Tool 暴露所选 Skill

每次聊天请求从 user-scoped Repository 读取已选 Skill，构造只包含这些 Skill 的不可变 registry，并注册 `load_skill(skill_name)` StructuredTool。工具只允许按标准 name 精确读取 registry，返回完整内容或明确的可用名称，不访问全局 Skill，也不会跨 user scope。

`create_agent` 的 system prompt 增加轻量 catalog，每项仅包含 name 和 description，并明确引导模型在任务匹配时调用 `load_skill`。未选择 Skill 时不注册该工具，也不增加 catalog。知识库、当前时间和 MCP 工具继续作为 tools 传入。

### 元数据在上传时解析并持久化

使用 YAML safe parser 解析 frontmatter，要求文件名严格为 `SKILL.md`，`name` 为 kebab-case 且长度受限，`description` 非空且不超过 1024 字符。SQLite 新增 `name`、`description` 列，API 返回这两个字段，前端直接展示而不是截取正文。

为兼容已有本地数据库，迁移为旧记录生成稳定 name、说明文字并补写 frontmatter；新上传必须满足严格标准。

### system prompt 不包含完整 Skill

聊天服务只装配强制指令、用户选择的系统提示词以及 Skill name/description catalog。所选 Skill 作为 `ChatAgentRequest.skills` 传给 runner，完整内容仅保存在请求级 Tool 闭包中，是否读取由模型工具调用决定。该实现遵循 LangChain 官方 Skills 文档，并参考 Deep Agents 源码的元数据校验和提示词原则。

### 示例采用标准目录结构

`docs/examples/skills/<skill-name>/SKILL.md` 包含 frontmatter 和正文。README 说明浏览器上传时进入子目录选择其中同名的 `SKILL.md`，Skill 身份来自 frontmatter `name`。

## Risks / Trade-offs

- [`load_skill` 结果进入聊天工具事件] → 沿用现有 SSE 与审计适配，只在结果摘要中截断持久化内容，完整 ToolMessage 仍供模型当前调用使用。
- [Qwen 可能不主动读取匹配 Skill] → 使用清晰、互斥的 description，并在端到端验证中提出明确匹配问题，检查 `read_file` 工具事件和回答标记。
- [旧 Skill 不符合规范] → 数据迁移生成兼容 frontmatter；所有后续上传严格校验。
- [请求级 Store 重复构造] → 只写入当前 user 已选择的少量 Skill，避免跨用户共享和无界上下文。

## Migration Plan

1. 新增 YAML parser 直接依赖、数据库列和旧记录迁移。
2. 更新上传校验、Repository、API/OpenAPI 和前端展示。
3. 为 Agent runner 注册请求级 `load_skill` Tool，并移除正文预注入。
4. 重写示例并执行后端、前端和 OpenSpec 全量验证。
5. 本地迁移数据库，启动后端/前端，通过浏览器完成上传、选择、对话和工具事件验证。

回滚时可恢复普通 `create_agent` 和旧 prompt 装配；新增数据库列可保留，不影响旧代码读取已有列。

## Open Questions

无。
