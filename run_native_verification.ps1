# Execute in PowerShell from the extracted project root on Windows.
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$Native = Join-Path $Root "Results\native_wolfram_results.json"
if (Test-Path $Native) { Remove-Item $Native -Force }
if (-not (Get-Command wolframscript -ErrorAction SilentlyContinue)) {
  throw "Wolfram Language is not on PATH. Install/configure a licensed Mathematica or Wolfram Engine and retry."
}
& wolframscript -file Examples/RunNative.wls
if ($LASTEXITCODE -ne 0) { throw "Wolfram native test returned error code $LASTEXITCODE" }
if (-not (Test-Path $Native)) { throw "No native result JSON created; verification incomplete." }
& python validation/verify_native.py
if ($LASTEXITCODE -ne 0) { throw "Native/Python cross-verification failed." }
Write-Host "Native Wolfram verification passed with a recorded JSON result." -ForegroundColor Green
