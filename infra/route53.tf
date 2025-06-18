resource "aws_route53_record" "api_alias" {
  zone_id = data.aws_route53_zone.primary.zone_id
  name    = var.domain_name # e.g. "api.example.com"
  type    = "A"

  alias {
    name                   = aws_lb.app.dns_name
    zone_id                = aws_lb.app.zone_id
    evaluate_target_health = true
  }
}
