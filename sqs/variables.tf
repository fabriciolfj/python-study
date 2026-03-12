variable "aws_region" {
  description = "Região AWS"
  type        = string
  default     = "us-east-1"
}

variable "queue_name" {
  description = "Nome da fila SQS"
  type        = string
  default     = "minha-fila"
}

variable "tags" {
  description = "Tags padrão dos recursos"
  type        = map(string)
  default = {
    Environment = "dev"
    ManagedBy   = "terraform"
  }
}
