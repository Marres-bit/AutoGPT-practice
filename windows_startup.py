"""
Module Auto-Startup Windows
Enregistre l'application pour démarrer avec Windows
"""

import winreg
import sys
from pathlib import Path
import subprocess


class WindowsAutoStartup:
    """Gère le démarrage automatique avec Windows"""
    
    REGISTRY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
    APP_NAME = "CryptoAnalyzerAuto"
    
    @staticmethod
    def get_script_path() -> str:
        """Retourne le chemin du script main.py"""
        return str(Path(__file__).parent / "main.py")
    
    @staticmethod
    def get_python_path() -> str:
        """Retourne le chemin de l'exécutable Python"""
        return sys.executable
    
    @classmethod
    def enable_startup(cls) -> bool:
        """Active le démarrage au boots"""
        try:
            script_path = cls.get_script_path()
            python_path = cls.get_python_path()
            
            # Commande: python main.py --headless (pour mode arrière-plan)
            command = f'"{python_path}" "{script_path}" --autonomous'
            
            # Accès au registre
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, cls.REGISTRY_PATH, 0, winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, cls.APP_NAME, 0, winreg.REG_SZ, command)
            
            print(f"✅ Démarrage automatique activé")
            print(f"   Commande: {command}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur activation démarrage: {e}")
            return False
    
    @classmethod
    def disable_startup(cls) -> bool:
        """Désactive le démarrage automatique"""
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, cls.REGISTRY_PATH, 0, winreg.KEY_WRITE) as key:
                winreg.DeleteValue(key, cls.APP_NAME)
            
            print(f"✅ Démarrage automatique désactivé")
            return True
            
        except FileNotFoundError:
            print("ℹ️ L'entrée n'existe pas")
            return True
        except Exception as e:
            print(f"❌ Erreur désactivation: {e}")
            return False
    
    @classmethod
    def is_enabled(cls) -> bool:
        """Vérifie si le démarrage automatique est activé"""
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, cls.REGISTRY_PATH, 0, winreg.KEY_READ) as key:
                winreg.QueryValueEx(key, cls.APP_NAME)
            return True
        except FileNotFoundError:
            return False
    
    @classmethod
    def create_batch_launcher(cls) -> str:
        """Crée un fichier batch pour lancer l'app en arrière-plan"""
        batch_path = Path(__file__).parent / "run_autonomous.bat"
        
        script_path = cls.get_script_path()
        python_path = cls.get_python_path()
        
        batch_content = f"""@echo off
REM Crypto Analyzer - Autonomous Launcher
REM Démarre l'analyseur en arrière-plan au démarrage Windows

title Crypto Analyzer Service
cd /d "{Path(__file__).parent}"

REM Lancer Python en mode daemon (sans console)
start "" /min "{python_path}" "{script_path}" --autonomous

REM Cette fenêtre se ferme mais le script reste actif
exit
"""
        
        with open(batch_path, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        
        print(f"✅ Batch launcher créé: {batch_path}")
        return str(batch_path)


def main():
    """Test du module"""
    print("🔧 Gestion du Démarrage Automatique Windows\n")
    
    # Vérifier le statut
    if WindowsAutoStartup.is_enabled():
        print("✅ Démarrage automatique: ACTIVÉ")
        print("\nPour désactiver:")
        print("  WindowsAutoStartup.disable_startup()")
    else:
        print("❌ Démarrage automatique: DÉSACTIVÉ")
        print("\nPour activer:")
        print("  WindowsAutoStartup.enable_startup()")
    
    # Créer le batch launcher
    batch_path = WindowsAutoStartup.create_batch_launcher()
    print(f"\n📝 Batch launcher créé: {batch_path}")
    print("\nVous pouvez aussi ajouter directement à StartUp:")
    print("  Appuyez sur WIN+R")
    print("  Tapez: shell:startup")
    print("  Puis copiez le fichier run_autonomous.bat dedans")


if __name__ == "__main__":
    main()
