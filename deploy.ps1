$ErrorActionPreference = "Stop"

$distributionId = "E159EOKK4P9F3D"

aws s3 sync .\public\ s3://ampere-apps-web/
if ($LASTEXITCODE -ne 0) {
    throw "S3 sync failed with exit code $LASTEXITCODE"
}

$invalidationId = aws cloudfront create-invalidation `
    --distribution-id $distributionId `
    --paths "/*" `
    --query "Invalidation.Id" `
    --output text

if ($LASTEXITCODE -ne 0) {
    throw "CloudFront invalidation creation failed with exit code $LASTEXITCODE"
}

if ([string]::IsNullOrWhiteSpace($invalidationId)) {
    throw "CloudFront invalidation returned an empty ID"
}

Write-Host "Waiting for CloudFront invalidation: $invalidationId"

aws cloudfront wait invalidation-completed `
    --distribution-id $distributionId `
    --id $invalidationId

if ($LASTEXITCODE -ne 0) {
    throw "CloudFront invalidation wait failed with exit code $LASTEXITCODE"
}

Write-Host "deploy done"