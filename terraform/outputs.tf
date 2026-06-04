output "server_ip" {
  description = "EC2 고정 IP (이걸 ALLOWED_HOSTS에 입력)"
  value       = aws_eip.focus_memo.public_ip
}

output "ssh_command" {
  description = "서버 SSH 접속 명령어"
  value       = "ssh -i your-key.pem ubuntu@${aws_eip.focus_memo.public_ip}"
}
