export interface CiDiagnosisTaskRequest {
  readonly repositoryPath: string;
  readonly failureSummary: string;
  readonly testLog: string;
  readonly testName?: string;
  readonly commitSha?: string;
  readonly baseCommitSha?: string;
}

export interface CiDiagnosisTask {
  readonly id: string;
  readonly status: string;
  readonly repository_path: string;
  readonly failure_summary: string;
  readonly result_payload: Record<string, unknown>;
  readonly [key: string]: unknown;
}

export interface CiDiagnosisCreatedTask {
  readonly taskId: string;
  readonly status: string;
  readonly jobId: string;
}

export interface CiDiagnosisRecord { readonly [key: string]: unknown; }
