<script setup lang="ts">
import { computed, ref } from "vue";
import { createCiDiagnosisClient } from "../ci-diagnosis/ciDiagnosisClient";

const client = createCiDiagnosisClient();
const repositoryPath = ref("");
const failureSummary = ref("");
const testLog = ref("");
const taskId = ref<string | null>(null);
const status = ref("idle");
const report = ref<Record<string, unknown> | null>(null);
const repair = ref<Record<string, unknown> | null>(null);
const evidence = ref<readonly Record<string, unknown>[]>([]);
const tools = ref<readonly Record<string, unknown>[]>([]);
const steps = ref<readonly Record<string, unknown>[]>([]);
const error = ref<string | null>(null);
const canCancel = computed(() => taskId.value !== null && ["queued", "running"].includes(status.value));
const statusLabel = (value: unknown): string => ({ idle: "待开始", queued: "排队中", running: "诊断中", completed: "已完成", failed: "失败", cancel_requested: "正在取消", ok: "成功", error: "失败", not_run: "未执行", passed: "通过" }[String(value)] ?? String(value));

async function submit(): Promise<void> {
  error.value = null; status.value = "queued"; report.value = null;
  try {
    const created = await client.create({ repositoryPath: repositoryPath.value, failureSummary: failureSummary.value, testLog: testLog.value });
    taskId.value = created.taskId;
    void watch(created.taskId);
  } catch (caught) { status.value = "failed"; error.value = caught instanceof Error ? caught.message : "提交失败"; }
}

async function watch(id: string): Promise<void> {
  try {
    for await (const event of client.events(id)) {
      status.value = event.type.includes("completed") ? "completed" : "running";
      if (event.type === "complete" || event.type === "report") await refresh(id);
    }
  } catch { await refresh(id); }
}

async function refresh(id = taskId.value): Promise<void> {
  if (!id) return;
  const [task, stepResult, toolResult, evidenceResult] = await Promise.all([client.get(id), client.steps(id), client.tools(id), client.evidence(id)]);
  status.value = task.status; steps.value = stepResult.items as readonly Record<string, unknown>[]; tools.value = toolResult.items as readonly Record<string, unknown>[]; evidence.value = evidenceResult.items as readonly Record<string, unknown>[];
  const payload = task.result_payload.report;
  report.value = payload && typeof payload === "object" ? payload as Record<string, unknown> : null;
  const repairPayload = task.result_payload.repair;
  repair.value = repairPayload && typeof repairPayload === "object" ? repairPayload as Record<string, unknown> : null;
}

async function cancel(): Promise<void> { if (taskId.value) { await client.cancel(taskId.value); status.value = "cancel_requested"; } }
</script>

<template>
  <section class="ci-page">
    <div class="ci-hero"><p>DEVPILOT / CI 测试诊断</p><h2>测试失败根因诊断</h2><span>分析 Git、测试日志与源码，构建可追溯证据链。</span></div>
    <form class="ci-form" @submit.prevent="submit">
      <label>代码仓库路径<input v-model="repositoryPath" required placeholder="D:\\workspace\\order-service" /></label>
      <label>失败摘要<input v-model="failureSummary" required placeholder="test_create_order 返回 422" /></label>
      <label>测试日志<textarea v-model="testLog" required rows="7" placeholder="粘贴测试失败日志" /></label>
      <div><button type="submit" :disabled="status === 'queued' || status === 'running'">开始诊断</button><button v-if="canCancel" type="button" @click="cancel">取消任务</button><span class="ci-status">{{ statusLabel(status) }}</span></div>
    </form>
    <p v-if="error" class="ci-error">{{ error }}</p>
    <div class="ci-grid"><article><h3>诊断计划 / 步骤</h3><ol><li v-for="step in steps" :key="String(step.stepId)">{{ step.toolName }} · {{ statusLabel(step.status) }}</li></ol></article><article><h3>工具调用</h3><ul><li v-for="call in tools" :key="String(call.id)">{{ call.toolName }} · {{ statusLabel(call.status) }}</li></ul></article></div>
    <article class="ci-report"><h3>根因报告</h3><p v-if="report"><strong>{{ report.confirmed ? "已确认" : "待验证假设" }}</strong>：{{ report.rootCause }}</p><p v-else>等待诊断结果…</p><p v-if="report">建议修复：{{ report.suggestedFix }}</p><h4>测试验证</h4><p v-if="report">状态：{{ statusLabel(report.verificationStatus) }} · 命令：{{ report.verificationCommand || "未执行" }}</p><pre v-if="report && report.verificationResult">{{ JSON.stringify(report.verificationResult, null, 2) }}</pre><h4>受控修复</h4><p v-if="repair">状态：{{ statusLabel(repair.status) }} · 修复尝试：{{ repair.attempts }}</p><p v-if="repair">修改文件：{{ Array.isArray(repair.changedFiles) ? repair.changedFiles.join(", ") : "无" }}</p><pre v-if="repair && repair.patch">{{ JSON.stringify(repair.patch, null, 2) }}</pre><h4>证据</h4><ul><li v-for="item in evidence" :key="String(item.id)">{{ item.type }} · {{ item.summary }}</li></ul></article>
  </section>
</template>

<style scoped>
.ci-page { height: 100%; overflow: auto; padding: clamp(1rem, 3vw, 2.5rem); }
.ci-hero p { color: var(--accent-strong); font-size: .72rem; letter-spacing: .1em; margin: 0; }.ci-hero h2 { margin: .4rem 0; }.ci-hero span { color: var(--text-secondary); }
.ci-form, .ci-report, .ci-grid article { background: var(--surface-raised); border: 1px solid var(--line); border-radius: var(--radius-md); padding: 1rem; }.ci-form { display: grid; gap: .8rem; margin: 1.2rem 0; max-width: 52rem; }.ci-form label { display: grid; gap: .35rem; font-size: .8rem; font-weight: 650; }.ci-form input, .ci-form textarea { border: 1px solid var(--line-strong); border-radius: .4rem; padding: .6rem; font: inherit; }.ci-form button { background: var(--accent); border-radius: .4rem; color: #fff; margin-right: .5rem; padding: .55rem .9rem; }.ci-status { color: var(--text-secondary); font-size: .8rem; }.ci-grid { display: grid; gap: 1rem; grid-template-columns: repeat(2, minmax(0, 1fr)); }.ci-grid li, .ci-report li { margin: .4rem 0; }.ci-error { color: var(--status-danger-text); } @media (max-width: 760px) { .ci-grid { grid-template-columns: 1fr; } }
</style>
