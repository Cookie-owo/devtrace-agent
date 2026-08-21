## 1. 配置抽取与 merge

- [x] 1.1 新增用户项目配置文件，将指定 LLM、CLS MCP、CLS 上传目标字段移入用户覆盖文件，并把基础配置对应字段置空。
- [x] 1.2 实现后端项目配置递归 merge，确保缺失用户配置时保留基础默认值且不读取本机环境变量。
- [x] 1.3 实现前端项目配置 merge，确保 Vite 端读取同一组基础配置和用户覆盖配置。
- [x] 1.4 更新本地启动脚本和配置相关测试，验证 CLS MCP 启动值和 LLM/CLS 字段来自 merged 配置。

## 2. 后端用户聊天资产

- [x] 2.1 新增 SQLite 模型、Alembic 迁移、Repository record/protocol/实现，用于用户系统提示词和用户 Skill 文件。
- [x] 2.2 新增提示词创建、更新、删除接口，并保证默认提示词、tenant 隔离和删除回退。
- [x] 2.3 新增 `*SKILL.md` 上传、列表展示、删除接口，并保证文件名校验、内容校验、tenant 隔离和选择清理。
- [x] 2.4 更新 `/chat/configuration` 读写逻辑，返回用户资产并只允许选择当前 user 的提示词和 Skill。
- [x] 2.5 更新流式聊天服务，发送给 Agent 的 `system_prompt` 使用当前 user 选择的提示词正文和 Skill 文件内容。

## 3. 前端与共享契约

- [x] 3.1 更新 `packages/api-contracts` 的聊天配置 DTO 和 OpenAPI 路径。
- [x] 3.2 更新前端 Chat client/store，支持提示词创建、修改、删除和 Skill 上传、删除、选择。
- [x] 3.3 重构聊天装配设置面板，展示用户历史提示词和 Skill，支持创建、保存、修改、上传、删除、选中及执行中/保存中状态。

## 4. 验证与归档

- [x] 4.1 补充后端测试覆盖配置 merge、提示词 CRUD、Skill 上传/删除/选择以及 Agent 实际接收动态 system prompt。
- [x] 4.2 补充前端测试覆盖提示词编辑保存、Skill 上传删除和选择保存。
- [x] 4.3 运行后端 lint/type/test、前端 typecheck/test/build 和 OpenSpec 验证。
- [x] 4.4 启动项目并用前端验证提示词创建/保存/修改/生效，以及 Skill 上传/删除/选中/生效。
- [x] 4.5 归档 OpenSpec 变更，提交并通过 443 推送。
