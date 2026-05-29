# Add Redis to user PATH
$redisPath = "C:\Program Files\Redis"
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (-not $currentPath.Contains($redisPath)) {
    [Environment]::SetEnvironmentVariable("Path", $currentPath + ";$redisPath", "User")
    Write-Host "Added Redis to user PATH"
}

# Set Redis configuration environment variables for current user
[Environment]::SetEnvironmentVariable("REDIS_HOME", $redisPath, "User")
[Environment]::SetEnvironmentVariable("REDIS_CONF", "$redisPath\redis.conf", "User")

Write-Host "Redis environment variables have been set up for current user"
Write-Host "Please restart your terminal for changes to take effect"

# Create a local Redis configuration directory
$localRedisPath = "$env:USERPROFILE\Redis"
if (-not (Test-Path $localRedisPath)) {
    New-Item -ItemType Directory -Path $localRedisPath
    Write-Host "Created local Redis directory at $localRedisPath"
}

# Copy Redis configuration to local directory
Copy-Item redis.conf "$localRedisPath\redis.conf" -Force
Write-Host "Copied Redis configuration to $localRedisPath\redis.conf"

# Update REDIS_CONF to point to local configuration
[Environment]::SetEnvironmentVariable("REDIS_CONF", "$localRedisPath\redis.conf", "User")
Write-Host "Updated REDIS_CONF to use local configuration" 