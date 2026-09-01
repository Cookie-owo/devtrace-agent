<script setup lang="ts">
import { Activity, ArrowRight, BookOpen, Eye, EyeOff, LoaderCircle, ShieldCheck, Sparkles } from "lucide-vue-next";
import { computed, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import { useAuthStore } from "../stores/auth";

const props = defineProps<{ readonly mode: "login" | "register" }>();
const auth = useAuthStore();
const route = useRoute();
const router = useRouter();
const form = reactive({ displayName: "", email: "", password: "" });
const passwordVisible = ref(false);
const isLogin = computed(() => props.mode === "login");
const heading = computed(() => (isLogin.value ? "欢迎回来" : "创建你的工作台"));
const submitLabel = computed(() => (isLogin.value ? "登录" : "注册并进入"));
const alternatePath = computed(() => (isLogin.value ? "/register" : "/login"));
const alternateLabel = computed(() => (isLogin.value ? "还没有账号？创建工作台" : "已有账号？直接登录"));

function intendedPath(): string {
  const redirect = route.query.redirect;
  return typeof redirect === "string" && redirect.startsWith("/") ? redirect : "/chat";
}

async function submit(): Promise<void> {
  try {
    if (isLogin.value) await auth.login({ email: form.email, password: form.password });
    else await auth.register({ displayName: form.displayName, email: form.email, password: form.password });
    await router.replace(intendedPath());
  } catch {
    // The auth store publishes the normalized API error to global feedback.
  }
}
</script>

<template>
  <main class="auth-view">
    <section class="auth-shell" :aria-labelledby="`${mode}-title`">
      <aside class="auth-shell__aside">
        <RouterLink class="auth-view__brand" to="/login" aria-label="DevPilot 首页"><span class="auth-view__brand-mark"><Sparkles :size="19" aria-hidden="true" /></span><span>DevPilot</span></RouterLink>
        <div class="auth-shell__message"><p>AI Developer Console</p><h2>让每一次排障，<br /><em>都有可靠的上下文。</em></h2><span>连接知识、工具与智能诊断，构建更快、更稳的研发工作流。</span></div>
        <div class="auth-shell__signals"><div><ShieldCheck :size="17" aria-hidden="true" /><span>安全的工作区隔离</span></div><div><Activity :size="17" aria-hidden="true" /><span>实时的系统洞察</span></div><div><BookOpen :size="17" aria-hidden="true" /><span>可追溯的知识引用</span></div></div>
        <small class="auth-shell__copyright">DEVTOOLS FOR EVERY TEAM · 2026</small>
      </aside>
      <div class="auth-shell__content">
        <div class="auth-shell__content-top"><span>{{ isLogin ? "已有工作区" : "开始使用 DevPilot" }}</span><span class="auth-shell__secure"><ShieldCheck :size="14" aria-hidden="true" />安全登录</span></div>
        <div class="auth-view__intro"><p>{{ isLogin ? "运维智能工作台" : "创建你的研发空间" }}</p><h1 :id="`${mode}-title`">{{ heading }}</h1><span>{{ isLogin ? "继续你的对话、知识与诊断工作。" : "用一个账号管理你的对话、知识与诊断记录。" }}</span></div>
        <form class="auth-view__form" @submit.prevent="submit">
          <label v-if="!isLogin"><span>昵称</span><input v-model.trim="form.displayName" autocomplete="name" required placeholder="你的称呼" /></label>
          <label><span>邮箱</span><input v-model.trim="form.email" autocomplete="email" inputmode="email" type="email" required placeholder="name@company.com" /></label>
          <label><span>密码</span><span class="auth-view__password"><input v-model="form.password" :autocomplete="isLogin ? 'current-password' : 'new-password'" minlength="8" :type="passwordVisible ? 'text' : 'password'" required placeholder="至少 8 位字符" /><button type="button" :aria-label="passwordVisible ? '隐藏密码' : '显示密码'" :title="passwordVisible ? '隐藏密码' : '显示密码'" @click="passwordVisible = !passwordVisible"><EyeOff v-if="passwordVisible" :size="17" aria-hidden="true" /><Eye v-else :size="17" aria-hidden="true" /></button></span></label>
          <button class="auth-view__submit" type="submit" :disabled="auth.isLoading"><span>{{ auth.isLoading ? (isLogin ? "正在登录" : "正在创建") : submitLabel }}</span><LoaderCircle v-if="auth.isLoading" class="auth-view__spin" :size="17" aria-hidden="true" /><ArrowRight v-else :size="17" aria-hidden="true" /></button>
        </form>
        <RouterLink class="auth-view__alternate" :to="alternatePath">{{ alternateLabel }} <ArrowRight :size="15" aria-hidden="true" /></RouterLink>
        <p class="auth-shell__legal">继续即表示你同意 DevPilot 的服务条款与隐私政策。</p>
      </div>
    </section>
  </main>
</template>

<style scoped>
.auth-view { align-items: center; background: #eef2f7; display: grid; min-height: 100dvh; padding: clamp(1rem, 4vw, 3rem); }
.auth-shell { background: #fff; border: 1px solid #dfe6ef; border-radius: 1.25rem; box-shadow: 0 24px 60px rgb(15 23 42 / 12%); display: grid; grid-template-columns: minmax(18rem, .86fr) minmax(25rem, 1.14fr); margin: 0 auto; max-width: 67rem; min-height: 38rem; overflow: hidden; width: 100%; }
.auth-shell__aside { background: #0b1220; color: #eaf2ff; display: flex; flex-direction: column; padding: clamp(1.6rem, 4vw, 3rem); position: relative; }.auth-view__brand { align-items: center; color: #f8fafc; display: inline-flex; font-size: 1.05rem; font-weight: 730; gap: .6rem; text-decoration: none; }.auth-view__brand-mark { align-items: center; background: #2563eb; border-radius: .6rem; color: #fff; display: inline-flex; height: 2.15rem; justify-content: center; width: 2.15rem; }.auth-shell__message { margin: auto 0; max-width: 24rem; }.auth-shell__message p { color: #60a5fa; font-size: .72rem; font-weight: 700; letter-spacing: .1em; margin: 0 0 1rem; text-transform: uppercase; }.auth-shell__message h2 { font-size: clamp(1.8rem, 3vw, 2.45rem); font-weight: 650; letter-spacing: -.04em; line-height: 1.2; margin: 0; }.auth-shell__message em { color: #93c5fd; font-style: normal; }.auth-shell__message > span { color: #94a3b8; display: block; font-size: .84rem; line-height: 1.7; margin-top: 1.2rem; }.auth-shell__signals { border-top: 1px solid rgb(148 163 184 / 18%); display: grid; gap: .75rem; padding-top: 1.3rem; }.auth-shell__signals div { align-items: center; color: #cbd5e1; display: flex; font-size: .76rem; gap: .6rem; }.auth-shell__signals svg { color: #60a5fa; }.auth-shell__copyright { color: #64748b; font-size: .62rem; letter-spacing: .08em; margin-top: 2rem; }
.auth-shell__content { display: flex; flex-direction: column; padding: clamp(1.5rem, 5vw, 4.2rem); }.auth-shell__content-top { align-items: center; color: #94a3b8; display: flex; font-size: .7rem; justify-content: space-between; }.auth-shell__secure { align-items: center; color: #0f766e; display: inline-flex; gap: .3rem; }.auth-view__intro { margin: clamp(3.5rem, 9vw, 6rem) 0 2.1rem; }.auth-view__intro p { color: #2563eb; font-size: .76rem; font-weight: 700; letter-spacing: .04em; margin: 0 0 .65rem; }.auth-view__intro h1 { color: #0f172a; font-size: clamp(2rem, 4vw, 2.7rem); font-weight: 700; letter-spacing: -.045em; line-height: 1.08; margin: 0; }.auth-view__intro > span { color: #64748b; display: block; font-size: .9rem; line-height: 1.65; margin-top: .85rem; }
.auth-view__form { display: grid; gap: 1.1rem; max-width: 28rem; }label { color: #475569; display: grid; font-size: .76rem; font-weight: 650; gap: .45rem; }input { background: #fff; border: 1px solid #d8e1ec; border-radius: .65rem; color: #0f172a; font: inherit; min-height: 2.85rem; padding: 0 .85rem; transition: border-color var(--transition-fast), box-shadow var(--transition-fast); width: 100%; }input::placeholder { color: #b0bac8; }input:focus { border-color: #2563eb; box-shadow: 0 0 0 3px rgb(37 99 235 / 12%); outline: none; }.auth-view__password { display: block; position: relative; }.auth-view__password input { padding-right: 2.85rem; }.auth-view__password button { align-items: center; border-radius: .45rem; color: #94a3b8; display: inline-flex; height: 2.35rem; justify-content: center; position: absolute; right: .25rem; top: .25rem; width: 2.35rem; }.auth-view__password button:hover { background: #f1f5f9; color: #334155; }.auth-view__submit { align-items: center; background: #2563eb; border-radius: .65rem; color: #fff; display: flex; font-size: .88rem; font-weight: 680; justify-content: space-between; margin-top: .35rem; min-height: 3rem; padding: 0 1rem; transition: background var(--transition-fast), transform var(--transition-fast); }.auth-view__submit:hover:not(:disabled) { background: #1d4ed8; transform: translateY(-1px); }.auth-view__submit:disabled { cursor: wait; opacity: .72; }.auth-view__spin { animation: auth-spin .8s linear infinite; }.auth-view__alternate { align-items: center; color: #2563eb; display: inline-flex; font-size: .82rem; font-weight: 650; gap: .35rem; margin-top: 1.5rem; text-decoration: none; }.auth-view__alternate:hover { color: #1d4ed8; }.auth-shell__legal { color: #94a3b8; font-size: .66rem; line-height: 1.5; margin: auto 0 0; }
@keyframes auth-spin { to { transform: rotate(360deg); } }
@media (max-width: 760px) { .auth-view { align-items: start; padding: 0; }.auth-shell { border: 0; border-radius: 0; box-shadow: none; display: block; min-height: 100dvh; }.auth-shell__aside { min-height: 15rem; padding: 1.4rem 1.25rem 1.5rem; }.auth-shell__message { margin: 2.8rem 0 0; }.auth-shell__message h2 { font-size: 1.65rem; }.auth-shell__signals, .auth-shell__copyright { display: none; }.auth-shell__content { padding: 1.6rem 1.25rem 2rem; }.auth-view__intro { margin: 2.8rem 0 1.8rem; }.auth-view__intro h1 { font-size: 2rem; }.auth-shell__legal { margin-top: 3rem; } }
</style>

