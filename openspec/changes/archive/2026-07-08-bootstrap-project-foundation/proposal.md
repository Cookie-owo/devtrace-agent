## Why

仓库将从零开始重建，需要在功能工作开始前建立一个干净的基础。现在建立单一代码库、后端、前端、共享合约、基础设施、文档和质量门禁可以防止旧的实现假设渗入新的方案中。

## 什么更改

- 创建一个包含 `apps/backend`、`apps/frontend`、`packages/api-contracts`、`infra`、`openspec` 和 `docs` 的 monorepo 结构。
- 在 `apps/backend/src/super_ai` 下使用 `uv`、`pyproject.toml` 和 `src` 布局添加一个 Python 后端模板。
- 使用 Vite 和 TypeScript 在 `apps/frontend` 下添加一个 Vue 3 前端模板。
- 添加后端和前端测试目录，并包含最小可执行测试。
- 在根目录添加 README 和适用于根目录、后端和前端工作流的环境变量示例。
- 为后端配置基线质量工具：`ruff`、`pyright`、`pytest` 和 `pytest-asyncio`。
- **BREAKING**: 不保留或支持旧目录或历史实现代码。

## 功能

### 新功能
- `project-foundation`: 定义了新后端、前端、合约、基础设施、文档和质量工作流所需的仓库基础。

### 修改后的功能

无。

## 影响

- 添加新的仓库结构和初始的源代码、测试、配置、文档和环境示例文件。
- 基于 `uv` 引入后端 Python 开发命令。
- 基于 `npm`、Vite、Vue 3 和 TypeScript 引入前端开发命令。
- 添加 OpenSpec 验证、后端 lint/类型/测试检查以及前端类型/测试/构建检查的验证路径。
