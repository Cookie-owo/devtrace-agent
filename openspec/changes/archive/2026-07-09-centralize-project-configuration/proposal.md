## Why

项目配置被拆分为环境示例、运行时环境变量和提供方特定的 JSON 文件。对于这个私有仓库，本地开发应使用带有具体值的受跟踪配置文件，以便后端、前端和 Compose 启动都读取同一份真实来源。

## 什么更改

- **BREAKING**: 移除 `.env.example`、基础设施 `.env`、前端 `VITE_*`、后端提供者 JSON 以及本地机器环境变量回退作为应用程序配置输入。
- 为直接本地启动和 Docker Compose 启动添加受跟踪的根项目配置文件。
- 在受跟踪的配置中存储具体的私有仓库开发值，包括 Qwen/OpenAI-compatible 模型设置和腾讯 CLS 凭证。
- 更新后端配置加载，以便从项目配置文件中读取 SQLite 内存、Qwen 提供者和 Milvus 向量存储设置。
- 更新前端配置加载，以便从根项目配置文件中读取 API 基础 URL。
- 仅在第三方 Docker 镜像需要该接口时保留字面量环境变量，其值来源于 Compose 配置，而不是本地 `.env` 文件。
- 更新测试、文档和 OpenSpec 规范以反映受跟踪的配置文件操作。

## 功能

### 新功能

无。

### 修改的功能

- `project-foundation`: 项目配置文件现在包含具体的私有仓库开发值，而不是占位符示例。
- `qwen-openai-provider`: Qwen/OpenAI-compatible 凭据和模型设置仅从跟踪的项目配置文件中加载。
- `docker-compose-startup`: Compose启动不再依赖本地`.env`文件，而是使用跟踪的项目配置来配置应用服务。
- `memory-repositories`: SQLite内存数据库设置从跟踪的项目配置文件中加载。
- `milvus-vector-store`: Milvus连接设置从跟踪的项目配置文件中加载。

## 影响

- 添加 `config/project.json` 和 `config/project.compose.json`。
- 移除 root/backend/frontend/infra `.env.example`，infra `.env` 和 backend 供应商特定的 JSON 配置。
- 重构 backend 设置模块、应用启动、Alembic 配置、前端配置加载、Docker Compose 和 Dockerfile 行为。
- 更新文档、OpenSpec 要求以及仅配置文件的应用程序配置的自动化测试。
