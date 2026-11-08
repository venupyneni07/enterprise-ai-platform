resource "aws_subnet" "public" {
  for_each = {
    "ap-south-1a" = "10.40.0.0/24"
    "ap-south-1b" = "10.40.1.0/24"
    "ap-south-1c" = "10.40.2.0/24"
  }

  vpc_id                  = aws_vpc.this.id
  availability_zone       = each.key
  cidr_block              = each.value
  map_public_ip_on_launch = false

  tags = {
    Name = "enterprise-ai-dev-public-${each.key}"
    Tier = "public"
  }
}
