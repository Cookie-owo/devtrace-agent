<script setup lang="ts">
import { AlertTriangle, BookOpen, Database, FileText, FileWarning, Layers3, UploadCloud } from "lucide-vue-next";
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import { useRoute } from "vue-router";

import type { DocumentIndexTask, KnowledgeDocument } from "@agent-py/api-contracts";

import AppEmptyState from "../components/AppEmptyState.vue";
import AppErrorState from "../components/AppErrorState.vue";
import AppLoadingState from "../components/AppLoadingState.vue";
import KnowledgeDocumentList from "../components/KnowledgeDocumentList.vue";
import KnowledgeUpload from "../components/KnowledgeUpload.vue";
import { useKnowledgeStore } from "../stores/knowledge";

const knowledge = useKnowledgeStore();
const route = useRoute();
const pendingDeletion = ref<KnowledgeDocument | null>(null);

onMounted(() => { void initializeFromCitation().catch(() => undefined); });
onBeforeUnmount(() => { knowledge.stopPolling(); });

function run(operation: () => Promise<unknown>): void { void operation().catch(() => undefined); }
function openDocument(document: KnowledgeDocument): void { run(() => knowledge.openDocument(document)); }

async function initializeFromCitation(): Promise<void> {
  await knowledge.initialize();
  const knowledgeBaseId = route.query.knowledgeBaseId;
  if (typeof knowledgeBaseId === "string" && knowledgeBaseId !== knowledge.selectedKnowledgeBaseId) {
    await knowledge.selectKnowledgeBase(knowledgeBaseId);
  }
  const documentId = route.query.documentId;
  if (typeof documentId !== "string") return;
  const document = knowledge.documents.find((item) => item.id === documentId);
  if (document !== undefined) await knowledge.openDocument(document);
}

function confirmDelete(): void {
  const document = pendingDeletion.value;
  if (document === null) return;
  run(async () => {
    await knowledge.deleteDocument(document);
    pendingDeletion.value = null;
  });
}

function uploadDocument(file: File, chunking: import("@agent-py/api-contracts").DocumentChunkingConfiguration): void {
  run(() => knowledge.upload(file, chunking));
}
</script>

