########################
# ECR – Frontend Container (Keeping for backup/future use)
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
  runtime       = "python3.12"
  handler       = "handler.lambda_handler"
  filename      = "../app.zip"
  source_code_hash = filebase64sha256("../app.zip")
  architectures = ["arm64"]
  memory_size   = 1024
  timeout       = 30
  depends_on    = [aws_s3_object.lambda_zip]

  environment {
    variables = {
      NODE_ENV            = "production"
      SUPABASE_URL        = "https://nskovpgvtwulyyengchu.supabase.co"
      SUPABASE_KEY        = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5za292cGd2dHd1bHl5ZW5nY2h1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU5MTg3ODksImV4cCI6MjA4MTQ5NDc4OX0.OgJbVecBzjYFeC4ZI8gyK6z_npc9rqPm7Nyzwuj8JSo"
      STRIPE_API_KEY      = "sk_test_51Sf8e4PZJw42mYq2DjzBuBg2WNTlUdyiRoM8wBT2KAO2KHi7q2hLgiJ6ojZspiWHYeL7pvSpO8vQTSxAd0Ejbkra00FMPJTLri"
      GROQ_API_KEY        = var.groq_api_key
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
# S3 Redirect (Root -> WWW) for Streamlit Cloud
########################

resource "aws_s3_bucket" "root_redirect" {
  bucket = var.root_domain
}

resource "aws_s3_bucket_website_configuration" "root_redirect" {
  bucket = aws_s3_bucket.root_redirect.id

  redirect_all_requests_to {
    host_name = var.www_subdomain
    protocol  = "https"
  }
}

# Remove public access block to allow website redirection (S3 requirement for website endpoint)
resource "aws_s3_bucket_public_access_block" "root_redirect" {
  bucket = aws_s3_bucket.root_redirect.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "root_redirect" {
  bucket = aws_s3_bucket.root_redirect.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.root_redirect.arn}/*"
      }
    ]
  })
  
  depends_on = [aws_s3_bucket_public_access_block.root_redirect]
}

########################
# Route 53
########################

# Hosted Zone
resource "aws_route53_zone" "public" {
  name = var.root_domain
}

# Root Domain (ALIAS to CloudFront for HTTPS support)
resource "aws_route53_record" "root" {
  zone_id = aws_route53_zone.public.zone_id
  name    = var.root_domain
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.root_redirect.domain_name
    zone_id                = aws_cloudfront_distribution.root_redirect.hosted_zone_id
    evaluate_target_health = false
  }
}

# Note: The 'www' record is intentionally NOT managed here (Manual CNAME to Streamlit)

########################
# ACM & API Config (Backend)
########################

resource "aws_acm_certificate" "api" {
  domain_name       = var.api_subdomain
  validation_method = "DNS"
  provider          = aws.us-east-1

  lifecycle {
    create_before_destroy = true
  }
}

########################
# ACM for Root Domain (Needed for CloudFront)
########################

resource "aws_acm_certificate" "root" {
  domain_name       = var.root_domain
  validation_method = "DNS"
  provider          = aws.us-east-1

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "root_validation" {
  for_each = {
    for dvo in aws_acm_certificate.root.domain_validation_options : dvo.domain_name => {
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

resource "aws_acm_certificate_validation" "root" {
  provider                = aws.us-east-1
  certificate_arn         = aws_acm_certificate.root.arn
  validation_record_fqdns = [for record in aws_route53_record.root_validation : record.fqdn]
}

########################
# CloudFront for Root Redirect (HTTPS -> WWW)
########################

resource "aws_cloudfront_distribution" "root_redirect" {
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "Root Domain Redirect (HTTPS support)"
  aliases             = [var.root_domain]
  price_class         = "PriceClass_100" # Lowest cost (US/EU only)

  origin {
    domain_name = aws_s3_bucket_website_configuration.root_redirect.website_endpoint
    origin_id   = "S3Redirect"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only" # S3 Website only speaks HTTP
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3Redirect"

    # Forward nothing, just cache the 301 redirect
    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
    compress               = true
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate_validation.root.certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
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