## Context

项目当前只有 `config/project.json` 一个配置入口，个人 API key、模型名、CLS MCP 凭据和 CLS 日志目标与通用默认值混在一起。后端通过 `project_config_section()` 读取该文件，前端通过 Vite 直接 import 该 JSON。聊天装配当前由 `chatAssembly` 静态 catalog 驱动，SQLite 只保存选择 ID，无法表达用户创建的提示词内容或上传的 `SKILL.md` 文件内容。

## Goals / Non-Goals

**Goals:**

- 保留 `config/project.json` 作为基础默认配置，并新增一个用户覆盖配置文件，仅保存每个使用者不同的字段。
- 让后端和前端通过同一个深度 merge 语义读取最终项目配置。
- 通过 SQLite Repository 管理用户系统提示词、用户上传的 Skill 和当前选择。
- 让流式聊天 Agent 的 `system_prompt` 使用当前用户选择的提示词正文和 Skill 文件内容。
- 更新共享 API 契约、前端界面和测试，证明创建、保存、修改、上传、删除、选择和 Agent 生效。

**Non-Goals:**

- 不引入环境变量读取作为项目配置来源。
- 不实现 Skill Marketplace、远程 Skill 下载或跨用户共享 Skill。
- 不把用户上传的 Skill 转换为可执行代码；本次只将 `SKILL.md` 的说明内容作为 LangChain Agent system prompt 的动态上下文注入。

## Decisions

1. 使用 `config/user.project.json` 作为用户覆盖文件。
   - 原因：文件名明确表达它是项目配置的用户覆盖层，开发者只需要修改一个文件。
   - 备选：使用 `.env` 或环境变量；这与当前仓库约束和用户明确要求相反。

2. 配置加载器执行递归对象 merge，数组和标量由覆盖文件整体替换。
   - 原因：个人字段多位于已有对象内部，递归 merge 能保留默认值并只覆盖必要字段。
   - 备选：只 merge 顶层对象；会迫使用户复制完整 `llm` 或 `clsLogUpload` 段，违背最小改动目标。

3. 用户聊天资产持久化到 SQLite，业务层只通过 Repository 访问。
   - 原因：符合现有 memory repositories 边界，也便于后续迁移 PostgreSQL。
   - 备选：把用户资产存成 Markdown 文件；会绕开现有认证和 tenant 隔离边界。

4. 每个用户首次访问聊天配置时自动创建一个默认系统提示词。
   - 原因：避免空配置导致前端无法选择或聊天无法启动，同时仍允许用户之后编辑或新增。
   - 备选：继续使用项目 catalog 默认提示词；这会保留旧的静态装配语义。

5. Skill 上传只接受文件名匹配 `*SKILL.md` 的 Markdown 文本，并保存原始内容。
   - 原因：用户明确要求 `xxxSKILL.md`，保存原文能完整保留 Skill 指令。
   - 备选：解析为结构化字段；当前需求不需要复杂解析，并且可能丢失 Skill 文档语义。

6. LangChain Agent 仍通过 `create_agent(..., system_prompt=...)` 接收动态装配后的内容。
   - 原因：当前 LangChain Agent 边界已经把 `system_prompt` 作为标准入口，用户 Skill 是 Markdown 指令而不是可执行工具。
   - 备选：为每个 Skill 创建 LangChain tool；上传的 `SKILL.md` 不包含可调用函数实现，强行转换会制造伪工具。

## Risks / Trade-offs

- [Risk] 用户覆盖文件包含个人凭据，发给别人时可能需要替换。→ 文档和基础配置明确列出唯一需要修改的字段，基础配置保留空值。
- [Risk] 删除当前选中的系统提示词或 Skill 可能导致选择失效。→ Repository/API 删除后回退到默认提示词，并从选择中移除被删除 Skill。
- [Risk] 旧数据库缺少用户资产表。→ 提供 Alembic 迁移，并在本地启动前运行 `alembic upgrade head`。
- [Risk] 上传 Skill 内容过长会影响提示词长度。→ 后端限制上传文件大小，并在 prompt 中按选中列表注入。

## Migration Plan

1. 新增 `config/user.project.json` 并将指定个人字段从基础配置移入该文件。
2. 更新配置加载器和前端配置读取，使默认读取结果为基础配置与用户覆盖配置的 merge。
3. 新增 SQLite 表、Repository 和 API，迁移已有 `user_chat_configurations` 选择表继续使用。
4. 更新流式聊天服务，从用户资产 Repository 装配 system prompt。
5. 更新前端设置面板和共享契约。
6. 运行迁移、后端/前端测试、类型检查、构建，并启动项目做端到端验证。

回滚时可以恢复旧 `chatAssembly` catalog 使用方式并保留新表不读；配置层可临时删除用户覆盖文件以检查基础配置缺失报错。
