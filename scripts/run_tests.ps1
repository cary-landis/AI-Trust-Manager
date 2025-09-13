$ErrorActionPreference = 'Stop'

# PSScriptRoot points to scripts/; compute repo root
$repoRoot = Join-Path $PSScriptRoot '..' | Resolve-Path

$venvPy = Join-Path $repoRoot '.venv313\Scripts\python.exe'
if (-not (Test-Path $venvPy)) {
  if (Test-Path "$env:LOCALAPPDATA\Microsoft\WindowsApps\python3.13.exe") {
    & "$env:LOCALAPPDATA\Microsoft\WindowsApps\python3.13.exe" -m venv (Join-Path $repoRoot '.venv313')
  } elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & (Get-Command python).Source -m venv (Join-Path $repoRoot '.venv313')
  } else {
    Write-Error "Python not found. Install Python 3.13 and re-run."
  }
}

& $venvPy -m pip install --upgrade pip setuptools wheel
& $venvPy -m pip install -r (Join-Path $repoRoot 'requirements.txt')

# Run the table-driven runner
& $venvPy (Join-Path $repoRoot 'tests\run_tests.py')
