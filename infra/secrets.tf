resource "aws_secretsmanager_secret" "app_secret_key" {
  name        = "${local.repo_sanitized}-secret-key"
  description = "JWT SECRET_KEY for Expense Tracker"
}

resource "aws_secretsmanager_secret_version" "app_secret_key_ver" {
  secret_id     = aws_secretsmanager_secret.app_secret_key.id
  secret_string = var.SECRET_KEY
}

# Repeat for DB password if you prefer:
resource "aws_secretsmanager_secret" "db_password" {
  name        = "${local.repo_sanitized}-db-password"
  description = "Postgres password for CI"
}

resource "aws_secretsmanager_secret_version" "db_password_ver" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = var.POSTGRES_PASSWORD
}
