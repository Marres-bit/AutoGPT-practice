@echo off
REM Script de démarrage automatique avec apprentissage permanent
REM Auteur: AI Agent Autonome
REM Date: 2026-01-10

echo ========================================
echo  🧠 AGENT AI - MODE APPRENTISSAGE
echo ========================================
echo.
echo Configuration:
echo   - Durée: 2 jours
echo   - Intervalle: 1 heure
echo   - Apprentissage: PERMANENT
echo   - Mode: TestNet
echo.
echo Fichiers generés:
echo   - learning_state.json (état apprentissage)
echo   - mistakes_log.json (historique erreurs)
echo   - error_patterns.json (patterns detectés)
echo   - sp_agent.log (logs détaillés)
echo   - last_cycle_summary.txt (résumé dernier cycle)
echo.
echo ========================================
echo.

pause

echo.
echo 🚀 Démarrage de l'agent...
echo.

cd /d "%~dp0"
python run_testnet_loop.py

echo.
echo ========================================
echo  ✅ Agent terminé
echo ========================================
echo.
echo Pour consulter les résultats:
echo   - cat last_cycle_summary.txt
echo   - cat learning_state.json
echo   - tail sp_agent.log
echo.

pause
