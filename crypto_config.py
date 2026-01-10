"""
Configuration du Système Autonome de Crypto-Analyse
Fichier centralisé pour tous les paramètres
"""

# ═══════════════════════════════════════════════════════════════════
# 1️⃣ PARAMÈTRES DU SCHEDULER
# ═══════════════════════════════════════════════════════════════════

# Intervalle d'analyse par défaut (en heures)
DEFAULT_ANALYSIS_INTERVAL = 4

# Lancer l'analyse immédiatement au démarrage? 
ANALYZE_ON_STARTUP = True

# Mode daemon (pas de GUI)
DAEMON_MODE = False


# ═══════════════════════════════════════════════════════════════════
# 2️⃣ PARAMÈTRES DE L'ANALYSEUR CRYPTO
# ═══════════════════════════════════════════════════════════════════

# Variation minimale à considérer comme significative (%)
MIN_VARIATION_THRESHOLD = 5.0

# Nombre maximum de cryptos à analyser
MAX_CRYPTOS_ANALYZED = 50

# Nombre de cryptos à afficher (top gagnants/perdants)
TOP_CRYPTOS_DISPLAY = 20

# Source API (coingecko ou binance)
CRYPTO_API_SOURCE = "coingecko"  # "coingecko" ou "binance"

# Timeout pour les requêtes API (en secondes)
API_TIMEOUT = 10


# ═══════════════════════════════════════════════════════════════════
# 3️⃣ PARAMÈTRES DES RAPPORTS WORD
# ═══════════════════════════════════════════════════════════════════

# Chemin du Bureau (défaut: Desktop de l'utilisateur)
DESKTOP_PATH = None  # None = auto-détection

# Format du nom de fichier
REPORT_FILENAME_FORMAT = "Crypto_Compte_rendu_{date}.docx"

# Nombre maximum de rapports à conserver (0 = illimité)
MAX_REPORTS_TO_KEEP = 0

# Inclure graphiques dans les rapports?
INCLUDE_CHARTS = False  # À implémenter dans phase 2

# Ajouter historique des prix?
INCLUDE_PRICE_HISTORY = False  # À implémenter dans phase 2


# ═══════════════════════════════════════════════════════════════════
# 4️⃣ PARAMÈTRES DE FILTERING DES CRYPTOS
# ═══════════════════════════════════════════════════════════════════

# Inclure les petites cap? (market cap < $100M)
INCLUDE_SMALL_CAP = True

# Inclure les stablecoins? (USDT, USDC, etc.)
INCLUDE_STABLECOINS = False

# Langues d'analyse disponibles
ANALYSIS_LANGUAGES = ["fr", "en", "es", "de"]
DEFAULT_LANGUAGE = "fr"

# Détail du résumé (brief, medium, detailed)
ANALYSIS_DETAIL_LEVEL = "medium"


# ═══════════════════════════════════════════════════════════════════
# 5️⃣ PARAMÈTRES DE NOTIFICATION
# ═══════════════════════════════════════════════════════════════════

# Notifier quand variation extrême détectée (%)
ALERT_EXTREME_VARIATION = 50.0

# Notifier si une crypto abandonnée soudainement?
ALERT_ABANDONED = True

# Notifier si volume d'échange anormal?
ALERT_UNUSUAL_VOLUME = True

# Méthodes de notification (console, email, webhook)
NOTIFICATION_METHODS = ["console"]  # À implémenter


# ═══════════════════════════════════════════════════════════════════
# 6️⃣ PARAMÈTRES DE SÉCURITÉ
# ═══════════════════════════════════════════════════════════════════

# Vérifier la validité des données avant traitement?
VALIDATE_DATA = True

# Retry automatique en cas d'erreur API?
AUTO_RETRY = True

# Nombre de tentatives
MAX_RETRIES = 3

# Délai entre les tentatives (en secondes)
RETRY_DELAY = 5


# ═══════════════════════════════════════════════════════════════════
# 7️⃣ PARAMÈTRES DE DÉMARRAGE AUTOMATIQUE WINDOWS
# ═══════════════════════════════════════════════════════════════════

# Autoriser le démarrage automatique au boot Windows?
ENABLE_WINDOWS_STARTUP = False  # À changer manuellement ou via GUI

# Mode de démarrage (startup ou service)
STARTUP_MODE = "startup"  # "startup" (registre) ou "service" (Windows Service)

# Cacher la fenêtre au démarrage?
HIDE_WINDOW_ON_STARTUP = False


# ═══════════════════════════════════════════════════════════════════
# 8️⃣ PARAMÈTRES DE LOGGING
# ═══════════════════════════════════════════════════════════════════

# Niveau de log (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL = "INFO"

# Dossier pour les logs
LOG_FOLDER = None  # None = dossier du script

# Garder historique des logs?
KEEP_LOG_HISTORY = True

# Nombre maximum de fichiers log
MAX_LOG_FILES = 10


# ═══════════════════════════════════════════════════════════════════
# 9️⃣ PARAMÈTRES DE PERFORMANCE
# ═══════════════════════════════════════════════════════════════════

# Forcer le garbage collection après analyse?
FORCE_GARBAGE_COLLECTION = False

# Limiter la mémoire utilisée (en MB, 0 = illimité)
MEMORY_LIMIT = 0

# Nombre de threads parallèles pour analyses
PARALLEL_THREADS = 1  # 1 = séquentiel


# ═══════════════════════════════════════════════════════════════════
# 🔟 PARAMÈTRES DE CACHE
# ═══════════════════════════════════════════════════════════════════

# Cacher les résultats API pour éviter appels répétés?
USE_CACHE = False

# TTL du cache (en minutes)
CACHE_TTL_MINUTES = 30

# Dossier de cache
CACHE_FOLDER = None  # None = dossier temp


# ═══════════════════════════════════════════════════════════════════
# FONCTION POUR CHARGER LA CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

def get_config():
    """Retourne la configuration actuelle"""
    return {
        # Scheduler
        "interval": DEFAULT_ANALYSIS_INTERVAL,
        "startup_analysis": ANALYZE_ON_STARTUP,
        "daemon_mode": DAEMON_MODE,
        
        # Analyseur
        "min_variation": MIN_VARIATION_THRESHOLD,
        "max_cryptos": MAX_CRYPTOS_ANALYZED,
        "top_display": TOP_CRYPTOS_DISPLAY,
        "api_source": CRYPTO_API_SOURCE,
        "timeout": API_TIMEOUT,
        
        # Rapports
        "report_format": REPORT_FILENAME_FORMAT,
        "max_reports": MAX_REPORTS_TO_KEEP,
        
        # Notification
        "alert_extreme": ALERT_EXTREME_VARIATION,
        "language": DEFAULT_LANGUAGE,
        
        # Windows
        "enable_startup": ENABLE_WINDOWS_STARTUP,
        "startup_mode": STARTUP_MODE,
        
        # Autres
        "log_level": LOG_LEVEL,
        "auto_retry": AUTO_RETRY,
    }


def print_config():
    """Affiche la configuration actuelle"""
    print("\n" + "="*70)
    print("CONFIGURATION AUTONOME DE CRYPTO-ANALYSE")
    print("="*70)
    
    config = get_config()
    for key, value in config.items():
        print(f"  {key:25} = {value}")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    print_config()
