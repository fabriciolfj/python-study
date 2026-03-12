d

# -------------------------------------------------------------------
# Variáveis
# -------------------------------------------------------------------
variable "aws_region" {
  description = "Região AWS"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Ambiente (dev, staging, prod)"
  type        = string
  default     = "dev"
}

# -------------------------------------------------------------------
# Tabela DynamoDB – produtos
# -------------------------------------------------------------------
resource "aws_dynamodb_table" "produtos" {
  name         = "produtos"
  billing_mode = "PAY_PER_REQUEST"   # On-demand; troque por PROVISIONED se preferir
  hash_key  = "produto_id"   # Partition Key (PK)
  range_key = "criado_em"    # Sort Key (SK)

  attribute {
    name = "produto_id"
    type = "S"
  }

  attribute {
    name = "criado_em"
    type = "S"
  }

  # -------------------------------------------------------------------
  # GSI – Global Secondary Index (exemplo)
  # -------------------------------------------------------------------
  # global_secondary_index {
  #   name            = "nome-index"
  #   hash_key        = "nome"
  #   projection_type = "ALL"
  # }

  # -------------------------------------------------------------------
  # TTL – expiração automática de itens
  # -------------------------------------------------------------------
  ttl {
    attribute_name = "expires_at"
    enabled        = false
  }

  # -------------------------------------------------------------------
  # Point-in-Time Recovery
  # -------------------------------------------------------------------
  point_in_time_recovery {
    enabled = var.environment == "prod"
  }

  # -------------------------------------------------------------------
  # Criptografia em repouso (usa CMK do KMS se informado)
  # -------------------------------------------------------------------
  server_side_encryption {
    enabled = true
  }

  tags = {
    Name        = "produtos"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

# -------------------------------------------------------------------
# Outputs
# -------------------------------------------------------------------
output "table_name" {
  description = "Nome da tabela DynamoDB"
  value       = aws_dynamodb_table.produtos.name
}

output "table_arn" {
  description = "ARN da tabela DynamoDB"
  value       = aws_dynamodb_table.produtos.arn
}

output "table_id" {
  description = "ID da tabela DynamoDB"
  value       = aws_dynamodb_table.produtos.id
}