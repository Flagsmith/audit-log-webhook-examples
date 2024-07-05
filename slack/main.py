import hmac
import json
import logging
import os
from hashlib import sha256
from textwrap import dedent

from fastapi import FastAPI, HTTPException, Request
from slack_sdk import WebClient
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)

FLAGSMITH_WEBHOOK_SECRET = os.environ.get("FLAGSMITH_WEBHOOK_SECRET")


class ValidateFlagsmithWebhookSignatureMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        received_signature = request.headers.get("x-flagsmith-signature")
        if received_signature and not FLAGSMITH_WEBHOOK_SECRET:
            raise HTTPException(
                status_code=500,
                detail="Received a webhook signature but FLAGSMITH_WEBHOOK_SECRET is not set",
            )
        elif not FLAGSMITH_WEBHOOK_SECRET:
            return await call_next(request)
        body = await request.body()
        expected_signature = hmac.new(
            key=FLAGSMITH_WEBHOOK_SECRET.encode(),
            msg=body,
            digestmod=sha256,
        ).hexdigest()
        if not hmac.compare_digest(expected_signature, received_signature):
            raise HTTPException(status_code=400)
        return await call_next(request)


slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
slack_channel = os.environ["SLACK_CHANNEL"]

app = FastAPI()
app.add_middleware(ValidateFlagsmithWebhookSignatureMiddleware)


@app.post("/")
async def main(request: Request):
    slack_message = dedent(
        f"""
        *Received Flagsmith audit event*
        ```{json.dumps(await request.json(), indent=2)}```
        """
    ).strip()
    slack_client.chat_postMessage(channel=slack_channel, text=slack_message)
