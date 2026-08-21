## Why

`config/project.json` 和包含真实云凭据的 `config/user.project.json` 已进入 Git 历史，即使后续删除，任何能访问旧 commit 或其他分支的人仍可读取。需要同时阻止未来跟踪并重写所有可达历史引用。

## What Changes

- 从所有本地与远端分支历史中删除 `config/project.json` 和 `config/user.project.json`，其他路径内容保持不变。
- 将两个本地配置文件加入 `.gitignore`，避免未来提交。
- 新增不含凭据的 `config/project.template.json`，用于新克隆初始化本地配置。
- 更新配置加载、文档和测试，使项目明确从被忽略的本地配置读取。
- 强制推送重写后的 `main`、`backup` 和 `codex/add-agent-md` 分支。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `repo-hygiene`: 本地项目配置不得被 Git 跟踪，历史中不得保留配置文件路径。
- `shared-user-project-configuration`: 使用受忽略的本地配置与无密钥模板，不再将 user 配置定义为受版本控制文件。

## Impact

这是破坏性的 Git 历史重写，所有受影响 commit hash 会变化，其他协作者需要重新克隆或重置。影响配置模板、文档、测试和三个远端分支；本机运行配置内容保留。
