output "api_url" {
  value = "https://${var.api_subdomain}"
}

output "api_gateway_id" {
  value = aws_apigatewayv2_api.http_api.id
}

output "lambda_arn" {
  value = aws_lambda_function.api.arn
}

output "lambda_name" {
  value = aws_lambda_function.api.function_name
}

output "nameservers" {
  value = aws_route53_zone.public.name_servers
}

output "frontend_url" {
  value = "https://${var.www_subdomain}"
}

