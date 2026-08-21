## Context

当前 Chat 页面已有服务器端系统提示词和 Skill 配置，但前端把两类资产混在同一个面板中，用户难以理解“单选提示词”和“多选 Skill”的差异。知识库上传策略仍允许 csv/json/txt，并且 PDF 仅按 UTF-8 解码，导致真实 PDF 文档无法可靠索引。AIOps 页面已有功能组件，但信息架构和视觉层级不够接近用户期望的 ChatGPT 网页式工作台。

本次前端设计按 `frontend-design` 与 `ui-ux-pro-max` 的工具型 AI 控制台方向执行：中文界面、密集但清晰、低装饰、明确状态、表单错误就近恢复、所有交互保持键盘可用。视觉基线选择偏中性的 AI-native 控制台，而不是营销页或装饰性仪表盘。

## Goals / Non-Goals

**Goals:**
- Chat 工作区提供两个独立侧边栏：“对话系统提示词设置”和“skill设置”，分别承载单选提示词和多选 Skill。
- Prompt 条目支持折叠/展开，展开后可编辑保存；删除当前使用的提示词时后端仍回退到默认提示词。
- Skill 上传在前后端都给出具体规范：文件名 `*SKILL.md`、UTF-8 Markdown、非空、最大 64KB。
- 知识库上传只接受 Markdown 和 PDF，并使用 `langchain-text-splitters` 与 `pypdf` 优先处理分片和 PDF 文本提取。
- 仅 `fixed-character` 策略暴露和接受 `maxCharacters`/`overlapCharacters`，`markdown-heading` 与 `paragraph` 不要求这些参数。
- AIOps 工作区重构为更像 ChatGPT 网页的中文诊断控制台，突出查询输入、实时状态、步骤时间线、证据链和报告。

**Non-Goals:**
- 不改变聊天 Agent、AIOps LangGraph 或 MCP 工具调用的核心推理流程。
- 不引入除 Markdown/PDF 之外的新文档格式。
- 不把 Skill 执行成独立插件运行时；本次仍作为系统提示词上下文传递给 Agent。
- 不迁移历史已上传文档；历史记录保留原元数据，新上传走新策略。

## Decisions

1. **聊天配置拆成两个右侧侧边栏**
   - 使用两个 Vue `<script setup>` 组件分别管理提示词和 Skill，保留共享 Pinia store/API 客户端。
   - 理由：单选与多选的心智模型不同，拆开后能显示更具体的规则和保存状态。
   - 备选：保留一个 tab 面板。放弃原因是用户明确要求“单独抽出来当一个侧边栏”。

2. **Prompt 折叠状态只保存在前端 UI**
   - 折叠/展开不影响后端事实数据，只影响当前页面可视状态。
   - 理由：折叠属于展示偏好，避免污染聊天配置契约。

3. **Skill 规范在 UI 与后端错误中双写**
   - 前端上传前进行文件名/大小/空内容检查，界面固定展示规范；后端仍执行最终校验并返回统一错误码。
   - 理由：前端即时反馈降低失败成本，后端保持安全边界。

4. **文档类型收紧为后缀优先、MIME 辅助**
   - 后端只允许 `.md` 与 `.pdf` 后缀；Markdown 允许浏览器常见的 `text/markdown`、`text/plain` 或空/`application/octet-stream`，PDF 要求 `application/pdf` 或空/`application/octet-stream`。
   - 理由：浏览器对 `.md` MIME 识别不稳定，后缀必须是主判断；同时不再接受 csv/json/txt。

5. **分片实现优先使用现成库并保留确定性兜底**
   - `fixed-character` 使用 `RecursiveCharacterTextSplitter`。
   - `markdown-heading` 使用 `MarkdownHeaderTextSplitter`，并保留过大段落的固定字符兜底。
   - `paragraph` 使用段落边界聚合，必要时使用固定字符兜底。
   - PDF 文本使用 `pypdf.PdfReader` 提取；无法提取文字时返回明确验证错误，避免空内容进入索引。

6. **AIOps 页面使用三栏响应式控制台**
   - 桌面：左侧输入/告警/历史，中间实时诊断时间线，右侧证据/报告/案例。
   - 窄屏：按任务输入、实时进展、证据报告顺序堆叠。
   - 视觉风险点控制在一个“诊断脉冲轨道”签名元素上，其余界面保持克制。

## Risks / Trade-offs

- [Risk] 旧文档格式不再可上传可能影响临时测试数据。→ 在文案、契约和测试中明确只支持 Markdown/PDF，必要时用户先转成 Markdown。
- [Risk] 扫描版 PDF 无可提取文本。→ 使用 pypdf 提取不到文本时给出明确错误，后续再单独引入 OCR。
- [Risk] 侧边栏增多导致小屏拥挤。→ 使用响应式布局让侧边栏在窄屏变为上下连续面板，并控制最小触控区域。
- [Risk] LangChain text splitters 版本行为变更。→ 后端测试覆盖三种策略、固定参数和无文本 PDF 错误，必要时保留本地兜底函数。
