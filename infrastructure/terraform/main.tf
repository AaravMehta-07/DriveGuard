terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# --- VPC & Networking ---
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "driveguard-vpc-${var.environment}"
  cidr = "10.0.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true

  tags = {
    Environment = var.environment
    Project     = "DriveGuard"
  }
}

# --- RDS PostgreSQL with PostGIS ---
resource "aws_db_instance" "postgres" {
  identifier           = "driveguard-db-${var.environment}"
  engine               = "postgres"
  engine_version       = "16.3" # Supports PostGIS
  instance_class       = var.db_instance_class
  allocated_storage    = 50
  max_allocated_storage = 200
  storage_type         = "gp3"
  
  db_name              = "driveguard"
  username             = var.db_username
  password             = var.db_password # In production, read from Secrets Manager
  
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = module.vpc.database_subnet_group_name != "" ? module.vpc.database_subnet_group_name : aws_db_subnet_group.default.name
  
  multi_az             = var.environment == "prod" ? true : false
  publicly_accessible  = false
  skip_final_snapshot  = false
  final_snapshot_identifier = "driveguard-db-final-snapshot-${var.environment}"
  
  storage_encrypted    = true
  
  tags = {
    Environment = var.environment
  }
}

resource "aws_db_subnet_group" "default" {
  name       = "driveguard-db-subnet-group-${var.environment}"
  subnet_ids = module.vpc.private_subnets

  tags = {
    Name = "driveguard-db-subnet-group"
  }
}

resource "aws_security_group" "rds_sg" {
  name        = "driveguard-rds-sg-${var.environment}"
  description = "Security group for RDS PostgreSQL"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_sg.id]
  }
}

# --- ElastiCache Redis ---
resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "driveguard-redis-${var.environment}"
  engine               = "redis"
  node_type            = var.redis_node_type
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  engine_version       = "7.0"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.redis_subnet_group.name
  security_group_ids   = [aws_security_group.redis_sg.id]
}

resource "aws_elasticache_subnet_group" "redis_subnet_group" {
  name       = "driveguard-redis-subnet-group-${var.environment}"
  subnet_ids = module.vpc.private_subnets
}

resource "aws_security_group" "redis_sg" {
  name        = "driveguard-redis-sg-${var.environment}"
  description = "Security group for Redis"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_sg.id]
  }
}

# --- S3 Bucket for Uploads & Offline Packs ---
resource "aws_s3_bucket" "storage" {
  bucket = "driveguard-storage-${var.environment}-${var.aws_region}"
}

resource "aws_s3_bucket_versioning" "storage_versioning" {
  bucket = aws_s3_bucket.storage.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "storage_lifecycle" {
  bucket = aws_s3_bucket.storage.id

  rule {
    id     = "expire_old_versions"
    status = "Enabled"
    
    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "storage_encryption" {
  bucket = aws_s3_bucket.storage.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# --- ECS Fargate ---
resource "aws_ecs_cluster" "cluster" {
  name = "driveguard-cluster-${var.environment}"
}

resource "aws_security_group" "ecs_sg" {
  name        = "driveguard-ecs-sg-${var.environment}"
  description = "Security group for ECS tasks"
  vpc_id      = module.vpc.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# --- Secrets Manager ---
resource "aws_secretsmanager_secret" "api_secrets" {
  name = "driveguard/api-secrets-${var.environment}"
}

# --- CloudFront CDN ---
resource "aws_cloudfront_distribution" "cdn" {
  origin {
    domain_name = aws_s3_bucket.storage.bucket_regional_domain_name
    origin_id   = "S3-DriveGuardStorage"
  }

  enabled             = true
  is_ipv6_enabled     = true
  
  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-DriveGuardStorage"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
    viewer_protocol_policy = "redirect-to-https"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}
