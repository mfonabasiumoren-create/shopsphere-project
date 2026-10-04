resource "aws_security_group" "alb" {
  name        = "shopsphere-alb-sg"
  description = "Security group for the ShopSphere Application Load Balancer"
  vpc_id      = aws_vpc.shopsphere_vpc.id

  tags = {
    Name    = "shopsphere-alb-sg"
    Project = "ShopSphere"
    Tier    = "Public"
  }
}

resource "aws_vpc_security_group_ingress_rule" "alb_http" {
  security_group_id = aws_security_group.alb.id

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 80
  to_port     = 80
  ip_protocol = "tcp"
  description = "Allow HTTP traffic from the internet"
}

resource "aws_vpc_security_group_egress_rule" "alb_all" {
  security_group_id = aws_security_group.alb.id

  cidr_ipv4   = "0.0.0.0/0"
  ip_protocol = "-1"
  description = "Allow outbound traffic from the ALB"
}

resource "aws_security_group" "app" {
  name        = "shopsphere-app-sg"
  description = "Security group for the ShopSphere application tier"
  vpc_id      = aws_vpc.shopsphere_vpc.id

  tags = {
    Name    = "shopsphere-app-sg"
    Project = "ShopSphere"
    Tier    = "Application"
  }
}

resource "aws_vpc_security_group_ingress_rule" "app_from_alb" {
  security_group_id            = aws_security_group.app.id
  referenced_security_group_id = aws_security_group.alb.id

  from_port   = 8080
  to_port     = 8080
  ip_protocol = "tcp"
  description = "Allow application traffic from the ALB"
}

resource "aws_vpc_security_group_egress_rule" "app_all" {
  security_group_id = aws_security_group.app.id

  cidr_ipv4   = "0.0.0.0/0"
  ip_protocol = "-1"
  description = "Allow outbound traffic from the application tier"
}

resource "aws_security_group" "db" {
  name        = "shopsphere-db-sg"
  description = "Security group for the ShopSphere database tier"
  vpc_id      = aws_vpc.shopsphere_vpc.id

  tags = {
    Name    = "shopsphere-db-sg"
    Project = "ShopSphere"
    Tier    = "Database"
  }
}

resource "aws_vpc_security_group_ingress_rule" "db_from_app" {
  security_group_id            = aws_security_group.db.id
  referenced_security_group_id = aws_security_group.app.id

  from_port   = 3306
  to_port     = 3306
  ip_protocol = "tcp"
  description = "Allow MySQL traffic from the application tier"
}

resource "aws_vpc_security_group_egress_rule" "db_all" {
  security_group_id = aws_security_group.db.id

  cidr_ipv4   = "0.0.0.0/0"
  ip_protocol = "-1"
  description = "Allow outbound traffic from the database tier"
}