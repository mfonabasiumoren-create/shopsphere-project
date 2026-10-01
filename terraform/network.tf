resource "aws_vpc" "shopsphere_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name    = "shopsphere-vpc"
    Project = "ShopSphere"
  }
}

resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.shopsphere_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name    = "shopsphere-public-a"
    Project = "ShopSphere"
    Tier    = "Public"
  }
}

resource "aws_subnet" "public_b" {
  vpc_id                  = aws_vpc.shopsphere_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true

  tags = {
    Name    = "shopsphere-public-b"
    Project = "ShopSphere"
    Tier    = "Public"
  }
}

resource "aws_subnet" "app_a" {
  vpc_id                  = aws_vpc.shopsphere_vpc.id
  cidr_block              = "10.0.11.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = false

  tags = {
    Name    = "shopsphere-app-a"
    Project = "ShopSphere"
    Tier    = "Application"
  }
}

resource "aws_subnet" "app_b" {
  vpc_id                  = aws_vpc.shopsphere_vpc.id
  cidr_block              = "10.0.12.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = false

  tags = {
    Name    = "shopsphere-app-b"
    Project = "ShopSphere"
    Tier    = "Application"
  }
}

resource "aws_subnet" "db_a" {
  vpc_id                  = aws_vpc.shopsphere_vpc.id
  cidr_block              = "10.0.21.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = false

  tags = {
    Name    = "shopsphere-db-a"
    Project = "ShopSphere"
    Tier    = "Database"
  }
}

resource "aws_subnet" "db_b" {
  vpc_id                  = aws_vpc.shopsphere_vpc.id
  cidr_block              = "10.0.22.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = false

  tags = {
    Name    = "shopsphere-db-b"
    Project = "ShopSphere"
    Tier    = "Database"
  }
}

resource "aws_internet_gateway" "shopsphere_igw" {
  vpc_id = aws_vpc.shopsphere_vpc.id

  tags = {
    Name    = "shopsphere-igw"
    Project = "ShopSphere"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.shopsphere_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.shopsphere_igw.id
  }

  tags = {
    Name    = "shopsphere-public-rt"
    Project = "ShopSphere"
  }
}

resource "aws_route_table_association" "public_a" {
  subnet_id      = aws_subnet.public_a.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_b" {
  subnet_id      = aws_subnet.public_b.id
  route_table_id = aws_route_table.public.id
}

resource "aws_eip" "nat" {
  domain = "vpc"

  tags = {
    Name    = "shopsphere-nat-eip"
    Project = "ShopSphere"
  }
}

resource "aws_nat_gateway" "shopsphere_nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_a.id

  depends_on = [aws_internet_gateway.shopsphere_igw]

  tags = {
    Name    = "shopsphere-nat-gw"
    Project = "ShopSphere"
  }
}

resource "aws_route_table" "app" {
  vpc_id = aws_vpc.shopsphere_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.shopsphere_nat.id
  }

  tags = {
    Name    = "shopsphere-app-rt"
    Project = "ShopSphere"
  }
}

resource "aws_route_table_association" "app_a" {
  subnet_id      = aws_subnet.app_a.id
  route_table_id = aws_route_table.app.id
}

resource "aws_route_table_association" "app_b" {
  subnet_id      = aws_subnet.app_b.id
  route_table_id = aws_route_table.app.id
}

resource "aws_route_table" "db" {
  vpc_id = aws_vpc.shopsphere_vpc.id

  tags = {
    Name    = "shopsphere-db-rt"
    Project = "ShopSphere"
  }
}

resource "aws_route_table_association" "db_a" {
  subnet_id      = aws_subnet.db_a.id
  route_table_id = aws_route_table.db.id
}

resource "aws_route_table_association" "db_b" {
  subnet_id      = aws_subnet.db_b.id
  route_table_id = aws_route_table.db.id
}