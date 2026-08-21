## 上下文

后端目前只有基础元数据，没有 LLM 提供商。仓库指南已经要求 `langchain-openai` `ChatOpenAI` 使用配置中的 OpenAI-compatible Qwen/Bailian 设置，并明确禁止记录密钥或将业务代码与供应商专用的 SDK 耦合。

阿里云 Model Studio 文档通过 Qwen 聊天端点进行 OpenAI-compatible 访问，而 LangChain 文档支持显式的 `api_key`、`base_url`、`model`、`temperature` 和 `timeout` 样式配置。因此，实现应使用 OpenAI-compatible 设置，而不是 DashScope 特定的运行时 API。

## Goals / Non-Goals

**目标：**
- 为 OpenAI-compatible Qwen 设置添加一个跟踪的后端提供者配置文件。
- 在跟踪的配置中存储默认模型名称：`qwen3.7-max`、`text-embedding-v4` 和 `qwen3-vl-rerank`。
- 将 `langchain-openai` 作为后端 LLM 运行时依赖项。
- 提供一个可替换的 LLM 提供者抽象。
- 使用 `ChatOpenAI` 实现默认提供者。
- 提供一个可以无需真实网络调用进行测试的异步 readiness 检查。
- 更新环境示例和文档，而不要提交真实的密钥。

**非目标:**
- 不提供聊天服务、提示编排、记忆、工具、SSE 流式传输、AIOps 诊断或持久化行为。
- 不使用 DashScope SDK。
- 不将真实的 API 密钥提交到跟踪文件中；跟踪的配置仅存储 `api_key_env`。
- 自动化测试中不强制进行实时模型调用。

## 决策

### 决策：对跟踪的提供者默认值使用 JSON
后端将包含 `apps/backend/config/qwen-openai.json` 中的非秘密提供者默认值。JSON 保持在 Python 3.10 的 Python 标准库中的解析，并避免添加配置依赖项。

考虑过的替代方案：
- TOML：被拒绝，因为 Python 3.10 缺少 `tomllib`，仅为此配置添加解析器是不必要的。
- YAML：被拒绝，因为它会添加另一个解析器依赖。

### 决策：使用小型配置数据类
提供者层将加载跟踪的 JSON 文件，从配置的环境变量中读取密钥，并公开一个类型化的数据类。这将密钥处理与已提交的默认值分开。

考虑的替代方案：
- 添加 `pydantic-settings`：目前被拒绝，因为所需的解析工作量较小，添加另一个依赖项为时过早。
- 在业务代码中硬编码 Qwen 设置：被拒绝，因为端点、模型名称、温度和超时必须由配置控制。

### 决策：将 `ChatOpenAI` 隐藏在提供者协议之后
业务代码将调用一个提供者接口，该接口创建一个聊天模型并检查 readiness。具体的 Qwen 实现将由后续的 OpenAI-compatible 提供者替换。

考虑的替代方案：
- 在服务中直接实例化 `ChatOpenAI`：被拒绝，因为这会将业务代码与供应商选择耦合。
- 现在构建完整的提供者注册表：在存在多个提供者之前被拒绝。

### 决策：就绪性调用一个最小的提示，但测试使用假数据
readiness 方法将创建配置的聊天模型，并使用最小提示调用 `ainvoke`。单元测试将注入虚假模型以在不进行网络调用的情况下验证成功和失败行为。

考虑的替代方案：
- 仅检查配置的就绪状态：被拒绝，因为需求要求具备连接能力。
- 自动化测试调用 Qwen 本地：被拒绝，因为测试必须是确定性的，并且不能需要真实的密钥。

## Risks / Trade-offs

- 实时 readiness 调用可能会产生供应商费用或延迟 → 缓解措施：将其作为显式检查公开，而不是模块导入行为。
- Qwen 区域/基础 URL 因账户/工作区而异 → 缓解措施：保持 `OPENAI_BASE_URL` 可配置，并记录占位符默认值。
- LangChain 第三方兼容性仅限于官方 OpenAI API 字段 → 缓解措施：仅依赖标准聊天模型行为，避免使用供应商特定的响应字段。
- 密钥泄露风险 → 缓解措施：不要提交真实密钥，不要在 readiness 输出中包含密钥，并在提交前进行扫描。

## 迁移计划

1. 为提供者功能添加 OpenSpec 资产。
2. 添加失败的后端测试，用于配置、提供者构建、假 readiness 成功、假 readiness 失败，以及无 DashScope 依赖。
3. 实现配置和提供者模块。
4. 添加 `langchain-openai` 依赖并刷新 `uv.lock`。
5. 添加带有 Qwen 聊天、嵌入和重新排序模型名称的跟踪 JSON 提供者配置。
6. 使用占位符值更新后端环境示例和文档。
7. 运行后端检查、OpenSpec 验证、同步规范、归档、提交和推送。

## 开放问题

此提供程序设置无相关内容。后续的功能提案应决定提示模板、流式语义、每个工作流的重试次数以及生成的 API readiness 端点。