<template>
  <section class="knowledge-view" aria-label="知识库工作区">
    <header class="knowledge-view__header">
      <div><p>Knowledge Workspace</p><h2>文档与索引</h2><span>把团队经验沉淀成可检索、可引用的智能上下文。</span></div>
      <div class="knowledge-view__header-actions"><span class="knowledge-view__sync"><span></span>索引服务在线</span><label v-if="knowledge.knowledgeBases.length > 1" class="knowledge-view__base"><span>当前知识库</span><select :value="knowledge.selectedKnowledgeBaseId ?? ''" :disabled="knowledge.isLoading" aria-label="当前知识库" @change="run(() => knowledge.selectKnowledgeBase(($event.target as HTMLSelectElement).value))"><option v-for="base in knowledge.knowledgeBases" :key="base.id" :value="base.id">{{ base.name }}</option></select></label></div>
    </header>
    <div class="knowledge-view__metrics" aria-label="知识库概览"><article><span class="knowledge-view__metric-icon"><FileText :size="16" aria-hidden="true" /></span><div><small>已上传文档</small><strong>{{ knowledge.documents.length }}</strong></div></article><article><span class="knowledge-view__metric-icon knowledge-view__metric-icon--blue"><Layers3 :size="16" aria-hidden="true" /></span><div><small>索引状态</small><strong>{{ knowledge.indexTasks.filter((task) => task.status === 'succeeded').length }} 已完成</strong></div></article><article><span class="knowledge-view__metric-icon knowledge-view__metric-icon--purple"><BookOpen :size="16" aria-hidden="true" /></span><div><small>检索方式</small><strong>语义 + 关键词</strong></div></article></div>

    <AppLoadingState v-if="knowledge.isLoading && knowledge.documents.length === 0" label="正在加载知识库" />
    <AppErrorState v-else-if="knowledge.errorMessage && knowledge.documents.length === 0" :can-retry="true" :message="knowledge.errorMessage" @retry="run(knowledge.initialize)" />
    <template v-else>
      <KnowledgeUpload :disabled="knowledge.isUploading || knowledge.selectedKnowledgeBaseId === null" :is-uploading="knowledge.isUploading" @upload="uploadDocument" />
      <section v-if="knowledge.pendingOverwriteFile" class="knowledge-view__confirmation" role="alert"><FileWarning :size="18" aria-hidden="true" /><div><strong>发现同名文档</strong><p>{{ knowledge.pendingOverwriteFile.name }} 会替换现有文档及其向量数据。</p></div><div><button type="button" @click="knowledge.clearPendingOverwrite">取消</button><button type="button" class="knowledge-view__danger-command" @click="run(knowledge.overwritePendingUpload)">确认替换</button></div></section>
      <div class="knowledge-view__body">
        <section class="knowledge-view__documents" aria-labelledby="knowledge-documents-heading">
          <header><div><p>已上传文档</p><h3 id="knowledge-documents-heading">{{ knowledge.documents.length }} 份资料</h3></div><Database :size="19" aria-hidden="true" /></header>
          <div v-if="knowledge.documents.length === 0" class="knowledge-view__empty"><div class="knowledge-view__empty-icon"><UploadCloud :size="24" aria-hidden="true" /></div><strong>建立你的第一份知识资产</strong><p>上传 SOP、故障复盘或运行手册，之后它们会成为对话和诊断中的可信来源。</p><span><Database :size="14" aria-hidden="true" />支持 Markdown 与 PDF，单个文件不超过 10 MB</span></div>
          <KnowledgeDocumentList v-else :documents="knowledge.documents" :index-tasks="knowledge.indexTasks" :preview="knowledge.chunkPreview" :selected-document="knowledge.selectedDocument" @close="knowledge.closeDocument" @delete="pendingDeletion = $event" @detail="openDocument" @rebuild="run(() => knowledge.rebuildDocumentIndex($event))" @retry="run(() => knowledge.retryIndexTask($event))" />
        </section>
      </div>
    </template>

    <section v-if="pendingDeletion" class="knowledge-view__confirmation knowledge-view__confirmation--delete" role="alertdialog" aria-label="确认删除文档"><AlertTriangle :size="18" aria-hidden="true" /><div><strong>删除 {{ pendingDeletion.filename }}？</strong><p>此操作会删除文档记录和已建立的向量索引。</p></div><div><button type="button" @click="pendingDeletion = null">取消</button><button type="button" class="knowledge-view__danger-command" @click="confirmDelete">确认删除</button></div></section>
  </section>
</template>

