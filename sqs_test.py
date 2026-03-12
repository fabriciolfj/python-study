import json
import logging
import os
import time

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

QUEUE_URL = os.environ.get("QUEUE_URL")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

def get_client():
    return boto3.client("sqs", region_name=AWS_REGION)

def publish(payload: dict, message_group_id: str | None = None) -> str:
    client = get_client()

    kwargs = {
        "QueueUrl": QUEUE_URL,
        "MessageBody": json.dumps(payload),
        "MessageAttributes": {
            "ContentType": {
                "DataType": "String",
                "StringValue": "application/json",
            }
        },
    }

    if  message_group_id:
        kwargs["MessageGroupId"] = message_group_id

    try:
        response = client.send_message(**kwargs)
        message_id = response["MessageId"]
        logger.info(f"Sent message {message_id}")
        return message_id
    except ClientError as e:
        logger.error(e)
        raise

def process_message(msg: str) -> None:
    logger.info(f"Processing message: {msg}")

def consume(max_message: int = 10, wait_seconds: int = 2, pool_interval: int = 0) -> None:
    client = get_client()
    logger.info(f"Waiting {max_message} messages")

    while True:
        response = client.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=max_message,
            WaitTimeSeconds=wait_seconds,
            MessageAttributeNames=["All"],
        )

        messages = response.get("Messages", [])
        if not messages:
            logger.info(f"No messages received")
            if pool_interval:
                time.sleep(pool_interval)
            continue

        for message in messages:
            receipt_handle = message["ReceiptHandle"]
            try:
                body = json.loads(message["Body"])
                process_message(body)

                client.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=receipt_handle)
                logger.info(f"Deleted message {receipt_handle}")
            except Exception as e:
                logger.error(e)
                raise

        if pool_interval:
            time.sleep(pool_interval)

if __name__ == "__main__":
    import sys

    mode = sys.argv[1] if len(sys.argv) > 1 else "consume"

    if mode == "publish":
        sample_payload = {"evento": "pedido_criado", "pedidoId": 42, "valor": 199.90}
        publish(sample_payload)

    elif mode == "consume":
        consume()

    else:
        print("Uso: python sqs_client.py [publish|consume]")
        sys.exit(1)