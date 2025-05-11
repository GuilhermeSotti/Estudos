output "vpc_id" {
  value = aws_vpc.main.id
}

output "s3_bucket" {
  value = aws_s3_bucket.datalake.bucket
}

output "redshift_endpoint" {
  value = aws_redshift_cluster.main.endpoint
}

output "mqtt_endpoint" {
  value = aws_iot_endpoint.api_endpoint
}
