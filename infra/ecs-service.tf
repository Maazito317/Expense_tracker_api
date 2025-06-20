resource "aws_ecs_service" "app" {
  name            = local.repo_sanitized
  cluster         = aws_ecs_cluster.app.id          #Tells ECS which cluster to run in
  task_definition = aws_ecs_task_definition.app.arn #Tells ECS which task definition to use
  launch_type     = "FARGATE"                       # Use Fargate for serverless container management
  desired_count   = 1                               # Number of tasks to run; scale as needed

  # 3.3.1 Network settings for Fargate (awsvpc)
  network_configuration {
    subnets = data.aws_subnets.default.ids # Use public subnets from the default VPC
    # If you had private subnets, you could use those too, but ensure NAT Gateway
    security_groups  = [aws_security_group.ecs_sg.id] # Applies your “allow port 8000” rules.
    assign_public_ip = false                          # Gives each task a public IP so you can hit it directly while we wire up the ALB.
  }

  # Attach each container to the ALB target group
  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn # from infra/alb.tf
    container_name   = local.repo_sanitized        # must match the name in your task def
    container_port   = 8000
  }

  # 3.3.2 Deployment settings (optional tuning)
  deployment_minimum_healthy_percent = 50
  deployment_maximum_percent         = 200

  # 3.3.3 Ensure IAM exec role is ready first
  depends_on = [
    aws_iam_role_policy_attachment.ecs_task_exec_attach
  ]
}
