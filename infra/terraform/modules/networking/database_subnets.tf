resource "aws_subnet" "database" {
  for_each = {
    "ap-south-1a" = "10.40.64.0/24"
    "ap-south-1b" = "10.40.65.0/24"
    "ap-south-1c" = "10.40.66.0/24"
  }

  vpc_id                  = aws_vpc.this.id
  availability_zone       = each.key
  cidr_block              = each.value
  map_public_ip_on_launch = false

  tags = {
    Name = "enterprise-ai-dev-database-${each.key}"
    Tier = "database"
  }
}
