variable "aws_region" {
  description = "Região AWS"
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnets" {
  description = "Lista de CIDRs para subnets públicas"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnets" {
  description = "Lista de CIDRs para subnets privadas"
  type        = list(string)
  default     = ["10.0.3.0/24", "10.0.4.0/24"]
}

variable "s3_bucket_name" {
  description = "Nome do bucket S3 para Data Lake"
  type        = string
  default     = "industrial-data-lake-${random_id.bucket_suffix.hex}"
}

variable "redshift_cluster_id" {
  description = "ID do cluster Redshift"
  type        = string
  default     = "industrial-redshift"
}
