# Windows 安装指南

本指南使用 Windows 10/11、PowerShell 和 Docker Desktop。应用服务在本机运行，Docker 只运行 etcd、MinIO、Milvus、Attu 和 Alertmanager。

## 1. 安装基础工具

以管理员身份打开 PowerShell：

```powershell
winget install Git.Git
winget install Docker.DockerDesktop
winget install OpenJS.NodeJS.LTS
winget install astral-sh.uv
```

安装完成后启动 Docker Desktop，并新开一个命令提示符确认：

```text
git --version
node --version
npm --version
uv --version
docker --version
```

## 2. 安装官方 CLS MCP Server

```text
npm install -g cls-mcp-server@1.0.4
cls-mcp-server --help
```

## 3. 获取并启动项目

```text
git clone <你的私有仓库地址> agent_py
cd agent_py
scripts\start-local.bat
```

首次启动会安装项目依赖、执行 SQLite 迁移、启动基础设施容器，并在本机启动 MCP、后端和前端。打开 `http://127.0.0.1:5173` 开始使用。

## 4. 配置

在启动前从安全模板创建被 Git 忽略的本地配置：

```powershell
Copy-Item config/project.template.json config/project.json
Copy-Item config/user.project.template.json config/user.project.json
```

在本地配置中填写或核对 Qwen API Key、CLS `secretId`/`secretKey`、`region`、`logsetId`、`topicId` 和本机地址。字段说明见[配置与运维教程](../operations-and-monitoring.md)。
