@echo off
REM ====================================================
REM  🤖 AGENT TRADING CRYPTO - INTERFACE PREMIUM
REM ====================================================
REM  Lancement automatique de l'interface ultra premium
REM  avec animations, glassmorphism et rapports Word
REM ====================================================

title Agent Trading Crypto - Premium Interface

echo.
echo ====================================================
echo  🤖 AGENT TRADING CRYPTO - DEMARRAGE
echo ====================================================
echo.
echo  📊 Interface Ultra Premium
echo  💎 Design Glassmorphism
echo  📈 Rapports Word Automatiques
echo  🎨 Animations Fluides
echo.
echo  🚀 Lancement en cours...
echo.

REM Se placer dans le bon répertoire
cd /d "%~dp0"

REM Lancer l'interface premium
python gui_premium.py

REM En cas d'erreur
if errorlevel 1 (
    echo.
    echo ❌ ERREUR AU LANCEMENT
    echo.
    echo Vérifiez:
    echo   1. Python est installé: python --version
    echo   2. Dépendances installées: pip install -r requirements.txt
    echo   3. Fichier .env configuré avec OPENAI_API_KEY
    echo.
    pause
)
