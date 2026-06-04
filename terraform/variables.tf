variable "aws_region" {
  description = "AWS 리전"
  type        = string
  default     = "ap-northeast-2"  # 서울
}

variable "key_pair_name" {
  description = "EC2 SSH 접속용 키페어 이름 (AWS 콘솔에서 미리 생성)"
  type        = string
}
