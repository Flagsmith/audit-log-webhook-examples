# Slack Audit Log webhook handler

## Requirements

* [Slack bot token](https://api.slack.com/tutorials/tracks/getting-a-token) with `chat:write` permissions
* Target Slack channel name or ID
* URL for the webhook to listen on, reachable by Flagsmith
* [Audit Log webhook](https://docs.flagsmith.com/system-administration/webhooks) configured 
* Optional: Shared webhook secret to validate the request came from Flagsmith

```bash
export SLACK_BOT_TOKEN=...
export SLACK_CHANNEL=my-slack-channel-name-or-id

# Optional
export FLAGSMITH_WEBHOOK_SECRET=...
```

## Develop

```bash
poetry install
```

```bash
poetry shell
fastapi dev
```

## Run

```
fastapi run
```
