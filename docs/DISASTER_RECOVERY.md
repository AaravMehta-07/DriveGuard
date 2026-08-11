# Disaster Recovery

## Database Backups
- **Automated**: Daily full, WAL archiving for PITR (Point-In-Time Recovery).
- **Retention**: 30 days.
- **Encrypted**: All backups encrypted at rest via KMS.

## Restore Procedure
1. Provision new DB instance.
2. Restore base backup.
3. Replay WAL up to target timestamp.

## S3 Backup/Versioning
- All S3 buckets have versioning enabled.
- Lifecycle policies transition old versions to Glacier.

## Migration Rollback
- Down revisions must be tested for all schema changes.

## Staging Restore Test Procedure
- Bi-weekly automated restore of production snapshot to a sterile staging environment to verify backup integrity.
