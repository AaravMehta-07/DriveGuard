output "vpc_id" {
  value = module.vpc.vpc_id
}

output "db_endpoint" {
  value       = aws_db_instance.postgres.endpoint
  description = "Endpoint for the PostgreSQL RDS instance"
}

output "redis_endpoint" {
  value       = aws_elasticache_cluster.redis.cache_nodes[0].address
  description = "Endpoint for the Redis ElastiCache cluster"
}

output "storage_bucket_name" {
  value       = aws_s3_bucket.storage.id
  description = "S3 bucket for uploads and offline packs"
}


