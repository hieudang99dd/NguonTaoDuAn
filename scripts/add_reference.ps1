param(
  [Parameter(Mandatory=$true)][ValidateSet(2024,2025,2026)][int]$Year,
  [Parameter(Mandatory=$true)][string]$SourceDll,
  [switch]$Replace,
  [ValidateSet("net8","net10")][string]$HostRuntime
)
$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if (-not (Test-Path -LiteralPath $SourceDll -PathType Leaf)) { throw "Reference file not found: $SourceDll" }
$source = (Resolve-Path -LiteralPath $SourceDll).Path
if ([IO.Path]::GetExtension($source) -ne '.dll') { throw 'Expected a DLL assembly' }
$destinationFolder = Join-Path $repoRoot ("references\" + $Year)
New-Item -ItemType Directory -Force -Path $destinationFolder | Out-Null
$destination = Join-Path $destinationFolder ([IO.Path]::GetFileName($source))
if (Test-Path -LiteralPath $destination) {
  $old = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash
  $incoming = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
  if ($old -ne $incoming -and -not $Replace) {
    throw "Reference DLL exists with different hash. Review and use -Replace if intended."
  }
}
if (-not [string]::Equals($source, $destination, [StringComparison]::OrdinalIgnoreCase)) {
  Copy-Item -LiteralPath $source -Destination $destination -Force
}
$hash = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "IMPORTED: $destination"
Write-Host "SHA256: $hash"
Write-Host 'Declared host year is not proof of version compatibility. Verify build + NETLOAD.'
Write-Host 'Keep Autodesk references local; never distribute them in the NETLOAD package.'
