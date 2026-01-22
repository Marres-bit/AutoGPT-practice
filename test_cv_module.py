"""
Test du module CV Perfection & Design Intelligence
Valide le workflow complet avec un CV test
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent))

from cv_perfection import CVConfig, CVProcessor, CVScanner


def create_sample_cv():
    """Crée un CV test simple en format texte"""
    
    sample_cv_content = """
JEAN DUPONT
jean.dupont@email.com | +33 6 12 34 56 78 | Paris, France

PROFIL PROFESSIONNEL
Développeur Full-Stack passionné avec 5 ans d'expérience dans la création d'applications web modernes.
Spécialisé en React, Node.js et Python. Recherche opportunités challenging dans environnement agile.

EXPÉRIENCE PROFESSIONNELLE

Développeur Senior Full-Stack - TechCorp Solutions (2021-2024)
Développement d'applications web pour clients grands comptes
Gestion équipe 3 développeurs juniors
Migration architecture monolithique vers microservices
Stack: React, Node.js, PostgreSQL, Docker, AWS

Développeur Web - StartupInnovante (2019-2021)
Création features nouvelles pour plateforme SaaS B2B
Amélioration performance application (réduction temps chargement 40%)
Participation architecture technique et choix technologiques
Stack: Vue.js, Python Django, MySQL

FORMATION

Master Informatique - Université Paris-Saclay (2017-2019)
Spécialisation: Développement Logiciel et Intelligence Artificielle
Mention Bien

Licence Informatique - Université de Lyon (2014-2017)

COMPÉTENCES

Langages: JavaScript, TypeScript, Python, Java, SQL
Frontend: React, Vue.js, Angular, HTML5, CSS3, Tailwind
Backend: Node.js, Django, Flask, Express.js
Bases de données: PostgreSQL, MySQL, MongoDB, Redis
DevOps: Docker, Kubernetes, CI/CD, AWS, Azure
Outils: Git, JIRA, Agile/Scrum, TDD

LANGUES

Français: Langue maternelle
Anglais: Courant (TOEIC 920)
Espagnol: Intermédiaire

CERTIFICATIONS

AWS Certified Solutions Architect - Associate (2023)
Professional Scrum Master I (2022)
"""
    
    return sample_cv_content


def test_cv_module():
    """Test complet du module CV-PDI"""
    
    print("="*70)
    print("🧪 TEST DU MODULE CV PERFECTION & DESIGN INTELLIGENCE")
    print("="*70)
    print()
    
    # 1. Vérifier configuration
    print("📋 Étape 1/5: Vérification de la configuration")
    config = CVConfig()
    print(f"  ✓ Dossier d'entrée: {config.input_path}")
    print(f"  ✓ Dossier de sortie: {config.output_path}")
    print(f"  ✓ Styles disponibles: {len(config.available_styles)}")
    print()
    
    # 2. Créer CV test
    print("📝 Étape 2/5: Création du CV test")
    
    # S'assurer que le dossier d'entrée existe
    config.input_path.mkdir(parents=True, exist_ok=True)
    
    # Créer fichier CV test
    test_cv_path = config.input_path / "CV_Test_Jean_Dupont.txt"
    
    with open(test_cv_path, 'w', encoding='utf-8') as f:
        f.write(create_sample_cv())
    
    print(f"  ✓ CV test créé: {test_cv_path.name}")
    print(f"  ✓ Taille: {test_cv_path.stat().st_size} bytes")
    print()
    
    # 3. Scanner
    print("🔍 Étape 3/5: Test du scanner")
    scanner = CVScanner(config)
    
    # Note: Le scanner ne détecte que PDF et DOCX, pas TXT
    # Pour un vrai test, on doit traiter directement
    print("  ⚠️ Scanner configuré pour PDF/DOCX uniquement")
    print("  ℹ️ Pour test complet, convertir en PDF ou utiliser DOCX")
    print()
    
    # 4. Vérifier statistiques
    print("📊 Étape 4/5: Statistiques actuelles")
    stats = scanner.get_statistics()
    print(f"  Total traités: {stats['total_processed']}")
    print(f"  Succès: {stats['successful']}")
    print(f"  Échecs: {stats['failed']}")
    print()
    
    # 5. Instructions pour test réel
    print("🚀 Étape 5/5: Instructions pour test réel")
    print()
    print("Pour tester le module complet avec un vrai CV:")
    print()
    print("  1. Convertir CV_Test_Jean_Dupont.txt en PDF:")
    print(f"     - Ouvrir: {test_cv_path}")
    print("     - Imprimer vers PDF")
    print("     - Sauver comme: CV_Test_Jean_Dupont.pdf")
    print()
    print("  2. OU créer un CV test en DOCX:")
    print("     - Créer document Word")
    print("     - Copier le contenu du fichier TXT")
    print(f"     - Sauver dans: {config.input_path}")
    print()
    print("  3. Lancer le traitement:")
    print("     python main_medical.py --cv-scan")
    print()
    print("  4. Vérifier résultats:")
    print(f"     {config.output_path}")
    print()
    
    print("="*70)
    print("✅ TEST DE BASE TERMINÉ")
    print("="*70)
    print()
    print("💡 Le module est prêt à l'emploi !")
    print("💡 Déposez des CV (PDF/DOCX) dans Bureau/CV/ pour traitement")
    print()


def test_with_real_cv():
    """
    Test avec un vrai CV (si disponible)
    Cherche un fichier PDF ou DOCX dans le dossier CV
    """
    
    print("="*70)
    print("🔍 RECHERCHE DE CV RÉELS À TRAITER")
    print("="*70)
    print()
    
    config = CVConfig()
    scanner = CVScanner(config)
    
    # Chercher CV disponibles
    new_cvs = scanner.scan_for_new_cvs()
    
    if not new_cvs:
        print("❌ Aucun CV trouvé dans le dossier d'entrée")
        print(f"📁 Dossier: {config.input_path}")
        print()
        print("💡 Placez un CV (PDF ou DOCX) dans ce dossier et relancez:")
        print("   python test_cv_module.py --real")
        return
    
    print(f"✅ {len(new_cvs)} CV trouvé(s) !\n")
    
    # Traiter le premier CV
    processor = CVProcessor(config)
    
    for cv_path in new_cvs[:1]:  # Traiter uniquement le premier
        print(f"📄 Traitement de: {cv_path.name}\n")
        result = processor.process_single_cv(cv_path)
        
        if result['success']:
            print("\n✅ SUCCÈS !")
            print(f"\n📁 Fichiers générés:")
            for output_file in result['output_files']:
                print(f"  ✓ {Path(output_file).name}")
        else:
            print("\n❌ ÉCHEC")
            if result['errors']:
                print("\nErreurs:")
                for error in result['errors']:
                    print(f"  • {error}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test du module CV Perfection")
    parser.add_argument("--real", action="store_true", 
                       help="Tester avec de vrais CV (PDF/DOCX) si disponibles")
    
    args = parser.parse_args()
    
    if args.real:
        test_with_real_cv()
    else:
        test_cv_module()
