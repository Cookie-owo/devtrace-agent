## 上下文

该仓库已在本地为 Codex 和 OpenSpec 初始化。Git 当前报告 `.idea/` 作为未跟踪的本地 IDE 元数据，这与项目工作流程无关。

## Goals / Non-Goals

**目标：**
- 添加一个根 `.gitignore`，该文件忽略 JetBrains IDE 元数据。
- 保留项目设置文件，如 `.codex/`、`openspec/` 和 `agent.md`，使其对 Git 可见。

**非目标:**
- 不要配置远程仓库。
- 不要更改 OpenSpec、Codex 或应用程序运行时行为。
- 请勿从文件系统中删除本地 `.idea/` 目录。

## 决策

- 因为这是 Git 用于仓库范围的忽略规则的标准机制，所以使用根 `.gitignore`。
- 目前仅添加 `.idea/`，因为这是 Git 当前报告的 user 要求忽略的唯一本地元数据目录。

## Risks / Trade-offs

- 未来的工具可能会创建其他本地元数据，这些元数据仍然会出现在 Git 状态中。缓解措施：仅在已知且有意的情况下添加忽略条目。
