## Why

当前聊天 Skill 缺少标准 frontmatter 和目录结构，运行时还会把完整 Markdown 无条件拼入 system prompt，既不符合 Agent Skills 规范，也失去了按需加载带来的上下文节省。项目需要采用 LangChain 官方 Skills 渐进式披露模式，让模型只根据 `name`、`description` 判断是否调用 `load_skill` 加载完整 Skill。

## What Changes

- **BREAKING**：上传的 `SKILL.md` 必须包含有效 YAML frontmatter，至少提供 kebab-case `name` 和明确的 `description`。
- 将 5 个示例重写为 `skill-name/SKILL.md` 标准目录结构，并补齐元数据和中文使用说明。
- 保持 `langchain.agents.create_agent`，注册 user-scoped `load_skill` LangChain Tool。
- system prompt 只列出所选 Skill 的 name 和 description，并引导模型仅在相关时调用 `load_skill(name)`；完整内容不再预注入。
- API 与前端展示标准 Skill 名称和描述，用户仍可上传、选择和删除自己的 Skill。
- 增加自动化及前端端到端验证，证明 Skill 可被模型按需发现和加载。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `chat-prompt-skill-configuration`：上传校验、元数据、示例结构和运行时 Skill 装配改为 Agent Skills 标准。
- `stream-rag-chat`：聊天 Agent 使用标准 `load_skill` Tool 和轻量 Skill catalog 渐进式加载 Skill。
- `chat-experience`：前端 Skill 列表展示标准名称和描述，并保持上传与会话配置工作流。

## Impact

- 后端直接声明安全 YAML parser 依赖，更新 `uv.lock`。
- 修改聊天配置解析、SQLite Skill 模型与迁移、Repository、API 契约、聊天 Agent runner 和 SSE 适配。
- 修改 Vue Skill 侧边栏、共享 TypeScript/OpenAPI 契约和测试。
- 修改 `docs/examples/skills` 的文件结构与使用文档。
