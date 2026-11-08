resource "aws_internet_gateway" "public" {
  vpc_id = aws_vpc.this.id

  tags = {
    Name = "enterprise-ai-dev-igw"
  }
}