<style scoped>
.knowledge-view { background: #f6f8fc; box-sizing: border-box; display: flex; flex-direction: column; gap: 1rem; height: 100%; min-height: 0; overflow: hidden; padding: clamp(1rem, 2.2vw, 2rem); }
.knowledge-view__header { align-items: end; display: flex; gap: 1.5rem; justify-content: space-between; } .knowledge-view__header-actions { align-items: center; display: flex; gap: .9rem; } .knowledge-view__sync { align-items: center; color: #0f766e; display: inline-flex; font-size: .72rem; font-weight: 650; gap: .35rem; white-space: nowrap; } .knowledge-view__sync > span { background: #10b981; border-radius: 50%; box-shadow: 0 0 0 .25rem rgb(16 185 129 / 12%); height: .45rem; width: .45rem; }
.knowledge-view__header p, .knowledge-view__documents > header p { color: var(--text-tertiary); font-size: 0.72rem; font-weight: 700; margin: 0 0 0.35rem; }
h2 { color: #0f172a; font-size: clamp(1.55rem, 3vw, 2rem); font-weight: 700; letter-spacing: -.035em; margin: 0; } .knowledge-view__metrics { display: grid; gap: .75rem; grid-template-columns: repeat(3, minmax(0, 1fr)); } .knowledge-view__metrics article { align-items: center; background: #fff; border: 1px solid #e2e8f0; border-radius: .8rem; box-shadow: 0 1px 2px rgb(15 23 42 / 4%); display: flex; gap: .7rem; min-height: 4.1rem; padding: .75rem .85rem; } .knowledge-view__metric-icon { align-items: center; background: #f1f5f9; border-radius: .55rem; color: #475569; display: inline-flex; height: 2.15rem; justify-content: center; width: 2.15rem; } .knowledge-view__metric-icon--blue { background: #eff6ff; color: #2563eb; } .knowledge-view__metric-icon--purple { background: #f5f3ff; color: #7c3aed; } .knowledge-view__metrics small, .knowledge-view__metrics strong { display: block; } .knowledge-view__metrics small { color: #94a3b8; font-size: .68rem; } .knowledge-view__metrics strong { color: #0f172a; font-size: .82rem; margin-top: .25rem; }
.knowledge-view__header > div > span { color: var(--text-secondary); display: block; font-size: 0.88rem; line-height: 1.6; margin-top: 0.45rem; max-width: 42rem; }
.knowledge-view__base { display: grid; gap: 0.35rem; min-width: min(16rem, 100%); }
.knowledge-view__base > span { color: var(--text-tertiary); font-size: 0.7rem; font-weight: 700; }
select { background: var(--surface-raised); border: 1px solid var(--line-strong); border-radius: 0.45rem; color: var(--text-primary); min-height: 2.55rem; padding: 0 0.65rem; }
.knowledge-view__body { background: #fff; border: 1px solid #e2e8f0; border-radius: .9rem; box-shadow: 0 1px 2px rgb(15 23 42 / 4%); display: grid; flex: 1 1 auto; min-height: 0; min-width: 0; overflow: hidden; }
.knowledge-view__documents { display: grid; grid-template-rows: auto minmax(0, 1fr); min-height: 0; min-width: 0; overflow: hidden; }
.knowledge-view__documents > header { align-items: center; border-bottom: 1px solid var(--line); display: flex; justify-content: space-between; min-height: 4.25rem; padding: 0.8rem 1rem; }
.knowledge-view__documents > header h3 { font-size: 0.98rem; font-weight: 680; margin: 0; }
.knowledge-view__empty { align-items: center; align-self: center; display: flex; flex-direction: column; gap: .55rem; justify-self: center; max-width: 28rem; padding: 2rem; text-align: center; } .knowledge-view__empty-icon { align-items: center; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: .8rem; color: #2563eb; display: inline-flex; height: 3.1rem; justify-content: center; margin-bottom: .35rem; width: 3.1rem; } .knowledge-view__empty strong { color: #0f172a; font-size: 1rem; } .knowledge-view__empty p { color: #64748b; font-size: .8rem; line-height: 1.6; margin: 0; } .knowledge-view__empty > span { align-items: center; color: #94a3b8; display: inline-flex; font-size: .68rem; gap: .3rem; margin-top: .2rem; }
.knowledge-view__confirmation { align-items: center; background: var(--status-waiting-bg); border: 1px solid var(--status-waiting-border); border-radius: var(--radius-md); display: grid; gap: 0.8rem; grid-template-columns: auto minmax(0, 1fr) auto; padding: 0.75rem 1rem; }
.knowledge-view__confirmation > svg { color: var(--status-waiting-text); }
.knowledge-view__confirmation strong { font-size: 0.84rem; }
.knowledge-view__confirmation p { color: var(--text-secondary); font-size: 0.78rem; margin: 0.25rem 0 0; }
.knowledge-view__confirmation > div:last-child { display: flex; gap: 0.45rem; }
.knowledge-view__confirmation button { border: 1px solid var(--line-strong); border-radius: 0.4rem; font-size: 0.78rem; min-height: 2rem; padding: 0 0.55rem; white-space: nowrap; }
.knowledge-view__confirmation button:hover { background: rgb(255 255 255 / 65%); }
.knowledge-view__confirmation .knowledge-view__danger-command { border-color: var(--danger); color: var(--danger); }
.knowledge-view__confirmation--delete { background: var(--danger-soft); border-color: var(--status-danger-border); }
@media (max-width: 680px) { .knowledge-view { height: auto; min-height: 100%; overflow-y: auto; } .knowledge-view__header-actions { align-items: stretch; flex-direction: column; gap: .55rem; } .knowledge-view__metrics { grid-template-columns: 1fr; } .knowledge-view__body { flex: 0 0 auto; overflow: visible; } .knowledge-view__documents { display: block; overflow: visible; } .knowledge-view__header { align-items: stretch; flex-direction: column; gap: 1rem; } .knowledge-view__base { min-width: 0; } .knowledge-view__confirmation { align-items: start; grid-template-columns: auto minmax(0, 1fr); } .knowledge-view__confirmation > div:last-child { flex-wrap: wrap; grid-column: 2; } }
</style>




