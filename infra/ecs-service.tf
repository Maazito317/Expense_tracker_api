resource "aws_ecs_service" "app" {
  name            = local.repo_sanitized
  cluster         = aws_ecs_cluster.app.id
  task_definition = aws_ecs_task_definition.app.arn
  launch_type     = "FARGATE"
  desired_count   = 1

  # 3.3.1 Network settings for Fargate (awsvpc)
  network_configuration {
    subnets          = data.aws_subnets.default.ids
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = true
  }

  # 3.3.2 Deployment settings (optional tuning)
  deployment_minimum_healthy_percent = 50
  deployment_maximum_percent         = 200

  # 3.3.3 Ensure IAM exec role is ready first
  depends_on = [
    aws_iam_role_policy_attachment.ecs_task_exec_attach
  ]
}
