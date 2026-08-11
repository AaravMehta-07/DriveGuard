export interface EnforcementPoint {
  id: string;
  type: string;
  latitude: number;
  longitude: number;
  confidence: number;
  status: 'verified' | 'probable' | 'needs_review' | 'stale';
  source: string;
  lastVerified?: string;
  disputed?: boolean;
}

export interface ReviewQueueItem {
  id: string;
  itemType: string;
  reason: string;
  status: 'pending' | 'approved' | 'rejected' | 'deferred';
  createdDate: string;
  assignedTo?: string;
}

export interface AuditLogEntry {
  id: string;
  entityType: string;
  entityId: string;
  action: string;
  actor: string;
  timestamp: string;
  diff: {
    before: Record<string, any>;
    after: Record<string, any>;
  };
}

export interface CoverageMetrics {
  roadNetworkPercent: number;
  speedLimitPercent: number;
  signalPercent: number;
  cameraCounts: {
    verified: number;
    probable: number;
    needsReview: number;
  };
  tempOrdersStats: {
    active: number;
    expired: number;
  };
}

export interface IngestionJob {
  id: string;
  source: string;
  status: 'running' | 'success' | 'failed';
  successRate: number;
  unprocessedDocs: number;
  lastRun: string;
}

export interface FieldVerificationTask {
  id: string;
  locationId: string;
  assignedTo: string;
  status: 'pending' | 'in_progress' | 'completed';
  notes: string;
}
