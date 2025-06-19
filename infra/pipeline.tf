resource "aws_codepipeline" "ci_pipeline" {
  name     = "${var.github_repo}-pipeline"
  role_arn = aws_iam_role.pipeline_role.arn #iam for permissions

  artifact_store {
    type     = "S3"
    location = aws_s3_bucket.ci_artifacts.bucket
  }

  stage {
    name = "Source"
    action { # actions to be performed; pull from git and run on changes to main
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

  stage {
    name = "Build"
    action { # take input form prev stage; call codebuild; 
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