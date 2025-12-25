variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "claimappeals"  # change to your project name
}

variable "root_domain" {
  type    = string
  default = "denialcopilot.com"
}

variable "api_subdomain" {
  type    = string
  default = "api.denialcopilot.com"
}

variable "www_subdomain" {
  type    = string
  default = "www.denialcopilot.com"
}

variable "groq_api_key" {
  description = "Groq API Key (Sensitive)"
  type        = string
  sensitive   = true
}

