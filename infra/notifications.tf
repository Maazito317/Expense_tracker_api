#####################################################
# infra/notifications.tf
#####################################################

resource "aws_sns_topic" "ci_alerts" {
  name = "${local.repo_sanitized}-ci-alerts"
}

resource "aws_sns_topic_subscription" "email_sub" {
  topic_arn = aws_sns_topic.ci_alerts.arn
  protocol  = "email"
  endpoint  = "your.email@example.com"
}

resource "aws_cloudwatch_event_rule" "pipeline_failed" {
  name          = "${local.repo_sanitized}-pipeline-failed"
  description   = "Alert when CodePipeline execution fails"
  event_pattern = <<EOF
{
  "source": ["aws.codepipeline"],
  "detail-type": ["CodePipeline Pipeline Execution State Change"],
  "detail": {
    "pipeline": ["${var.github_repo}-pipeline"],
    "state": ["FAILED"]
  }
}
EOF
}

resource "aws_cloudwatch_event_target" "sns_notify" {
  rule = aws_cloudwatch_event_rule.pipeline_failed.name
  arn  = aws_sns_topic.ci_alerts.arn
}
