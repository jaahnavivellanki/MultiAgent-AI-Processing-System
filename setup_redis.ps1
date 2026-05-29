# Add Redis to PATH
$redisPath = "C:\Program Files\Redis"
$currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
if (-not $currentPath.Contains($redisPath)) {
    [Environment]::SetEnvironmentVariable("Path", $currentPath + ";$redisPath", "Machine")
    Write-Host "Added Redis to system PATH"
}

# Set Redis configuration environment variables
[Environment]::SetEnvironmentVariable("REDIS_HOME", $redisPath, "Machine")
[Environment]::SetEnvironmentVariable("REDIS_CONF", "$redisPath\redis.conf", "Machine")

Write-Host "Redis environment variables have been set up"
Write-Host "Please restart your terminal for changes to take effect" 