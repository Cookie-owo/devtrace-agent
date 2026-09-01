<script setup lang="ts">
import { Cable, CheckCircle2, CircleAlert, Clock3, Plus, RefreshCw, Save, Server, Trash2, Wrench } from "lucide-vue-next";
import { computed, onMounted, reactive, watch } from "vue";

import type { McpConnection, McpConnectionMutationRequest, McpTransport } from "@agent-py/api-contracts";

import AppLoadingState from "../components/AppLoadingState.vue";
import { useMcpStore } from "../stores/mcp";

const mcp = useMcpStore();
const draft = reactive<McpConnectionMutationRequest>({ name: "", transport: "sse", url: "", enabled: true, timeoutSeconds: 15, retries: 1 });
const isNew = computed(() => mcp.selected === null);
const statusLabel = (connection: McpConnection): string => {
  if (!connection.enabled) return "已停用";
  if (!connection.lastCheck) return "待检查";
  return connection.lastCheck.ok ? "已连接" : "连接失败";
};
const statusClass = (connection: McpConnection): string => {
  if (!connection.enabled) return "mcp-status--disabled";
  if (!connection.lastCheck) return "mcp-status--checking";
  return connection.lastCheck.ok ? "mcp-status--connected" : "mcp-status--failed";
};
const selectedToolCount = computed(() => mcp.selected?.lastCheck?.toolCount ?? 0);

watch(() => mcp.selected, (connection) => {
  if (connection === null) return;
  Object.assign(draft, { name: connection.name, transport: connection.transport, url: connection.url, enabled: connection.enabled, timeoutSeconds: connection.timeoutSeconds, retries: connection.retries });
}, { immediate: true });

onMounted(() => { void mcp.initialize().catch(() => undefined); });

function newConnection(): void {
  mcp.select("");
  Object.assign(draft, { name: "", transport: "sse" as McpTransport, url: "http://127.0.0.1:3000/sse", enabled: true, timeoutSeconds: 15, retries: 1 });
}

function run(operation: () => Promise<void>): void { void operation().catch(() => undefined); }
function removeSelected(): void {
  if (mcp.selected && window.confirm(`确定删除连接“${mcp.selected.name}”吗？此操作不可撤销。`)) run(() => mcp.remove(mcp.selected!.id));
}
function formatCheckedAt(value: string | null | undefined): string {
  if (!value) return "尚未检查";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "最近检查" : `检查于 ${date.toLocaleString("zh-CN", { month: "numeric", day: "numeric", hour: "2-digit", minute: "2-digit" })}`;
}
function parameterCount(schema: Record<string, unknown>): number {
  const properties = schema.properties;
  return properties && typeof properties === "object" ? Object.keys(properties).length : 0;
}
</script>

