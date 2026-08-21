## Context

仓库已有 `docs/` 文档目录、60 个完整 OpenSpec 历史归档和根 npm workspace，但没有文档站点、变更索引或同步机制。历史归档均包含 proposal、design、tasks 和 delta specs，适合一次性迁移。WIKI 必须引用 OpenSpec 源文件而不是复制内容，并在创建/归档后可重复同步。

## Goals / Non-Goals

**Goals:**

- 用 VitePress 提供本地可浏览的项目与变更 WIKI。
- 通过 `docs/openspec` 符号链接和 `@include` 保持 OpenSpec 为唯一事实来源。
- 提供仓库级 `wiki-sync` Skill 与确定性脚本，覆盖 active、archive 和全量历史同步。
- 独立验证 delta specs、主规格同步状态、include 目标、索引/侧栏一致性和构建。
- 忽略 VitePress 构建与缓存产物。

**Non-Goals:**

- 不修改历史 OpenSpec 文件内容。
- 不部署公网文档站点。
- 不把生成后的 HTML 提交到 Git。

## Decisions

### VitePress 作为根 workspace 开发依赖

在根 `package.json` 增加 `vitepress` 和 `docs:dev/docs:build/docs:preview`，文档源目录固定为 `docs`。这样不新增独立 workspace，也能复用根 `package-lock.json`。

### 使用符号链接和相对 include

创建 `docs/openspec -> ../openspec`。active 页面位于 `docs/changes/active/{name}/index.md`，include 使用 `../../../openspec/changes/{name}/...`；archive 页面使用 `../../../openspec/changes/archive/{date}-{name}/...`。页面同时 include proposal、design、tasks 和每个 delta spec。

### Skill 携带确定性同步脚本

`.codex/skills/wiki-sync/SKILL.md` 保存用户给定的触发语义、流程和 Guardrails；`scripts/sync_wiki.py` 负责扫描文件系统、生成页面/索引/Sidebar 和执行结构校验。脚本支持 active、archive 与 all 三种模式，避免手工维护 60 多条侧栏时漂移。

### 归档校验不以构建代替

脚本在写入前检查每个归档都有 delta specs，并根据 requirement 名称核对对应 main spec；写入后解析每个 `@include`，逐项确认目标存在，再检查页面集合、索引和 Sidebar 的顺序一致。`npm run docs:build` 是独立的最终门禁。

### 生成物统一忽略

`.gitignore` 增加 `docs/.vitepress/dist/` 与 `docs/.vitepress/cache/`。启动后再次检查工作区，若 VitePress 产生其他非源文件目录则一并忽略。

## Risks / Trade-offs

- [历史 main spec 可能被后续变更再次修改] → 同步校验以 capability、requirement 名称和移除语义为基础，报告不一致并阻断，不修改 OpenSpec。
- [Sidebar 条目很多] → 已归档分组默认折叠，并由脚本按日期倒序生成。
- [符号链接在部分 Windows Git 配置中可能受限] → 文档明确使用仓库约定的符号链接，构建验证在当前开发环境执行。

## Migration Plan

1. 安装 VitePress、建立配置和符号链接。
2. 添加并验证 `wiki-sync` Skill 与脚本。
3. 同步 active 变更和全部历史 archive 页面。
4. 校验 include、规格同步、索引/Sidebar 和 VitePress 构建。
5. 归档本变更后再次全量同步，使本变更自身进入 archive WIKI。
6. 启动 VitePress 并检查/忽略运行生成物。

## Open Questions

无。
