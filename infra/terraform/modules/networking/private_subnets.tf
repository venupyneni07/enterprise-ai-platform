resource "aws_subnet" "private_eks" {
  for_each = {
    "ap-south-1a" = "10.40.16.0/20"
    "ap-south-1b" = "10.40.32.0/20"
    "ap-south-1c" = "10.40.48.0/20"
  }

  vpc_id                  = aws_vpc.this.id
  availability_zone       = each.key
  cidr_block              = each.value
  map_public_ip_on_launch = false

  tags = {
    Name = "enterprise-ai-dev-private-eks-${each.key}"
    Tier = "private-eks"
  }
}
