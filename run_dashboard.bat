@echo off
echo Starting QFT vs Classical FFT Interactive Dashboard...
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    start "" ".venv\Scripts\python.exe" serve.py
) else (
    start "" python serve.py
)
