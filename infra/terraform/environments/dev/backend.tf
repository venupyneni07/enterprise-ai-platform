terraform {
  backend "s3" {
    bucket       = "enterprise-ai-platform-tfstate-dev-367986505593-ap-south-1"
    key          = "enterprise-ai-platform/dev/terraform.tfstate"
    region       = "ap-south-1"
    profile      = "enterprise-ai-dev-sso"
    encrypt      = true
    use_lockfile = true
  }
}
