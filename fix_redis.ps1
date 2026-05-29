# Stop Redis service if running
Stop-Service Redis -ErrorAction SilentlyContinue

# Set Redis configuration path
$redisPath = "C:\Program Files\Redis"
$configPath = "$redisPath\redis.windows.conf"

# Copy our configuration
Copy-Item redis.windows.conf $configPath -Force

# Update service configuration
$service = Get-WmiObject -Class Win32_Service -Filter "Name='Redis'"
if ($service) {
    $service.Change($null, $null, $null, $null, $null, $null, "`"$redisPath\redis-server.exe`" `"$configPath`"", $null, $null, $null, $null)
    $service.StopService()
    Start-Sleep -Seconds 2
    $service.StartService()
}

Write-Host "Redis service has been reconfigured. Please check Windows Services." 