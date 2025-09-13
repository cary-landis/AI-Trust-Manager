$ErrorActionPreference = 'Stop'

$venvPy = Join-Path $PSScriptRoot '..' | Resolve-Path | ForEach-Object { Join-Path $_ '.venv313\Scripts\python.exe' }
if (-not (Test-Path $venvPy)) {
  if (Test-Path "$env:LOCALAPPDATA\Microsoft\WindowsApps\python3.13.exe") {
    & "$env:LOCALAPPDATA\Microsoft\WindowsApps\python3.13.exe" -m venv (Join-Path $PSScriptRoot '..' | Resolve-Path | ForEach-Object { Join-Path $_ '.venv313' })
  } else {
    Write-Error "Python not found. Install Python 3.13 and re-run."
  }
}

& $venvPy -m pip install --upgrade pip setuptools wheel
& $venvPy -m pip install -r (Join-Path $PSScriptRoot '..' | Resolve-Path | ForEach-Object { Join-Path $_ 'requirements.txt' })
& $venvPy -m pytest -q
