############################
# infra/pipeline.tf
############################

resource "aws_codepipeline" "ci_pipeline" {
  name     = "${var.github_repo}-pipeline"
  role_arn = aws_iam_role.pipeline_role.arn

  # 1. Artifact store: where pipeline keeps and passes files
  artifact_store {
    type     = "S3"
    location = aws_s3_bucket.ci_artifacts.bucket
  }

  # 2. Source stage: pull code from GitHub
  stage {
    name = "Source"
    action {
      name             = "GitHubSource"
      category         = "Source"
      owner            = "ThirdParty"
      provider         = "GitHub"
      version          = "1"
      output_artifacts = ["source_output"]
      configuration = {
        Owner      = var.github_owner
        Repo       = var.github_repo
        Branch     = "main"
        OAuthToken = var.github_oauth_token
      }
    }
  }

  # 3. Build stage: run CodeBuild on the pulled source
  stage {
    name = "Build"
    action {
      name             = "CodeBuild"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      input_artifacts  = ["source_output"]
      output_artifacts = ["build_output"]
      configuration = {
        ProjectName = aws_codebuild_project.app_build.name
      }
    }
  }
}
