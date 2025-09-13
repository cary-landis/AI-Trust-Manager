$ErrorActionPreference = 'Stop'

# Resolve Python path (prefer venv, fallback to WindowsApps alias)
$venvPy = Join-Path $PSScriptRoot '..' | Resolve-Path | ForEach-Object { Join-Path $_ '.venv313\Scripts\python.exe' }
if (Test-Path $venvPy) {
  $py = $venvPy
} elseif (Test-Path "$env:LOCALAPPDATA\Microsoft\WindowsApps\python3.13.exe") {
  $py = "$env:LOCALAPPDATA\Microsoft\WindowsApps\python3.13.exe"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
  $py = (Get-Command python).Source
} else {
  Write-Error "Python not found. Install Python 3.13 and re-run."
}

# Ensure venv exists
$venvDir = Join-Path $PSScriptRoot '..' | Resolve-Path | ForEach-Object { Join-Path $_ '.venv313' }
if (-not (Test-Path $venvDir)) {
  & $py -m venv $venvDir
}

# Upgrade tooling and install deps
& "$venvDir\Scripts\python.exe" -m pip install --upgrade pip setuptools wheel
& "$venvDir\Scripts\python.exe" -m pip install -r (Join-Path $PSScriptRoot '..' | Resolve-Path | ForEach-Object { Join-Path $_ 'requirements.txt' })

# Run API
& "$venvDir\Scripts\python.exe" -m uvicorn --app-dir (Join-Path $PSScriptRoot '..' | Resolve-Path | ForEach-Object { Join-Path $_ 'src' }) ai_trust_manager.api.main:app --port 5080
