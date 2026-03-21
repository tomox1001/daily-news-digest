#!/bin/bash
# Daily News Digest — Slack通知スクリプト
# "Kawano's AI Assistant" ボットとして #ai-reports-kawano に投稿する
#
# Usage: ./scripts/slack_notify.sh "メッセージ本文"

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
source "${SCRIPT_DIR}/.env"

SLACK_CHANNEL="C0AKXQ9NEMA"
MESSAGE="$1"

SLACK_PAYLOAD=$(jq -n \
  --arg channel "${SLACK_CHANNEL}" \
  --arg text "${MESSAGE}" \
  '{"channel": $channel, "text": $text, "link_names": true}')

SLACK_RESPONSE=$(curl -sf \
  -X POST -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H 'Content-type: application/json; charset=utf-8' \
  -d "${SLACK_PAYLOAD}" \
  "https://slack.com/api/chat.postMessage")

if echo "${SLACK_RESPONSE}" | jq -e '.ok == true' > /dev/null 2>&1; then
  echo "Slack posted successfully."
  echo "${SLACK_RESPONSE}" | jq -r '.message.permalink // "no permalink"'
else
  echo "ERROR: Slack post failed:" >&2
  echo "${SLACK_RESPONSE}" | jq . >&2
  exit 1
fi