<template>
  <section class="mcp-view" aria-label="MCP 连接管理">
    <header class="mcp-view__header">
      <div><p>智能体基础设施</p><h2>MCP 工具连接</h2><span>管理智能体可使用的外部工具与能力。</span></div>
      <div class="mcp-view__header-actions"><span v-if="mcp.selected" class="mcp-status" :class="statusClass(mcp.selected)"><i />{{ statusLabel(mcp.selected) }}</span><button type="button" class="mcp-button mcp-button--primary" title="新建连接" @click="newConnection"><Plus :size="16" aria-hidden="true" />新建连接</button></div>
    </header>
    <AppLoadingState v-if="mcp.isLoading" label="正在加载 MCP 连接" />
    <div v-else class="mcp-view__workspace">
      <aside class="mcp-view__list" aria-label="MCP 连接列表">
        <div class="mcp-view__list-heading"><div><strong>连接列表</strong><small>{{ mcp.connections.length }} 个连接</small></div><Server :size="17" aria-hidden="true" /></div>
        <button v-for="connection in mcp.connections" :key="connection.id" type="button" class="mcp-view__connection" :class="{ 'mcp-view__connection--active': mcp.selectedId === connection.id }" @click="mcp.select(connection.id)">
          <span class="mcp-view__connection-icon"><Server :size="16" aria-hidden="true" /></span><span class="mcp-view__connection-copy"><strong>{{ connection.name }}</strong><small>{{ connection.transport === 'sse' ? 'SSE' : 'Streamable HTTP' }} · {{ formatCheckedAt(connection.lastCheck?.checkedAt) }}</small></span><span class="mcp-status mcp-status--compact" :class="statusClass(connection)"><i /></span>
        </button>
        <div v-if="mcp.connections.length === 0" class="mcp-view__list-empty"><Server :size="22" aria-hidden="true" /><strong>暂无连接</strong><span>创建第一个 MCP 服务连接。</span></div>
      </aside>

      <main class="mcp-view__editor">
        <form class="mcp-view__form" @submit.prevent="run(() => isNew ? mcp.create(draft) : mcp.update(draft))">
          <header class="mcp-view__section-header"><div><p>连接配置</p><h3>{{ draft.name || '未命名 MCP 服务' }}</h3></div><label class="mcp-toggle"><input v-model="draft.enabled" type="checkbox" /><span>启用连接</span></label></header>
          <section class="mcp-section"><div class="mcp-section__title"><h4>基本信息</h4><p>为智能体标识这条工具连接。</p></div><div class="mcp-fields"><label><span>连接名称</span><input v-model.trim="draft.name" required maxlength="120" placeholder="例如：生产日志" /></label><label><span>传输协议</span><select v-model="draft.transport"><option value="sse">SSE</option><option value="streamable_http">可流式 HTTP</option></select></label></div></section>
          <section class="mcp-section"><div class="mcp-section__title"><h4>服务地址</h4><p>填写真实 MCP 服务的访问地址。</p></div><label class="mcp-field-wide"><span>服务 URL</span><input v-model.trim="draft.url" type="url" required maxlength="2048" placeholder="https://mcp.example.com/sse" /></label></section>
          <section class="mcp-section"><div class="mcp-section__title"><h4>可靠性设置</h4><p>控制连接超时和失败重试行为。</p></div><div class="mcp-fields"><label><span>超时时间（秒）</span><input v-model.number="draft.timeoutSeconds" type="number" min="1" max="300" required /></label><label><span>重试次数</span><input v-model.number="draft.retries" type="number" min="0" max="5" required /></label></div></section>
          <div class="mcp-view__commands"><button v-if="mcp.selected" type="button" class="mcp-button mcp-button--secondary" :disabled="mcp.checkingId === mcp.selected.id" @click="run(() => mcp.check(mcp.selected!.id))"><RefreshCw :size="15" :class="{ spin: mcp.checkingId === mcp.selected.id }" aria-hidden="true" />{{ mcp.checkingId === mcp.selected.id ? '检查中…' : '测试连接' }}</button><button v-if="mcp.selected" type="button" class="mcp-button mcp-button--danger" :disabled="mcp.isSaving" @click="removeSelected"><Trash2 :size="15" aria-hidden="true" />删除</button><button type="submit" class="mcp-button mcp-button--primary" :disabled="mcp.isSaving"><Save :size="15" aria-hidden="true" />{{ mcp.isSaving ? '保存中…' : '保存修改' }}</button></div>
        </form>

        <section class="mcp-view__inspection" aria-label="服务能力"><header class="mcp-view__section-header"><div><p>实时工具发现</p><h3>服务能力</h3></div><Cable :size="19" aria-hidden="true" /></header><div v-if="mcp.checkingId" class="mcp-skeleton" aria-label="正在加载服务能力"><span /><span /><span /></div><template v-else-if="mcp.selected?.lastCheck?.ok"><div class="mcp-capability-summary"><div><strong>已发现 {{ selectedToolCount }} 个工具</strong><span>来自真实 MCP 服务的能力清单</span></div><CheckCircle2 :size="18" aria-hidden="true" /></div><div class="mcp-tool-list"><article v-for="tool in mcp.selected.lastCheck.tools" :key="tool.name" class="mcp-tool-card"><span class="mcp-tool-card__icon"><Wrench :size="15" aria-hidden="true" /></span><div><strong>{{ tool.name }}</strong><p>{{ tool.description || '暂无工具描述。' }}</p><small>{{ parameterCount(tool.inputSchema) }} 个参数</small></div><CheckCircle2 :size="15" aria-label="可用" /></article></div></template><div v-else class="mcp-view__empty"><CircleAlert :size="26" aria-hidden="true" /><strong>{{ mcp.selected?.lastCheck ? '连接失败' : '尚未发现工具' }}</strong><span>{{ mcp.selected?.lastCheck?.error || '保存连接并测试后，这里会展示服务真实返回的工具。' }}</span></div></section>
      </main>
    </div>
  </section>
</template>

