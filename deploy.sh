#!/usr/bin/env bash
set -Eeuo pipefail

PROFILE="${1:-new-aws}"
EXPECTED_ACCOUNT_ID="${2:-314267685786}"
BUCKET="cloxs-apps-web-314267685786"
DISTRIBUTION_ID="EQWPIWBHWFB17"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

assert_aws_account() {
  local account
  if ! account="$(aws sts get-caller-identity \
    --profile "$PROFILE" \
    --query Account \
    --output text \
    --no-cli-pager)"; then
    echo "AWS account verification command failed for profile: $PROFILE" >&2
    exit 1
  fi

  if [[ "$account" != "$EXPECTED_ACCOUNT_ID" ]]; then
    echo "AWS account verification failed. Expected=$EXPECTED_ACCOUNT_ID Actual=$account Profile=$PROFILE" >&2
    exit 1
  fi
}

assert_aws_account

echo "==> S3へアップロード中..."
if ! aws s3 sync "$SCRIPT_DIR/public/" "s3://$BUCKET/" \
  --exclude ".DS_Store" \
  --exclude "*/.DS_Store" \
  --sse AES256 \
  --profile "$PROFILE" \
  --no-cli-pager; then
  echo "S3 sync failed" >&2
  exit 1
fi

# Re-check immediately before the next AWS mutation.
assert_aws_account

echo "==> CloudFrontキャッシュ無効化中..."
if ! INVALIDATION_ID="$(aws cloudfront create-invalidation \
  --distribution-id "$DISTRIBUTION_ID" \
  --paths "/*" \
  --profile "$PROFILE" \
  --query 'Invalidation.Id' \
  --output text \
  --no-cli-pager)"; then
  echo "CloudFront invalidation creation failed" >&2
  exit 1
fi

if [[ -z "$INVALIDATION_ID" || "$INVALIDATION_ID" == "None" ]]; then
  echo "CloudFront invalidation returned an empty ID" >&2
  exit 1
fi

echo "==> CloudFront反映待ち: $INVALIDATION_ID"
if ! aws cloudfront wait invalidation-completed \
  --distribution-id "$DISTRIBUTION_ID" \
  --id "$INVALIDATION_ID" \
  --profile "$PROFILE" \
  --no-cli-pager; then
  echo "CloudFront invalidation wait failed: $INVALIDATION_ID" >&2
  exit 1
fi

echo "==> デプロイ完了: https://cloxs.jp ($INVALIDATION_ID)"
