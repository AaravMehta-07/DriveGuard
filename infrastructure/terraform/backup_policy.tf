# Automated database backups, retention rules, encrypted snapshot policy

resource "aws_backup_vault" "driveguard_vault" {
  name        = "driveguard-backup-vault-${var.environment}"
  kms_key_arn = aws_kms_key.backup_key.arn
}

resource "aws_kms_key" "backup_key" {
  description             = "KMS key for DriveGuard backups"
  deletion_window_in_days = 10
  enable_key_rotation     = true
}

resource "aws_backup_plan" "driveguard_backup_plan" {
  name = "driveguard-daily-backup-plan-${var.environment}"

  rule {
    rule_name         = "daily_retention_30_days"
    target_vault_name = aws_backup_vault.driveguard_vault.name
    schedule          = "cron(0 12 * * ? *)" # Run daily
    
    lifecycle {
      delete_after = 30
    }
  }
}

resource "aws_backup_selection" "driveguard_backup_selection" {
  iam_role_arn = aws_iam_role.backup_role.arn
  name         = "driveguard-backup-selection-${var.environment}"
  plan_id      = aws_backup_plan.driveguard_backup_plan.id

  resources = [
    aws_db_instance.postgres.arn
  ]
}

data "aws_iam_policy_document" "backup_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["backup.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "backup_role" {
  name               = "driveguard-backup-role-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.backup_assume_role.json
}

resource "aws_iam_role_policy_attachment" "backup_role_policy" {
  role       = aws_iam_role.backup_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup"
}
