# 3.1 Use the default VPC so we don't need to define one from scratch
data "aws_vpc" "default" {
  default = true
}

# 3.2 Grab its public subnets
data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# 3.3 Security Group for ECS tasks
resource "aws_security_group" "ecs_sg" {
  name        = "${local.repo_sanitized}-ecs-sg"
  description = "Allow inbound HTTP to ECS tasks"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "HTTP from anywhere (for ALB or curl)"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "All egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 3.4 Create the ECS cluster
resource "aws_ecs_cluster" "app" {
  name = "${local.repo_sanitized}-cluster"
}
