module "networking" {
  source = "../../modules/networking"

  vpc_name = "enterprise-ai-dev-vpc"
  vpc_cidr = "10.40.0.0/16"
}

output "vpc_id" {
  description = "Development VPC ID"
  value       = module.networking.vpc_id
}

output "vpc_cidr" {
  description = "Development VPC CIDR"
  value       = module.networking.vpc_cidr
}
