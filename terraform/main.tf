terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# 최신 Ubuntu 22.04 AMI 자동 조회
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# ── 보안 그룹 (방화벽) ────────────────────────────────────────
resource "aws_security_group" "focus_memo" {
  name        = "focus-memo-sg"
  description = "Focus Memo security group"

  # SSH 접속
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTP (Nginx 문지기)
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # 아웃바운드 전체 허용
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "focus-memo-sg" }
}

# ── EC2 인스턴스 (배포 서버) ──────────────────────────────────
resource "aws_instance" "focus_memo" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"   # AWS 프리티어

  key_name               = var.key_pair_name
  vpc_security_group_ids = [aws_security_group.focus_memo.id]

  # 서버 최초 부팅 시 Docker 설치 스크립트
  user_data = <<-EOF
    #!/bin/bash
    set -e
    apt-get update -y
    apt-get install -y docker.io docker-compose git
    systemctl start docker
    systemctl enable docker
    usermod -aG docker ubuntu

    # 앱 디렉토리 준비
    mkdir -p /home/ubuntu/app
    chown ubuntu:ubuntu /home/ubuntu/app

    # GitHub 저장소 클론
    sudo -u ubuntu git clone https://github.com/dongjebag59-dev/Innovative-Memo-App.git /home/ubuntu/app
  EOF

  tags = { Name = "focus-memo-server" }
}

# ── 고정 IP (Elastic IP) ──────────────────────────────────────
resource "aws_eip" "focus_memo" {
  instance = aws_instance.focus_memo.id
  domain   = "vpc"
  tags     = { Name = "focus-memo-eip" }
}
