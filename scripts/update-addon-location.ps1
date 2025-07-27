# Ensure this script is run as Administrator
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(`[Security.Principal.WindowsBuiltInRole] "Administrator")) {Write-Warning "You must run this script as Administrator!"exit}
# Define the registry base path under HKLM
$baseRegistryPath = "HKLM:\SOFTWARE\Alibre Design Add-Ons"
# Define the add-on name and path
$addonName = "{addon}"
$addonPath = "{path}"
# Check if the registry key exists; create it if not
if (-not (Test-Path $baseRegistryPath)) {New-Item -Path $baseRegistryPath -Force | Out-Null}
# Set or update the registry value
Set-ItemProperty -Path $baseRegistryPath -Name $addonName -Value $addonPath -Type String
# Confirmation
Write-Host "✅ Registry updated under HKLM for add-on: $addonName"
Write-Host "📁 Path set to: $addonPath"