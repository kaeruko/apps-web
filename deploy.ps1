$ErrorActionPreference = "Stop"

aws s3 sync .\public\ s3://ampere-apps-web/
if ($LASTEXITCODE -ne 0) {
    throw "S3 sync failed"
}

aws cloudfront create-invalidation `
  --distribution-id E159EOKK4P9F3D `
  --paths "/garunavi/*" "/sitemap.xml"

if ($LASTEXITCODE -ne 0) {
    throw "CloudFront invalidation failed"
}

Write-Host "deploy done"