@echo off
echo ============================================================
echo   Launching QFT vs Classical FFT Interactive Dashboard
echo ============================================================
cd /d "%~dp0"

if exist ".venv\Scripts\streamlit.exe" (
    ".venv\Scripts\streamlit.exe" run dashboard.py
) else (
    python -m streamlit run dashboard.py
)
pause
