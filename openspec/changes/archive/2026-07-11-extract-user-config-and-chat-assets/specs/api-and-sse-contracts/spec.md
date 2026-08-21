## ADDED Requirements

### Requirement: Chat prompt and Skill asset contracts
系统 SHALL 在共享 API 契约中定义用户系统提示词、用户 Skill 文件、聊天装配选择以及对应的受保护 HTTP 路径。

#### Scenario: Prompt CRUD contracts are shared
- **WHEN** 前端或后端实现系统提示词创建、修改、删除和配置读取
- **THEN** 两者 MUST 使用 `packages/api-contracts` 中导出的提示词 DTO、创建请求、更新请求和响应类型。

#### Scenario: Skill upload and delete contracts are shared
- **WHEN** 前端或后端实现 `*SKILL.md` 上传、展示、选择和删除
- **THEN** 两者 MUST 使用共享契约描述 Skill DTO、上传响应、删除响应和配置响应中的 Skill 集合。

#### Scenario: OpenAPI describes chat asset paths
- **WHEN** 检查 OpenAPI 合约
- **THEN** 它 MUST 包含受保护的 `/chat/prompts`、`/chat/prompts/{promptId}`、`/chat/skills` 和 `/chat/skills/{skillId}` 路径，并声明统一的 401、403 和验证错误响应。

#### Scenario: Chat configuration response includes editable assets
- **WHEN** 已认证的 user 读取 `/chat/configuration`
- **THEN** 响应契约 MUST 包含该 user 可编辑的系统提示词内容、上传 Skill 文件名、Skill 内容摘要和当前选择。
