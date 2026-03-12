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

# ---------------------------------------------------------------------------
# IAM Role
# ---------------------------------------------------------------------------

data "aws_iam_policy_document" "assume_role" {
  statement {
    sid     = "AllowEC2Assume"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "sqs_full_access" {
  name               = "${var.queue_name}-sqs-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
  description        = "Role com acesso total ao SQS"
  tags               = var.tags
}

data "aws_iam_policy_document" "sqs_full_access" {
  statement {
    sid    = "SQSFullAccess"
    effect = "Allow"

    actions = ["sqs:*"]

    resources = [
      aws_sqs_queue.main.arn,
      aws_sqs_queue.dlq.arn,
    ]
  }
}

resource "aws_iam_policy" "sqs_full_access" {
  name        = "${var.queue_name}-sqs-full-access-policy"
  description = "Acesso total às filas SQS do projeto"
  policy      = data.aws_iam_policy_document.sqs_full_access.json
  tags        = var.tags
}

resource "aws_iam_role_policy_attachment" "sqs_full_access" {
  role       = aws_iam_role.sqs_full_access.name
  policy_arn = aws_iam_policy.sqs_full_access.arn
}

# Instance profile para uso em EC2 (opcional)
resource "aws_iam_instance_profile" "sqs_full_access" {
  name = "${var.queue_name}-sqs-instance-profile"
  role = aws_iam_role.sqs_full_access.name
  tags = var.tags
}

# ---------------------------------------------------------------------------
# Dead Letter Queue
# ---------------------------------------------------------------------------

resource "aws_sqs_queue" "dlq" {
  name                      = "${var.queue_name}-dlq"
  message_retention_seconds = 1209600 # 14 dias
  tags                      = var.tags
}

# ---------------------------------------------------------------------------
# Fila Principal
# ---------------------------------------------------------------------------

resource "aws_sqs_queue" "main" {
  name                       = var.queue_name
  visibility_timeout_seconds = 30
  message_retention_seconds  = 86400 # 1 dia
  delay_seconds              = 0
  receive_wait_time_seconds  = 20 # long polling

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq.arn
    maxReceiveCount     = 3
  })

  tags = var.tags
}

# ---------------------------------------------------------------------------
# Queue Policy — vincula a role diretamente à resource policy da fila
# ---------------------------------------------------------------------------

data "aws_iam_policy_document" "sqs_queue_policy" {
  statement {
    sid    = "AllowRoleFullAccess"
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = [aws_iam_role.sqs_full_access.arn]
    }

    actions   = ["sqs:*"]
    resources = [aws_sqs_queue.main.arn]
  }
}

resource "aws_sqs_queue_policy" "main" {
  queue_url = aws_sqs_queue.main.id
  policy    = data.aws_iam_policy_document.sqs_queue_policy.json
}