## Context

`AppFeedback` 是应用唯一的全局操作提示出口，当前 store 只提供 `show` 和 `dismiss`，提示出现后不会自动退出。计时行为属于渲染生命周期，应避免把不可序列化的 timer 放入 Pinia state。

## Goals / Non-Goals

**Goals:**

- 所有全局操作提示显示 3 秒后自动关闭。
- 新提示替换旧提示时安全重置计时。
- 保留手动关闭和过渡动画。

**Non-Goals:**

- 不改变页面内表单校验、确认框或后台任务状态。
- 不引入新的通知依赖或队列系统。

## Decisions

- 在 `AppFeedback` 中监听当前消息并管理单一 timer，因为组件拥有提示的显示生命周期；相比在 Pinia state 保存 timer，这保持 store 可序列化且更容易在卸载时清理。
- timer 捕获消息 id，触发时再次比较当前 id，避免旧回调关闭后来出现的新提示。
- 每次消息变化先清理旧 timer，再为新消息创建完整 3 秒计时；手动关闭导致消息变为 null，同样会清理 timer。

## Risks / Trade-offs

- [三秒可能不足以阅读很长错误信息] → 当前全局反馈均为短消息且保留关闭按钮；详细错误仍由页面内错误区域承载。
- [测试定时逻辑可能变慢] → 使用 Vitest fake timers 验证，不引入真实等待。
