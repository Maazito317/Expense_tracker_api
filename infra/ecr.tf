resource "aws_ecr_repository" "app_repo" {
  name                 = local.repo_sanitized
  force_delete         = true
  image_tag_mutability = "IMMUTABLE" # prevents re-pushing the same tag

  image_scanning_configuration {
    scan_on_push = true # auto-scan every new image for vulnerabilities
  }
}
