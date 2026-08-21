## Why

当前聊天配置、Skill 上传、知识库上传和 AIOps 页面虽然具备基础功能，但交互入口混在一起、错误提示不够具体，知识库上传策略也与当前产品目标不一致。需要把面向中国用户的 ChatGPT 风格工作台进一步收敛为清晰、可恢复、可验证的体验。

## What Changes

- 将聊天系统提示词配置拆成独立侧边栏“对话系统提示词设置”，支持创建、保存、删除、单选使用，并让每个提示词可折叠/展开。
- 将 Skill 配置拆成独立侧边栏“skill设置”，支持上传、删除、多选使用，并在界面和后端错误中明确 Skill 文件规范。
- 收紧知识库上传策略：仅支持 `.md` 与 `.pdf`，并使用现成库处理 Markdown/PDF 文本和分片；非固定字符策略不展示也不要求最大字符和 overlap 输入。
- 重构 AIOps 页面为更专业的中文 AI 运维诊断工作台，强化运行中/等待中/失败等异步状态、证据链和报告布局。
- **BREAKING**：知识库文档上传不再接受 `.csv`、`.json`、`.txt`。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `chat-experience`: 聊天工作区的系统提示词和 Skill 配置入口从混合面板改为两个独立侧边栏，并强化折叠、选择和保存反馈。
- `chat-prompt-skill-configuration`: Skill 上传规范和后端校验错误需要明确文件名、大小、编码和内容要求。
- `knowledge-documents`: 上传策略收敛为 Markdown/PDF，前端和共享契约展示一致的限制和恢复提示。
- `document-chunking-strategies`: 三种分片策略使用明确参数模型，只有 `fixed-character` 接受最大字符和 overlap；Markdown/PDF 索引文本应由现成库优先提取和拆分。
- `aiops-diagnosis-ui`: AIOps 工作区视觉和信息架构升级为中文、响应式、证据优先的运维诊断控制台。

## Impact

- 后端：知识库上传校验、可索引文本提取、分片配置解析、Skill 上传校验和相关测试。
- 前端：聊天页面侧边栏组件、知识库上传表单、AIOps 页面与组件样式、错误提示和组件测试。
- 共享契约：文档上传策略、分片配置类型和 OpenAPI schema。
- 依赖：优先使用 `langchain-text-splitters` 做文本/Markdown 分片，使用 `pypdf` 提取 PDF 文本。
