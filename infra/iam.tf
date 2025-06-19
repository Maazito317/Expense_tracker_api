# Allowing the role to be assumed
data "aws_iam_policy_document" "codebuild_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["codebuild.amazonaws.com"]
    }
  }
}
# CodeBuild service role: creating the role
resource "aws_iam_role" "codebuild_role" {
  name               = "${var.github_repo}-codebuild-role"
  assume_role_policy = data.aws_iam_policy_document.codebuild_assume.json
}

# attaching the policy to the role define above
resource "aws_iam_role_policy_attachment" "codebuild_attach" {
  role       = aws_iam_role.codebuild_role.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess" # for initial learning
}

# CodePipeline service role
data "aws_iam_policy_document" "pipeline_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["codepipeline.amazonaws.com"]
    }
  }
}
resource "aws_iam_role" "pipeline_role" {
  name               = "${var.github_repo}-pipeline-role"
  assume_role_policy = data.aws_iam_policy_document.pipeline_assume.json
}

resource "aws_iam_role_policy_attachment" "pipeline_attach" {
  role       = aws_iam_role.pipeline_role.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

resource "aws_iam_policy" "codebuild_secrets_access" {
  name        = "${var.github_repo}-codebuild-secrets"
  description = "Allow CodeBuild to read secrets"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = ["secretsmanager:GetSecretValue"]
        Effect = "Allow"
        Resource = [
          aws_secretsmanager_secret.app_secret_key.arn,
          aws_secretsmanager_secret.db_password.arn
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "codebuild_secrets_attach" {
  role       = aws_iam_role.codebuild_role.name
  policy_arn = aws_iam_policy.codebuild_secrets_access.arn
}