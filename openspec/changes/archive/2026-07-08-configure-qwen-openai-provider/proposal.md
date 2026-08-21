## Why

后端需要一个与供应商无关的 LLM 提供商层，以便在聊天和 AIOps 功能开始调用模型之前。Qwen 应通过 OpenAI-compatible 协议连接，这样业务代码可以使用稳定的抽象而不依赖 DashScope SDK 或供应商私有的 API。

## 什么更改

- 添加一个包含OpenAI-compatible端点设置、`api_key_env`、聊天模型、嵌入模型、重新排序模型、温度、超时和重试参数的跟踪后端Qwen提供者配置文件。
- 将默认模型名称配置为`qwen3.7-max`、`text-embedding-v4`和`qwen3-vl-rerank`。
- 添加一个提供者抽象，可以创建一个OpenAI-compatible聊天模型，并且以后可以被另一个提供者替换。
- 使用`langchain-openai` `ChatOpenAI`实现默认的Qwen提供者。
- 为模型连接性添加readiness/config检查功能。
- 使用仅占位符的Qwen/OpenAI-compatible设置更新后端环境示例和文档。
- 确保真实的 API 密钥永远不会被提交或记录。

## 能力

### 新功能
- `qwen-openai-provider`: 定义后端 LLM 提供商配置、Qwen OpenAI-compatible 连接以及 readiness 检查。

### 修改后的功能

无。

## 影响

- 在后端运行时添加对 `langchain-openai` 的依赖。
- 添加后端跟踪模型配置、config/provider 模块和测试用例。
- 更新后端环境示例和文档。
- 不实现聊天业务流程、AIOps 提示、持久化或流式输出。