<style scoped>
.mcp-view { --mcp-navy: #0b1220; --mcp-blue: #2563eb; --mcp-blue-soft: #eff6ff; background: #f6f8fc; color: #0f172a; display: grid; grid-template-rows: auto minmax(0, 1fr); height: 100%; min-height: 0; }
.mcp-view__header { align-items: center; background: #fff; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; min-height: 5.8rem; padding: 1.1rem clamp(1rem, 3vw, 2rem); }
.mcp-view__header p, .mcp-view__section-header p { color: #64748b; font-size: 0.7rem; font-weight: 650; letter-spacing: .04em; margin: 0 0 .3rem; }.mcp-view__header h2 { font-size: 1.5rem; font-weight: 650; letter-spacing: -.02em; margin: 0; }.mcp-view__header > div:first-child span { color: #64748b; display: block; font-size: .82rem; margin-top: .35rem; }.mcp-view__header-actions { align-items: center; display: flex; gap: .8rem; }
.mcp-button { align-items: center; border: 1px solid transparent; border-radius: .6rem; display: inline-flex; font-size: .78rem; font-weight: 650; gap: .4rem; min-height: 2.55rem; padding: 0 .85rem; transition: background var(--transition-fast), border-color var(--transition-fast), color var(--transition-fast), transform var(--transition-fast); }.mcp-button:active { transform: translateY(1px); }.mcp-button:disabled { opacity: .6; }.mcp-button--primary { background: var(--mcp-blue); color: #fff; }.mcp-button--primary:hover { background: #1d4ed8; }.mcp-button--secondary { background: #fff; border-color: #cbd5e1; color: #334155; }.mcp-button--secondary:hover { border-color: var(--mcp-blue); color: var(--mcp-blue); }.mcp-button--danger { color: #b91c1c; }.mcp-button--danger:hover { background: #fff1f2; }
.mcp-status { align-items: center; color: #0f766e; display: inline-flex; font-size: .7rem; font-weight: 700; gap: .38rem; }.mcp-status i { background: currentColor; border-radius: 50%; display: inline-block; height: .45rem; width: .45rem; }.mcp-status--connected { color: #0f766e; }.mcp-status--checking { color: #b45309; }.mcp-status--failed { color: #b91c1c; }.mcp-status--disabled { color: #64748b; }.mcp-status--compact { font-size: 0; }
.mcp-view__workspace { display: grid; grid-template-columns: minmax(16rem, 18rem) minmax(0, 1fr); min-height: 0; padding: 1.2rem; gap: 1rem; }.mcp-view__list, .mcp-view__form, .mcp-view__inspection { background: #fff; border: 1px solid #e2e8f0; border-radius: .9rem; box-shadow: 0 1px 2px rgb(15 23 42 / 4%); min-width: 0; }.mcp-view__list { align-content: start; display: grid; gap: .4rem; overflow-y: auto; padding: .75rem; }.mcp-view__list-heading { align-items: start; color: #64748b; display: flex; justify-content: space-between; padding: .35rem .45rem .7rem; }.mcp-view__list-heading strong, .mcp-view__list-heading small { display: block; }.mcp-view__list-heading strong { color: #0f172a; font-size: .82rem; }.mcp-view__list-heading small { font-size: .68rem; margin-top: .2rem; }.mcp-view__connection { align-items: center; background: transparent; border-radius: .65rem; display: grid; gap: .6rem; grid-template-columns: auto minmax(0, 1fr) auto; min-height: 4.35rem; padding: .65rem .6rem; text-align: left; transition: background var(--transition-fast), box-shadow var(--transition-fast); }.mcp-view__connection:hover { background: #f8fafc; }.mcp-view__connection--active { background: var(--mcp-blue-soft); box-shadow: inset 2px 0 0 var(--mcp-blue); }.mcp-view__connection-icon { align-items: center; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: .55rem; color: var(--mcp-blue); display: inline-flex; height: 2.2rem; justify-content: center; width: 2.2rem; }.mcp-view__connection-copy { min-width: 0; }.mcp-view__connection-copy strong, .mcp-view__connection-copy small { display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }.mcp-view__connection-copy strong { font-size: .8rem; }.mcp-view__connection-copy small { color: #94a3b8; font-size: .67rem; margin-top: .2rem; }.mcp-view__list-empty, .mcp-view__empty { align-items: center; color: #94a3b8; display: flex; flex-direction: column; gap: .45rem; justify-content: center; min-height: 12rem; padding: 1.2rem; text-align: center; }.mcp-view__list-empty strong, .mcp-view__empty strong { color: #334155; font-size: .83rem; }.mcp-view__list-empty span, .mcp-view__empty span { font-size: .72rem; line-height: 1.5; }
.mcp-view__editor { display: grid; gap: 1rem; grid-template-columns: minmax(30rem, 1fr) minmax(20rem, .78fr); min-height: 0; overflow: hidden; }.mcp-view__form, .mcp-view__inspection { overflow-y: auto; padding: 1.4rem; }.mcp-view__section-header { align-items: center; display: flex; justify-content: space-between; }.mcp-view__section-header h3 { font-size: 1rem; font-weight: 650; margin: 0; }.mcp-toggle { align-items: center; color: #475569; display: flex; font-size: .76rem; font-weight: 600; gap: .4rem; }.mcp-toggle input { accent-color: var(--mcp-blue); height: 1rem; width: 1rem; }.mcp-section { border-top: 1px solid #eef2f7; margin-top: 1.35rem; padding-top: 1.15rem; }.mcp-section__title h4 { font-size: .92rem; font-weight: 650; margin: 0; }.mcp-section__title p { color: #94a3b8; font-size: .72rem; margin: .25rem 0 .8rem; }.mcp-fields { display: grid; gap: .8rem; grid-template-columns: repeat(2, minmax(0, 1fr)); }.mcp-fields label, .mcp-field-wide { color: #475569; display: grid; font-size: .75rem; font-weight: 600; gap: .4rem; }.mcp-field-wide { margin-top: .8rem; }.mcp-fields input, .mcp-fields select, .mcp-field-wide input { background: #fff; border: 1px solid #dde4ee; border-radius: .6rem; color: #0f172a; font: inherit; min-height: 2.65rem; padding: 0 .75rem; width: 100%; }.mcp-fields input:focus, .mcp-fields select:focus, .mcp-field-wide input:focus { border-color: var(--mcp-blue); box-shadow: 0 0 0 3px rgb(37 99 235 / 12%); outline: none; }.mcp-view__commands { align-items: center; border-top: 1px solid #eef2f7; display: flex; flex-wrap: wrap; gap: .5rem; justify-content: flex-end; margin-top: 1.5rem; padding-top: 1rem; }.mcp-button--danger { margin-right: auto; }
.mcp-view__inspection { background: #fbfdff; }.mcp-capability-summary { align-items: center; background: #ecfdf5; border: 1px solid #bbf7d0; border-radius: .65rem; color: #047857; display: flex; justify-content: space-between; margin-top: 1.2rem; padding: .8rem; }.mcp-capability-summary strong, .mcp-capability-summary span { display: block; }.mcp-capability-summary strong { font-size: .82rem; }.mcp-capability-summary span { font-size: .68rem; margin-top: .2rem; }.mcp-tool-list { display: grid; gap: .6rem; margin-top: 1rem; }.mcp-tool-card { align-items: start; background: #fff; border: 1px solid #e5eaf2; border-radius: .7rem; display: grid; gap: .6rem; grid-template-columns: auto minmax(0, 1fr) auto; padding: .75rem; }.mcp-tool-card__icon { align-items: center; background: #eff6ff; border-radius: .5rem; color: var(--mcp-blue); display: inline-flex; height: 2rem; justify-content: center; width: 2rem; }.mcp-tool-card strong { color: #0f172a; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .76rem; }.mcp-tool-card p { color: #64748b; font-size: .72rem; line-height: 1.45; margin: .25rem 0; }.mcp-tool-card small { color: #94a3b8; font-size: .66rem; }.mcp-tool-card > svg { color: #0f766e; }.mcp-skeleton { display: grid; gap: .7rem; margin-top: 1.2rem; }.mcp-skeleton span { animation: pulse 1.2s ease-in-out infinite; background: #e2e8f0; border-radius: .6rem; height: 4.2rem; }.mcp-skeleton span:nth-child(2) { animation-delay: .15s; }.mcp-skeleton span:nth-child(3) { animation-delay: .3s; }.spin { animation: spin .8s linear infinite; } @keyframes spin { to { transform: rotate(360deg); } } @keyframes pulse { 50% { opacity: .45; } }
@media (max-width: 1180px) { .mcp-view__workspace { grid-template-columns: minmax(14rem, 17rem) minmax(0, 1fr); }.mcp-view__editor { grid-template-columns: minmax(0, 1fr); overflow-y: auto; }.mcp-view__form { overflow: visible; }.mcp-view__inspection { overflow: visible; } }
@media (max-width: 760px) { .mcp-view { height: auto; }.mcp-view__header { align-items: flex-start; flex-direction: column; gap: 1rem; }.mcp-view__header-actions { justify-content: space-between; width: 100%; }.mcp-view__workspace { display: block; padding: .75rem; }.mcp-view__list { margin-bottom: .75rem; max-height: 17rem; }.mcp-view__editor { display: block; }.mcp-view__form { margin-bottom: .75rem; }.mcp-fields { grid-template-columns: minmax(0, 1fr); } }
</style>
