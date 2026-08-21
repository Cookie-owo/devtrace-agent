# Docker Compose 基础设施

`infra/compose.yaml` 仅管理本机开发所需的容器基础设施：**etcd, MinIO, Milvus, Attu 和 Alertmanager**。后端、前端和腾讯云 CLS MCP Server 由仓库根目录启动脚本直接在本机启动，不属于 Compose 服务。

## 启动基础设施

在仓库根目录执行：

```bash
docker compose -f infra/compose.yaml up -d etcd minio milvus attu alertmanager
```

服务地址：

- Alertmanager：`http://localhost:9093`
- Milvus：`localhost:19530`
- MinIO 控制台：`http://localhost:9001`
- Attu：`http://localhost:8001`
- Milvus Web UI/指标端口：`http://localhost:9091`

停止基础设施：

```bash
docker compose -f infra/compose.yaml down
```

仅在需要清除本地状态时才删除 Compose 卷：

```bash
docker compose -f infra/compose.yaml down -v
```

## 本机应用服务

在完成基础设施启动后，使用下列任一启动器运行官方 MCP、FastAPI 后端和 Vite 前端：

```bash
./scripts/start-local.sh
```

Windows 命令提示符：

```text
scripts\start-local.bat
```

## 配置与边界

- `config/project.json`：直接本机开发使用。
- `infra/compose.yaml`：只描述容器基础设施。

私有仓库允许在受版本控制的配置文件中保存开发模型与 CLS 凭据。应用代码不会读取本机 `.env` 文件。

文档上传与知识索引都是运行时工作流，绝不会在启动时自动执行。真实 CLS 日志上传与 Alertmanager 样例请遵循[真实日志与告警教程](../docs/tutorials/real-log-and-alert.md)。Compose 栈不会部署外部日志、链路追踪或云可观测性后端。
