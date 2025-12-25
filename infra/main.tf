########################
# ECR – Frontend Container
########################

resource "aws_ecr_repository" "frontend" {
  name                 = "${var.project_name}-frontend"
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = true
  }
}

########################
# S3 – Lambda artifacts
########################

resource "aws_s3_bucket" "lambda_artifacts" {
  bucket = "${var.project_name}-lambda-artifacts-${var.aws_region}"
}

resource "aws_s3_bucket_public_access_block" "lambda_artifacts" {
  bucket = aws_s3_bucket.lambda_artifacts.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_object" "lambda_zip" {
  bucket = aws_s3_bucket.lambda_artifacts.id
  key    = "app.zip"
  source = "../app.zip"
  etag   = filemd5("../app.zip")
}

########################
# IAM – Lambda execution
########################

resource "aws_iam_role" "lambda_exec" {
  name = "${var.project_name}-lambda-exec"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = "sts:AssumeRole"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

########################
# Lambda – API backend
########################

resource "aws_lambda_function" "api" {
  function_name = "${var.project_name}-api"
  role          = aws_iam_role.lambda_exec.arn

  # Set to your runtime and handler
  runtime = "python3.12"          # or nodejs20.x, etc.
  handler = "handler.lambda_handler" # file.function inside app.zip

  filename = "../app.zip"
  source_code_hash = filebase64sha256("../app.zip")

  architectures = ["arm64"]
  memory_size   = 1024
  timeout       = 30

  depends_on = [aws_s3_object.lambda_zip]

  environment {
    variables = {
      NODE_ENV            = "production"
      SUPABASE_URL        = "https://nskovpgvtwulyyengchu.supabase.co"
      SUPABASE_KEY        = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5za292cGd2dHd1bHl5ZW5nY2h1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU5MTg3ODksImV4cCI6MjA4MTQ5NDc4OX0.OgJbVecBzjYFeC4ZI8gyK6z_npc9rqPm7Nyzwuj8JSo"
      STRIPE_API_KEY      = "sk_test_51Sf8e4PZJw42mYq2DjzBuBg2WNTlUdyiRoM8wBT2KAO2KHi7q2hLgiJ6ojZspiWHYeL7pvSpO8vQTSxAd0Ejbkra00FMPJTLri"
      GROQ_API_KEY        = "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"
      STRIPE_PAYMENT_LINK = "https://buy.stripe.com/test_14AeVfdef2bk7YJ248bAs00"
    }
  }
}

########################
# API Gateway – HTTP API
########################

resource "aws_apigatewayv2_api" "http_api" {
  name          = "${var.project_name}-http-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id                 = aws_apigatewayv2_api.http_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.api.invoke_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "default_route" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_stage" "prod" {
  api_id      = aws_apigatewayv2_api.http_api.id
  name        = "prod"
  auto_deploy = true
}

resource "aws_lambda_permission" "api_invoke" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http_api.execution_arn}/*/*"
}

########################
# App Runner – Frontend Service
########################

resource "aws_iam_role" "apprunner_access_role" {
  name = "${var.project_name}-apprunner-access-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = "sts:AssumeRole"
      Principal = { 
        Service = [
          "apprunner.amazonaws.com",
          "build.apprunner.amazonaws.com",
          "tasks.apprunner.amazonaws.com"
        ] 
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "apprunner_ecr_access" {
  role       = aws_iam_role.apprunner_access_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}

resource "aws_apprunner_service" "frontend" {
  service_name = "${var.project_name}-frontend"

  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.apprunner_access_role.arn
    }
    image_repository {
      image_identifier      = "${aws_ecr_repository.frontend.repository_url}:latest"
      image_repository_type = "ECR"
      image_configuration {
        port = "8501"
        runtime_environment_variables = {
          SUPABASE_URL    = "https://nskovpgvtwulyyengchu.supabase.co"
          SUPABASE_KEY    = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5za292cGd2dHd1bHl5ZW5nY2h1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU5MTg3ODksImV4cCI6MjA4MTQ5NDc4OX0.OgJbVecBzjYFeC4ZI8gyK6z_npc9rqPm7Nyzwuj8JSo"
          STRIPE_API_KEY  = "sk_test_51Sf8e4PZJw42mYq2DjzBuBg2WNTlUdyiRoM8wBT2KAO2KHi7q2hLgiJ6ojZspiWHYeL7pvSpO8vQTSxAd0Ejbkra00FMPJTLri"
          GROQ_API_KEY    = "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"
          STRIPE_PAYMENT_LINK = "https://buy.stripe.com/test_14AeVfdef2bk7YJ248bAs00"
          
          # Critical WebSocket Fixes for App Runner
          STREAMLIT_SERVER_HEADLESS = "true"
          STREAMLIT_SERVER_ENABLE_CORS = "false"
          STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION = "false"
        }
      }
    }
    auto_deployments_enabled = true
  }

  instance_configuration {
    cpu    = "1024"
    memory = "2048"
  }

  tags = {
    Name = "${var.project_name}-frontend"
  }

  health_check_configuration {
    path = "/_stcore/health"
    protocol = "HTTP"
    healthy_threshold = 2
    unhealthy_threshold = 3
    interval = 10
    timeout = 5
  }

  depends_on = [aws_iam_role_policy_attachment.apprunner_ecr_access]
}

# App Runner Custom Domain Association (Handles both root and www via enable_www_subdomain)
resource "aws_apprunner_custom_domain_association" "domain" {
  domain_name          = var.root_domain
  service_arn          = aws_apprunner_service.frontend.arn
  enable_www_subdomain = true
}

########################
# ACM – certificate for denialcopilot.com (CloudFront)
########################

resource "aws_acm_certificate" "frontend" {
  domain_name               = var.root_domain
  subject_alternative_names = [var.www_subdomain]
  validation_method         = "DNS"
  provider                  = aws.us-east-1 # CloudFront requires us-east-1

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "frontend_validation" {
  for_each = {
    for dvo in aws_acm_certificate.frontend.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = aws_route53_zone.public.zone_id
}

resource "aws_acm_certificate_validation" "frontend" {
  provider                = aws.us-east-1
  certificate_arn         = aws_acm_certificate.frontend.arn
  validation_record_fqdns = [for record in aws_route53_record.frontend_validation : record.fqdn]
}

########################
# CloudFront – WebSocket-compatible distribution for Streamlit
########################

resource "aws_cloudfront_distribution" "frontend" {
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "MediSync SaaS Frontend (WebSocket Support)"
  default_root_object = ""
  aliases             = [var.root_domain, var.www_subdomain]

  origin {
    domain_name = aws_apprunner_service.frontend.service_url
    origin_id   = "AppRunnerOrigin"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "AppRunnerOrigin"

    # Use AWS Managed Policies for WebSocket support
    cache_policy_id          = "4135ea2d-6df8-44a3-9df3-4b5a84be39ad" # CachingDisabled
    origin_request_policy_id = "b689b0a8-53d0-40ab-baf2-68738e2966ac" # AllViewerExceptHostHeader

    viewer_protocol_policy = "redirect-to-https"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate_validation.frontend.certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  depends_on = [aws_acm_certificate_validation.frontend]
}

########################
# Route 53 – hosted zone
########################

# Root domain: denialcopilot.com
resource "aws_route53_zone" "public" {
  name = var.root_domain
}

########################
# ACM – certificate for api.denialcopilot.com
########################

resource "aws_acm_certificate" "api" {
  domain_name       = var.api_subdomain
  validation_method = "DNS"
  provider          = aws.us-east-1

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "api_validation" {
  for_each = {
    for dvo in aws_acm_certificate.api.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = aws_route53_zone.public.zone_id
}

resource "aws_acm_certificate_validation" "api" {
  provider                = aws.us-east-1
  certificate_arn         = aws_acm_certificate.api.arn
  validation_record_fqdns = [for record in aws_route53_record.api_validation : record.fqdn]
}

########################
# API Gateway custom domain
########################

resource "aws_apigatewayv2_domain_name" "api" {
  domain_name = var.api_subdomain

  domain_name_configuration {
    certificate_arn = aws_acm_certificate_validation.api.certificate_arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }
}

resource "aws_apigatewayv2_api_mapping" "api" {
  api_id      = aws_apigatewayv2_api.http_api.id
  domain_name = aws_apigatewayv2_domain_name.api.id
  stage       = aws_apigatewayv2_stage.prod.name
}

########################
# Route 53 – API A record
########################

resource "aws_route53_record" "api" {
  zone_id = aws_route53_zone.public.zone_id
  name    = var.api_subdomain
  type    = "A"

  alias {
    name                   = aws_apigatewayv2_domain_name.api.domain_name_configuration[0].target_domain_name
    zone_id                = aws_apigatewayv2_domain_name.api.domain_name_configuration[0].hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "frontend_www" {
  zone_id = aws_route53_zone.public.zone_id
  name    = var.www_subdomain
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.frontend.domain_name
    zone_id                = aws_cloudfront_distribution.frontend.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "root_alias" {
  zone_id = aws_route53_zone.public.zone_id
  name    = var.root_domain
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.frontend.domain_name
    zone_id                = aws_cloudfront_distribution.frontend.hosted_zone_id
    evaluate_target_health = false
  }
}

# App Runner CNAME records for validation
resource "aws_route53_record" "apprunner_validation" {
  for_each = {
    for record in aws_apprunner_custom_domain_association.domain.certificate_validation_records : record.name => record
  }

  zone_id = aws_route53_zone.public.zone_id
  name    = each.value.name
  type    = "CNAME"
  records = [each.value.value]
  ttl     = 60
}