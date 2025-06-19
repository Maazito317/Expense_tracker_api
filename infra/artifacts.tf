# Remove unusable characters from the GitHub repository name
# to create a valid S3 bucket name.
locals {
  repo_sanitized = lower(replace(var.github_repo, "_", "-"))
}

# To ensure the bucket name is unique, we append a random ID
resource "random_id" "id" {
  byte_length = 4
}

# Create an S3 bucket for CI artifacts
resource "aws_s3_bucket" "ci_artifacts" {
  bucket        = "${local.repo_sanitized}-artifacts-${random_id.id.hex}"
  force_destroy = true
  # No ACL block—ACLs are owner-enforced by default
}

resource "aws_s3_bucket_versioning" "ci_artifacts_versioning" {
  bucket = aws_s3_bucket.ci_artifacts.id

  versioning_configuration {
    status = "Enabled"
  }
}
