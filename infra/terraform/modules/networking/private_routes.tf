resource "aws_route_table" "private_eks" {
  for_each = aws_subnet.private_eks

  vpc_id = aws_vpc.this.id

  tags = {
    Name = "enterprise-ai-dev-private-eks-rt-${each.key}"
    Tier = "private-eks"
  }
}

resource "aws_route_table_association" "private_eks" {
  for_each = aws_subnet.private_eks

  subnet_id      = each.value.id
  route_table_id = aws_route_table.private_eks[each.key].id
}
