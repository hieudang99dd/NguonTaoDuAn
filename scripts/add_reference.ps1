param(
  [Parameter(Mandatory=$true)][ValidateRange(2020,2100)][int]$Year,
  [Parameter(Mandatory=$true)][string]$SourceDll
)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $SourceDll -PathType Leaf)) { throw "Reference file not found: $SourceDll" }
$source = (Resolve-Path -LiteralPath $SourceDll).Path
if ([IO.Path]::GetExtension($source).ToLowerInvariant() -ne '.dll') { throw 'Expected a .dll reference file' }
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$destDir = Join-Path $root ("references\" + $Year)
New-Item -ItemType Directory -Path $destDir -Force | Out-Null
$dest = Join-Path $destDir ([IO.Path]::GetFileName($source))
if (-not [string]::Equals($source, $dest, [StringComparison]::OrdinalIgnoreCase)) {
  Copy-Item -LiteralPath $source -Destination $dest -Force
}
$hash = (Get-FileHash -LiteralPath $dest -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host ("Reference: " + $dest)
Write-Host ("SHA256: " + $hash)
Write-Host "Check Autodesk licensing, version and framework in the consuming project."
Write-Host "Autodesk references are for local build only, not NETLOAD distribution."
