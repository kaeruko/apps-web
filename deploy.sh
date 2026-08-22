#!/bin/bash
set -e

BUCKET="ampere-apps-web"
DISTRIBUTION_ID="E159EOKK4P9F3D"

echo "==> S3へアップロード中..."
aws s3 sync public/ s3://$BUCKET/ \
  --exclude ".DS_Store" \
  --exclude "*/.DS_Store"

echo "==> CloudFrontキャッシュ無効化中..."
aws cloudfront create-invalidation \
  --distribution-id $DISTRIBUTION_ID \
  --paths "/*" \
  --query 'Invalidation.{Id:Id,Status:Status}' \
  --output table

echo "==> デプロイ完了！"
echo "    https://cloxs.jp"
