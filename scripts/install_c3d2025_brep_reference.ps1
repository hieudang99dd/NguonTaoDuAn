param(
    [Parameter(Mandatory=$true)]
    [string] $SourceDll
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$destDir = Join-Path $root 'references\2025'
$dest = Join-Path $destDir 'acdbmgdbrep.dll'
if (-not (Test-Path -LiteralPath $SourceDll -PathType Leaf)) { throw "Khong tim thay DLL: $SourceDll" }
if ([System.IO.Path]::GetFileName($SourceDll).ToLowerInvariant() -ne 'acdbmgdbrep.dll') { throw 'DLL phai co ten acdbmgdbrep.dll' }
New-Item -ItemType Directory -Path $destDir -Force | Out-Null
$resolvedSource = (Resolve-Path -LiteralPath $SourceDll).Path
if (-not [string]::Equals($resolvedSource, $dest, [System.StringComparison]::OrdinalIgnoreCase)) {
    Copy-Item -LiteralPath $resolvedSource -Destination $dest -Force
}
$hash = (Get-FileHash -LiteralPath $dest -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "OK: $dest"
Write-Host "SHA256: $hash"
Write-Host 'Reference for build only; do not distribute Autodesk API DLL.'
