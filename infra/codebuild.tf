# Resource type is aws_codebuild_project
# Resource name is the local identifier: app_build

resource "aws_codebuild_project" "app_build" {
  name         = "${var.github_repo}-build"
  service_role = aws_iam_role.codebuild_role.arn # we have to provide it with an iam role
  # 1) Artifacts must be CODEPIPELINE when triggered by CodePipeline
  artifacts {
    type = "CODEPIPELINE"
  }
  source {
    type      = "CODEPIPELINE"
    buildspec = file("buildspec.yml")
  }
  environment { # defines environment for the code to run on
    compute_type    = "BUILD_GENERAL1_SMALL"
    image           = "aws/codebuild/standard:6.0"
    type            = "LINUX_CONTAINER"
    privileged_mode = true # required for Docker builds
    environment_variable {
      name  = "POSTGRES_USER"
      value = var.POSTGRES_USER
    }
    environment_variable {
      name  = "POSTGRES_PASSWORD"
      value = aws_secretsmanager_secret.db_password.arn
    }
    environment_variable {
      name  = "POSTGRES_DB"
      value = var.POSTGRES_DB
    }
    environment_variable {
      name  = "POSTGRES_HOST"
      value = "localhost"
    }
    environment_variable {
      name  = "POSTGRES_PORT"
      value = var.POSTGRES_PORT
    }
    environment_variable {
      name  = "ENV"
      value = "ci"
    }
    # Full SQLAlchemy URL so migrations know the port
    environment_variable {
      name = "DATABASE_URL"
      # interpolate all your Postgres vars into one URL
      value = "postgresql://${var.POSTGRES_USER}:${var.POSTGRES_PASSWORD}@${var.POSTGRES_HOST}:${var.POSTGRES_PORT}/${var.POSTGRES_DB}"
    }
    environment_variable {
      name  = "SECRET_KEY"
      type  = "SECRETS_MANAGER"
      value = aws_secretsmanager_secret.app_secret_key.arn
    }
    environment_variable {
      name  = "ALGORITHM"
      value = var.ALGORITHM
    }
    environment_variable {
      name  = "ACCESS_TOKEN_EXPIRE_MINUTES"
      value = var.ACCESS_TOKEN_EXPIRE_MINUTES
    }
    environment_variable {
      name = "REPO_URI"
      # This comes from the aws_ecr_repository resource in YOUR account (468…)
      value = aws_ecr_repository.app_repo.repository_url
    }
  }
  logs_config {
    cloudwatch_logs {
      group_name  = "/aws/codebuild/${var.github_repo}-build"
      stream_name = "build-logs"
    }
  }

  tags = {
    Project     = var.github_repo
    Environment = "ci"
  }
}
