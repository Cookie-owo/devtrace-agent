import type { CiDiagnosisCreatedTask, CiDiagnosisRecord, CiDiagnosisTask, CiDiagnosisTaskRequest } from "@agent-py/api-contracts";
import { AUTH_TOKEN_STORAGE_KEY } from "../authClient";
import { createApiClient } from "../api/apiClient";
import { createSseClient } from "../api/sseClient";
import { API_BASE_URL } from "../config";

export function createCiDiagnosisClient() {
  const getAccessToken = () => window.localStorage.getItem(AUTH_TOKEN_STORAGE_KEY);
  const options = { baseUrl: API_BASE_URL, getAccessToken };
  const api = createApiClient(options);
  const sse = createSseClient(options);
  return {
    create: (body: CiDiagnosisTaskRequest) => api.request<CiDiagnosisCreatedTask>("/ci-diagnosis/tasks", { method: "POST", body: JSON.stringify(body) }),
    get: (id: string) => api.request<CiDiagnosisTask>(`/ci-diagnosis/tasks/${id}`),
    steps: (id: string) => api.request<{ items: readonly CiDiagnosisRecord[] }>(`/ci-diagnosis/tasks/${id}/steps`),
    evidence: (id: string) => api.request<{ items: readonly CiDiagnosisRecord[] }>(`/ci-diagnosis/tasks/${id}/evidence`),
    tools: (id: string) => api.request<{ items: readonly CiDiagnosisRecord[] }>(`/ci-diagnosis/tasks/${id}/tool-calls`),
    cancel: (id: string) => api.request<CiDiagnosisTask>(`/ci-diagnosis/tasks/${id}:cancel`, { method: "POST" }),
    events: (id: string) => sse.stream(`/ci-diagnosis/tasks/${id}/events`)
  };
}
