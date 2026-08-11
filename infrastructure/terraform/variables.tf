variable "aws_region" {
  description = "AWS region for infrastructure"
  type        = string
  default     = "ap-south-1" # India region (Mumbai)
}

variable "environment" {
  description = "Deployment environment (e.g., dev, staging, prod)"
  type        = string
  default     = "prod"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t4g.medium"
}

variable "db_username" {
  description = "PostgreSQL master username"
  type        = string
}

variable "db_password" {
  description = "PostgreSQL master password (use secrets manager in prod)"
  type        = string
  sensitive   = true
}

variable "redis_node_type" {
  description = "ElastiCache node type"
  type        = string
  default     = "cache.t4g.micro"
}
