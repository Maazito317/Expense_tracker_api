resource "aws_ecr_repository" "app_repo" {
  name                 = local.repo_sanitized
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# Optionally: lifecycle policy to auto-delete old images
resource "aws_ecr_lifecycle_policy" "expire_untagged" {
  repository = aws_ecr_repository.app_repo.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Expire untagged images older than 7 days"
        selection = {
          tagStatus   = "untagged"
          countType   = "sinceImagePushed"
          countNumber = 7
          countUnit   = "days"
        }
        action = { type = "expire" }
      }
    ]
  })
}
