# 3.2.1 IAM Role for ECS to pull images and write logs
# Without it, your container can’t fetch its image or send its logs to CloudWatch.
resource "aws_iam_role" "ecs_task_execution" {
  name = "${local.repo_sanitized}-ecs-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

# Attach the managed policy so ECS can pull & log
resource "aws_iam_role_policy_attachment" "ecs_task_exec_attach" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}
resource "aws_iam_role_policy_attachment" "ecr_pull_attach" {
  role       = aws_iam_role.ecs_task_execution.name                         # Same role as before
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly" # Adds ECR pull access
}
# 3.2.2 CloudWatch Log Group for your containers; Keeps logs centralized and lets you set retention.
resource "aws_cloudwatch_log_group" "ecs" {
  name              = "/ecs/${local.repo_sanitized}"
  retention_in_days = 7
}

# 3.2.3 The Task Definition itself
resource "aws_ecs_task_definition" "app" {
  family                   = local.repo_sanitized
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "256" # 0.25 vCPU
  memory                   = "512" # 512 MiB
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  task_role_arn            = aws_iam_role.ecs_task_execution.arn
  # If your app needs AWS API permissions at runtime, define a separate task_role_arn here

  container_definitions = jsonencode([
    {
      name      = local.repo_sanitized
      image     = aws_ecr_repository.app_repo.repository_url # ECR repo URL
      essential = true
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.ecs.name
          "awslogs-region"        = var.aws_region # assume you declared this
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
}
