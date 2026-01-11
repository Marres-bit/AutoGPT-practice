# Script de démarrage automatique de l'agent crypto
$pythonPath = (Get-Command python).Source
$scriptPath = "c:\Users\sanim\git-practice\AutoGPT\run_autonomous.py"
$logPath = "c:\Users\sanim\git-practice\AutoGPT\agent_startup.log"

# Log du démarrage
"[$(Get-Date)] Démarrage automatique de l'agent crypto (intervalle: 2h)" | Out-File -Append $logPath

# Démarrer l'agent en mode service avec intervalle de 2h
Start-Process -FilePath $pythonPath -ArgumentList $scriptPath, "--service", "--interval", "2" -WindowStyle Hidden -WorkingDirectory "c:\Users\sanim\git-practice\AutoGPT"

"[$(Get-Date)] Agent démarré avec succès" | Out-File -Append $logPath
