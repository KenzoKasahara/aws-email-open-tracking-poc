import base64
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 1×1 透明 GIF（43 バイト）
PIXEL_GIF = base64.b64decode(
    "R0lGODlhAQABAPAAAP///wAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw=="
)


def lambda_handler(event, context):
    headers = event.get("headers", {})
    query = event.get("queryStringParameters") or {}

    log_data = {
        "event_type": "mail_open",
        "query": query,
        "user_agent": headers.get("user-agent"),
        "source_ip": event.get("requestContext", {})
            .get("http", {})
            .get("sourceIp"),
    }

    logger.info(json.dumps(log_data, ensure_ascii=False))

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "image/gif",
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        },
        "body": base64.b64encode(PIXEL_GIF).decode("utf-8"),
        "isBase64Encoded": True,
    }
