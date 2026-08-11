import axios from 'axios';
import type { 
  CoverageMetrics, 
  EnforcementPoint, 
  ReviewQueueItem, 
  AuditLogEntry, 
  IngestionJob,
  FieldVerificationTask
} from './types';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  getCoverageMetrics: () => apiClient.get<CoverageMetrics>('/coverage').then(res => res.data),
  
  getEnforcementPoints: (filters?: Record<string, any>) => 
    apiClient.get<EnforcementPoint[]>('/enforcement', { params: filters }).then(res => res.data),
  
  updateEnforcementPoint: (id: string, data: Partial<EnforcementPoint>) =>
    apiClient.patch<EnforcementPoint>(`/enforcement/${id}`, data).then(res => res.data),
    
  getReviewQueue: (status?: string) => 
    apiClient.get<ReviewQueueItem[]>('/review-queue', { params: { status } }).then(res => res.data),
    
  getReviewItem: (id: string) => 
    apiClient.get<ReviewQueueItem>(`/review-queue/${id}`).then(res => res.data),
    
  processReviewDecision: (id: string, decision: 'approve' | 'reject' | 'defer', notes?: string) =>
    apiClient.post(`/review-queue/${id}/decision`, { decision, notes }).then(res => res.data),
    
  getIngestionJobs: () => 
    apiClient.get<IngestionJob[]>('/ingestion').then(res => res.data),
    
  triggerIngestionSync: (source: string) => 
    apiClient.post('/ingestion/sync', { source }).then(res => res.data),
    
  getAuditLogs: () => 
    apiClient.get<AuditLogEntry[]>('/audit-logs').then(res => res.data),
    
  getFieldTasks: () => 
    apiClient.get<FieldVerificationTask[]>('/field-tasks').then(res => res.data),
};
