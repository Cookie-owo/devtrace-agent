# Linux 安装指南

本指南以 Debian/Ubuntu 为例。应用服务在本机运行，Docker 只运行 etcd、MinIO、Milvus、Attu 和 Alertmanager。

## 1. 安装基础工具

```bash
sudo apt update
sudo apt install -y git curl ca-certificates docker.io docker-compose-plugin nodejs npm
curl -LsSf https://astral.sh/uv/install.sh | sh
```

重新打开终端后，确认工具可用：

```bash
git --version
node --version
npm --version
uv --version
docker --version
```

如需免 sudo 使用 Docker，请按 Docker Engine 官方文檔把当前用户加入 `docker` 组后重新登錄。

## 2. 安装官方 CLS MCP Server

```bash
npm install -g cls-mcp-server@1.0.4
cls-mcp-server --help
```

## 3. 获取并启动项目

```bash
git clone <你的私有仓库地址> agent_py
cd agent_py
./scripts/start-local.sh
```

首次启动会安装项目依赖、执行 SQLite 迁移、启动基础设施容器，并在本机启动 MCP、后端和前端。打开 `http://127.0.0.1:5173` 开始使用。

## 4. 配置

在启动前从安全模板创建被 Git 忽略的本地配置：

```bash
cp config/project.template.json config/project.json
cp config/user.project.template.json config/user.project.json
```

在本地配置中填写或核对 Qwen API Key、CLS `secretId`/`secretKey`、`region`、`logsetId`、`topicId` 和本机地址。字段说明见[配置与运维教程](../operations-and-monitoring.md)。
