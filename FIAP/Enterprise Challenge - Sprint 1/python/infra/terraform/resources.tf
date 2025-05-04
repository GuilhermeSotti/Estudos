resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# VPC, Subnets e Internet Gateway
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  tags = { Name = "industrial-vpc" }
}

resource "aws_subnet" "public" {
  for_each = toset(var.public_subnets)
  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value
  map_public_ip_on_launch = true
  tags = { Name = "public-${each.value}" }
}

resource "aws_subnet" "private" {
  for_each = toset(var.private_subnets)
  vpc_id     = aws_vpc.main.id
  cidr_block = each.value
  tags = { Name = "private-${each.value}" }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
}

# Security Group para MQTT, Lambdas, Redshift
resource "aws_security_group" "iot_sg" {
  name        = "iot-sg"
  description = "Allow MQTT and API access"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 8883
    to_port     = 8883
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# IoT Core: Thing, Policy, Certificate
resource "aws_iot_thing" "esp32" {
  name = "esp32-sensor"
}

resource "aws_iot_policy" "mqtt_policy" {
  name   = "esp32-mqtt-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action   = ["iot:Connect", "iot:Publish", "iot:Subscribe", "iot:Receive"]
      Effect   = "Allow"
      Resource = "*"
    }]
  })
}

resource "aws_iot_certificate" "cert" {
  active = true
}

resource "aws_iot_policy_attachment" "attach" {
  policy_name = aws_iot_policy.mqtt_policy.name
  target      = aws_iot_certificate.cert.arn
}

resource "aws_iot_thing_principal_attachment" "attach_principal" {
  thing_name = aws_iot_thing.esp32.name
  principal  = aws_iot_certificate.cert.arn
}

# S3 Data Lake
resource "aws_s3_bucket" "datalake" {
  bucket = var.s3_bucket_name
  versioning { enabled = true }
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default { sse_algorithm = "AES256" }
    }
  }
}

# Redshift Cluster
resource "aws_redshift_cluster" "main" {
  cluster_identifier = var.redshift_cluster_id
  node_type          = "dc2.large"
  master_username    = "admin"
  master_password    = random_password.red_pw.result
  cluster_type       = "single-node"
  iam_roles          = [aws_iam_role.redshift_role.arn]
}

resource "random_password" "red_pw" {
  length           = 16
  override_characters = "!@#$%*()-_=+"
}

resource "aws_iam_role" "redshift_role" {
  name = "RedshiftCopyRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "redshift.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "redshift_s3" {
  role       = aws_iam_role.redshift_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}
