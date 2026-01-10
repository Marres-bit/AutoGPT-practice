@echo off
echo ============================================
echo   Dr. Bob - Medical AI Agent
echo   Assistant Medical Autonome
echo ============================================
echo.
echo Demarrage de l'agent medical...
echo.

cd /d "%~dp0"
python main_medical.py

echo.
echo Agent ferme.
pause
