[CmdletBinding()]
param(
    [ValidateNotNullOrEmpty()]
    [string]$Profile = "new-aws",

    [ValidatePattern('^\d{12}$')]
    [string]$ExpectedAccountId = "314267685786",

    [ValidateNotNullOrEmpty()]
    [string]$Bucket = "cloxs-apps-web-314267685786",

    [ValidateNotNullOrEmpty()]
    [string]$DistributionId = "EQWPIWBHWFB17"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Assert-AwsAccount {
    $account = aws sts get-caller-identity `
        --profile $Profile `
        --query Account `
        --output text `
        --no-cli-pager

    if ($LASTEXITCODE -ne 0 -or $account -ne $ExpectedAccountId) {
        throw "AWS account verification failed. Expected=$ExpectedAccountId Actual=$account Profile=$Profile"
    }
}

$publicDirectory = Join-Path $PSScriptRoot "public"
if (-not (Test-Path -LiteralPath $publicDirectory -PathType Container)) {
    throw "Deploy source directory not found: $publicDirectory"
}

$girlsIndex = Join-Path $publicDirectory "minapp\girls\index.html"
if (-not (Test-Path -LiteralPath $girlsIndex -PathType Leaf)) {
    throw "Girls index file not found: $girlsIndex"
}

Assert-AwsAccount

aws s3 sync $publicDirectory "s3://$Bucket/" `
    --exclude ".DS_Store" `
    --exclude "*/.DS_Store" `
    --sse AES256 `
    --profile $Profile `
    --no-cli-pager

if ($LASTEXITCODE -ne 0) {
    throw "S3 sync failed with exit code $LASTEXITCODE"
}

# CloudFront uses the S3 REST object key directly. A request for /minapp/girls/
# therefore needs an object whose key is exactly "minapp/girls/".
# Keep the clean canonical URL working by publishing the same HTML there.
Assert-AwsAccount

aws s3api put-object `
    --bucket $Bucket `
    --key "minapp/girls/" `
    --body $girlsIndex `
    --content-type "text/html; charset=utf-8" `
    --server-side-encryption AES256 `
    --profile $Profile `
    --no-cli-pager | Out-Null

if ($LASTEXITCODE -ne 0) {
    throw "Girls trailing-slash alias upload failed with exit code $LASTEXITCODE"
}

# Re-check immediately before the next AWS mutation.
Assert-AwsAccount

$invalidationId = aws cloudfront create-invalidation `
    --distribution-id $DistributionId `
    --paths "/*" `
    --profile $Profile `
    --query "Invalidation.Id" `
    --output text `
    --no-cli-pager

if ($LASTEXITCODE -ne 0) {
    throw "CloudFront invalidation creation failed with exit code $LASTEXITCODE"
}

$invalidationId = $invalidationId.Trim()
if ([string]::IsNullOrWhiteSpace($invalidationId)) {
    throw "CloudFront invalidation returned an empty ID"
}

Write-Host "Waiting for CloudFront invalidation: $invalidationId"

aws cloudfront wait invalidation-completed `
    --distribution-id $DistributionId `
    --id $invalidationId `
    --profile $Profile `
    --no-cli-pager

if ($LASTEXITCODE -ne 0) {
    throw "CloudFront invalidation wait failed with exit code $LASTEXITCODE"
}

Write-Host "Deploy completed: https://cloxs.jp (invalidation $invalidationId)"
