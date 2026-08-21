## 上下文

聊天服务目前在 `LangChainChatAgentRunner` 中使用固定系统提示词，SQLite 已通过 Repository 访问会话、消息和工具审计。前端能展示工具审计，但没有用户级装配配置，也不会把工具调用和模型返回的 reasoning 内容折叠到对应助手消息下。

## Goals / Non-Goals

**目标：**
- 为每个用户保存一个系统提示词预设和多个受控 Skill 标识，首次读取时生成默认配置：通用提示词和 `frontend-design`。
- 在后端按当前用户配置构建下一次 Agent 的系统提示词，并为聊天 SSE 增加真实 reasoning delta 的可选通道。
- 在 Web 对话页可编辑、保存和恢复配置，并把工具调用和 reasoning 放在助手消息下的折叠详情中。

**非目标：**
- 不执行 Codex 本机技能、不加载任意用户提供的提示词文件、不暴露模型内部未返回的推理。
- 不重写已有会话、消息、工具审计或 MCP 调用流程；配置只影响保存后的后续聊天请求。

## 决策

### 将提示词和 Skill 目录定义为项目受控配置

在 `config/project.json` 中定义提示词预设和 Skill 的 id、中文名称与系统指令；前后端通过同一份受控服务目录读取选择，而不是让浏览器直接提交任意 system prompt。`frontend-design` 是默认 Skill，但它被翻译成受控的设计协作指令，不会尝试启动 Codex Skill 运行时。这样既满足多选装配，也防止提示词注入越过项目权限边界。

### 使用用户级 SQLite 仓库，而不是 localStorage

新增 `user_chat_configurations` 表，以 `owner_user_id` 唯一约束保存 `system_prompt_id`、`skill_ids_json` 与更新时间。读取采用 get-or-create 默认值，更新会验证所有 id 在目录中有效。Repository 继续自动传入 owner scope，因此刷新、换设备和鉴权隔离都由服务端保证。

### 每次聊天在服务端装配当前配置

`ChatStreamingService` 在建立 `ChatAgentRequest` 前读取配置，`LangChainChatAgentRunner` 使用目录生成基础安全指令、选中提示词和 Skill 指令。系统安全与当前时间/MCP 约束始终保留，用户选择只能增加回答风格或工作方法，不能删除安全约束或工具权限。配置不会追溯性改写已有消息。

### 仅流式和持久化模型的真实 reasoning 内容

扩展 SSE 与消息 metadata 的 `reasoning` 字段。适配器仅从 LangChain/Qwen chunk 的 `reasoning_content`、`reasoning` 或显式 reasoning content block 提取文本；不存在则不发事件、不显示折叠面板。前端增量聚合后在完成消息 metadata 中保存，工具审计继续走现有持久化路径。

### 使用原生 details 展示消息级上下文

在助手消息中使用可键盘操作的 `details/summary` 展示工具调用和深度思考，默认折叠。这样长会话保持可扫描，用户可按消息展开上下文，且不将原始 JSON 默认铺开。

## Risks / Trade-offs

- [模型不返回 reasoning] → UI 只显示工具调用，明确不伪造思考过程。
- [配置目录变更导致旧 id 无效] → Repository 读取时回退默认值并只保存有效 Skill id。
- [系统提示词被过长 Skill 指令淹没] → 限制目录条目数量与总长度，固定安全前缀始终最先装配。
- [用户期待自定义自由文本] → 首期只提供受控预设，后续可单独设计审核与长度限制。

## 迁移计划

1. 创建 SQLite 表和 Repository，未有记录的用户懒创建默认配置。
2. 发布契约和 API，再让聊天服务读取配置并发送可选 reasoning SSE。
3. 部署前端配置面板与消息折叠详情；回滚时保留表数据但恢复默认 Agent 提示词即可。

## 开放问题

无。首期的提示词和 Skill 均由项目配置目录提供。
