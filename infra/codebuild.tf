resource "aws_codebuild_project" "app_build" {
  name         = "${var.github_repo}-build"
  service_role = aws_iam_role.codebuild_role.arn

  # 1) Artifacts must be CODEPIPELINE when triggered by CodePipeline
  artifacts {
    type = "CODEPIPELINE"
  }

  # 2) Source must be CODEPIPELINE as well
  source {
    type      = "CODEPIPELINE"
    buildspec = file("buildspec.yml")
  }

  environment {
    compute_type    = "BUILD_GENERAL1_SMALL"
    image           = "aws/codebuild/standard:6.0"
    type            = "LINUX_CONTAINER"
    privileged_mode = true

    environment_variable {
      name  = "POSTGRES_USER"
      value = var.POSTGRES_USER
    }
    environment_variable {
      name  = "POSTGRES_PASSWORD"
      value = var.POSTGRES_PASSWORD
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
      value = var.SECRET_KEY
    }
    environment_variable {
      name  = "ALGORITHM"
      value = var.ALGORITHM
    }
    environment_variable {
      name  = "ACCESS_TOKEN_EXPIRE_MINUTES"
      value = var.ACCESS_TOKEN_EXPIRE_MINUTES
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
