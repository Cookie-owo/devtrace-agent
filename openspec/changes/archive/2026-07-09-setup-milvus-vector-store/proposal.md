## Why

知识库检索需要一个专用的向量存储边界，以便文档 chunk 可以被索引和搜索，而不会将业务代码与 Milvus 客户端调用或导入时的网络连接耦合。

## 什么更改

- 为知识库 chunk 嵌入添加一个 Milvus 向量存储功能。
- 定义集合模式、向量设置、索引设置、搜索参数和 tenant 元数据契约。
- 实现显式的 Milvus 连接管理、health 检查、集合初始化和索引初始化。
- 将 Milvus 启动委托给由 `standardize-docker-compose-startup` 引入的 Docker Compose 堆栈。
- 确保 Milvus 访问仅在应用程序启动或显式初始化流程期间发生，绝不在模块导入时发生。

## 功能

### 新功能
- `milvus-vector-store`: 定义后端 Milvus 向量集合、连接生命周期、初始化、health 检查以及 tenant 感知的 chunk 搜索边界。

### 修改后的功能
- 无。

## 影响

- 后端依赖项：添加官方 Milvus Python 客户端。
- 后端代码：添加向量存储配置、模式定义、连接管理器和仓库式存储抽象。
- 后端测试：添加对模式、初始化、health 检查、tenant 元数据、查询过滤器和导入时连接安全性的单元测试。
- 基础设施：使用现有的 `infra/compose.yaml` Milvus 服务作为运行时依赖；无需额外的 Milvus 启动脚本。
