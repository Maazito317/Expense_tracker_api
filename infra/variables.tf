# AWS variables for Terraform configuration
variable "aws_region" {
  description = "AWS region to deploy resources into"
  type        = string
  default     = "us-east-1"
}

# GitHub variables for CodePipeline source
variable "github_owner" {
  description = "GitHub organization or user owning the repo"
  type        = string
}

variable "github_repo" {
  description = "Name of the GitHub repository"
  type        = string
}

variable "github_oauth_token" {
  description = "GitHub OAuth token for CodePipeline source"
  type        = string
  sensitive   = true
}

# Postgres variables for CodeBuild and CI:
variable "POSTGRES_USER" {
  description = "Postgres username for CI"
  type        = string
}

variable "POSTGRES_PASSWORD" {
  description = "Postgres password for CI"
  type        = string
}

variable "POSTGRES_DB" {
  description = "Postgres database name for CI"
  type        = string
}

variable "POSTGRES_PORT" {
  description = "Postgres port"
  type        = string
  default     = "5432"
}

variable "POSTGRES_HOST" {
  description = "Postgres hostname for CI builds"
  type        = string
  default     = "localhost"
}

# JWT variables for authentication
variable "SECRET_KEY" {
  description = "JWT signing secret"
  type        = string
}

variable "ALGORITHM" {
  description = "JWT signing algorithm"
  type        = string
  default     = "HS256"
}

variable "ACCESS_TOKEN_EXPIRE_MINUTES" {
  description = "JWT expiry (minutes)"
  type        = string
  default     = "100"
}

# variable "route53_zone_id" {
#   description = "The ID of the public Route 53 Hosted Zone (e.g. Z123ABC4DEF567)"
#   type        = string
# }
