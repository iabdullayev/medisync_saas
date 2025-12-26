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

variable "stripe_api_key" {
  description = "Stripe API Key (Sensitive)"
  type        = string
  sensitive   = true
}

variable "supabase_url" {
  description = "Supabase Project URL"
  type        = string
  default     = "https://nskovpgvtwulyyengchu.supabase.co"
}

variable "supabase_key" {
  description = "Supabase Anon Key (Public)"
  type        = string
  default     = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5za292cGd2dHd1bHl5ZW5nY2h1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQ3MjU1MzAsImV4cCI6MjA1MDMwMTUzMH0.WbOQlQOBaUyNKQXMqGPKJGmEZYVdGzUOdUdFcJnHqjQ"
}
