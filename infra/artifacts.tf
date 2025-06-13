locals {
  repo_sanitized = lower(replace(var.github_repo, "_", "-"))
}

resource "random_id" "id" {
  byte_length = 4
}

resource "aws_s3_bucket" "ci_artifacts" {
  bucket = "${local.repo_sanitized}-artifacts-${random_id.id.hex}"
  # No ACL block—ACLs are owner-enforced by default
}

resource "aws_s3_bucket_versioning" "ci_artifacts_versioning" {
  bucket = aws_s3_bucket.ci_artifacts.id

  versioning_configuration {
    status = "Enabled"
  }
}
