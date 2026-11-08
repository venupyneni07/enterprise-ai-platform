resource "aws_route_table" "database" {
  for_each = aws_subnet.database

  vpc_id = aws_vpc.this.id

  tags = {
    Name = "enterprise-ai-dev-database-rt-${each.key}"
    Tier = "database"
  }
}

resource "aws_route_table_association" "database" {
  for_each = aws_subnet.database

  subnet_id      = each.value.id
  route_table_id = aws_route_table.database[each.key].id
}
