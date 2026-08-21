## Context

两个配置文件都已被 Git 跟踪：基础文件在 11 个提交中出现，并含测试 Prometheus 凭据和本地账户密码；user 文件在 2 个提交中出现，并含真实 Qwen 与腾讯云凭据。远端 `main`、`backup`、`codex/add-agent-md` 均可能保持旧对象可达。

## Goals / Non-Goals

**Goals:**

- 从所有分支的每个历史 tree 中移除两个精确路径。
- 从其他历史文件中替换与本地配置相同的已知 Qwen、腾讯云凭据和私有服务地址。
- 保留其他文件内容、提交元数据和拓扑。
- 保留本机运行配置，但阻止未来 Git 跟踪。
- 给新克隆提供无敏感值模板。

**Non-Goals:**

- 无法改变已被第三方克隆、fork、缓存或下载的副本。
- 不用历史重写代替已暴露凭据轮换。

## Decisions

- 使用 `git-filter-repo --invert-paths` 同时删除 `config/project.json` 与 `config/user.project.json`。相比 `filter-branch`，它更可靠地处理全部 refs 并清理重写元数据。
- 对全历史执行敏感值扫描；若同一凭据或私有服务地址曾复制到其他文件，使用 `git-filter-repo --replace-text` 只替换敏感值，保留文件及其余内容。
- 重写前在 `/tmp` 创建短期 bundle 和配置副本；成功推送和验证后立即删除 bundle，只将配置副本恢复到被忽略路径。
- 显式重写并强制推送三个远端分支，不将仅本地的开发分支意外发布。
- 模板中的所有 API key、云凭据、远端服务密码、演示账户密码和目标资源 ID 为空。

## Risks / Trade-offs

- [所有 commit hash 改变] → 保留作者、时间、消息和非目标 tree 内容，并通知协作者重新克隆。
- [GitHub 仍缓存旧对象] → 删除所有远端 refs；如旧 hash 仍可直达，需轮换凭据并联系 GitHub Support 清除缓存。
- [历史重写失败] → 使用临时 bundle 恢复；远端验证成功后才销毁。

## Migration Plan

1. 提交 `.gitignore`、模板、文档和归档 OpenSpec。
2. 备份配置与全部 refs，安装并运行 `git-filter-repo`。
3. 恢复被忽略的本地配置，重新添加 SSH 443 远端。
4. 强制推送三个远端分支。
5. 验证所有本地/远端可达提交均不包含目标路径或已知敏感值，再删除临时 bundle。
