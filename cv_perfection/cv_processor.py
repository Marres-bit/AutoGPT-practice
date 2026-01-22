"""
CV Processor - Orchestrateur principal du traitement de CV
Coordonne Scanner → Analyzer → Optimizer → Designer → Report
"""

from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import logging

from .config import CVConfig
from .cv_scanner import CVScanner
from .cv_analyzer import CVAnalyzer, CVAnalysis
from .cv_optimizer import CVOptimizer, OptimizedContent
from .cv_designer import CVDesigner


class CVProcessor:
    """Processeur principal - orchestre le workflow complet"""
    
    def __init__(self, config: Optional[CVConfig] = None):
        self.config = config or CVConfig()
        self.scanner = CVScanner(self.config)
        self.analyzer = CVAnalyzer()
        self.optimizer = CVOptimizer()
        self.designer = CVDesigner(self.config)
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Configure le logger"""
        logger = logging.getLogger('CVProcessor')
        logger.setLevel(logging.INFO)
        
        # Handler fichier
        log_path = self.config.output_path / 'cv_processor.log'
        fh = logging.FileHandler(log_path, encoding='utf-8')
        fh.setLevel(logging.INFO)
        
        # Format
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
        # Handler console
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        return logger
    
    def process_single_cv(self, cv_path: Path) -> Dict:
        """
        Traite un CV complet: analyse, optimise, design, rapport
        
        Args:
            cv_path: Chemin vers le CV à traiter
        
        Returns:
            Dictionnaire avec résultats du traitement
        """
        self.logger.info("="*70)
        self.logger.info(f"🚀 DÉBUT TRAITEMENT: {cv_path.name}")
        self.logger.info("="*70)
        
        result = {
            'success': False,
            'input_file': str(cv_path),
            'output_files': [],
            'analysis': None,
            'errors': []
        }
        
        try:
            # ÉTAPE 1: Analyse
            self.logger.info("\n📊 ÉTAPE 1/4: Analyse du CV")
            analysis = self.analyzer.analyze(cv_path)
            result['analysis'] = {
                'overall_score': analysis.overall_score,
                'page_count': analysis.page_count,
                'word_count': analysis.word_count,
                'sections_found': list(analysis.sections.keys()),
                'issues_count': len(analysis.issues),
                'warnings_count': len(analysis.warnings)
            }
            
            self.logger.info(f"  Score global: {analysis.overall_score:.1f}/10")
            self.logger.info(f"  Sections détectées: {len(analysis.sections)}")
            self.logger.info(f"  Problèmes: {len(analysis.issues)} | Avertissements: {len(analysis.warnings)}")
            
            # ÉTAPE 2: Optimisation
            self.logger.info("\n✨ ÉTAPE 2/4: Optimisation du contenu")
            optimized = self.optimizer.optimize(analysis, target_language='fr')
            self.logger.info(f"  {len(optimized.sections)} sections optimisées")
            
            # ÉTAPE 3: Design
            self.logger.info("\n🎨 ÉTAPE 3/4: Création du design professionnel")
            
            # Nom de base pour les fichiers
            base_name = cv_path.stem
            candidate_name = self._extract_candidate_name(analysis.raw_text)
            if candidate_name:
                base_name = f"CV_Parfait_{candidate_name}"
            else:
                base_name = f"CV_Parfait_{base_name}"
            
            # Générer CV(s)
            if self.config.generate_multiple_styles:
                self.logger.info("  Génération multiple styles activée")
                output_files = self.designer.create_multiple_styles(
                    analysis=analysis,
                    optimized_content=optimized,
                    output_dir=self.config.output_path,
                    base_filename=base_name
                )
                result['output_files'] = [str(f) for f in output_files]
            else:
                # Un seul style (défaut)
                style = self.config.default_style
                output_path = self.config.output_path / f"{base_name}_{style}.pdf"
                
                success = self.designer.create_professional_cv(
                    analysis=analysis,
                    optimized_content=optimized,
                    output_path=output_path,
                    style=style
                )
                
                if success:
                    result['output_files'].append(str(output_path))
            
            self.logger.info(f"  ✅ {len(result['output_files'])} fichiers créés")
            
            # ÉTAPE 4: Rapport d'amélioration
            if self.config.generate_improvement_report:
                self.logger.info("\n📝 ÉTAPE 4/4: Génération du rapport")
                report_path = self._generate_improvement_report(
                    cv_path=cv_path,
                    analysis=analysis,
                    optimized=optimized,
                    output_files=result['output_files']
                )
                if report_path:
                    result['output_files'].append(str(report_path))
                    self.logger.info(f"  Rapport: {report_path.name}")
            
            # Marquer comme traité
            self.scanner.mark_as_processed(cv_path, success=True)
            result['success'] = True
            
            self.logger.info("\n" + "="*70)
            self.logger.info("✅ TRAITEMENT TERMINÉ AVEC SUCCÈS")
            self.logger.info("="*70)
            
        except Exception as e:
            self.logger.error(f"\n❌ ERREUR: {e}")
            import traceback
            traceback.print_exc()
            result['errors'].append(str(e))
            self.scanner.mark_as_processed(cv_path, success=False, error=str(e))
        
        return result
    
    def process_all_pending(self) -> Dict:
        """
        Traite tous les CV en attente dans le dossier surveillé
        
        Returns:
            Statistiques de traitement
        """
        self.logger.info("🔍 Recherche de nouveaux CV...")
        
        new_cvs = self.scanner.scan_for_new_cvs()
        
        if not new_cvs:
            self.logger.info("✅ Aucun nouveau CV à traiter")
            return {'processed': 0, 'successful': 0, 'failed': 0}
        
        self.logger.info(f"📚 {len(new_cvs)} CV(s) à traiter\n")
        
        stats = {'processed': 0, 'successful': 0, 'failed': 0}
        
        for cv_path in new_cvs:
            result = self.process_single_cv(cv_path)
            stats['processed'] += 1
            if result['success']:
                stats['successful'] += 1
            else:
                stats['failed'] += 1
            
            self.logger.info("")  # Ligne vide entre CV
        
        # Résumé final
        self.logger.info("\n" + "="*70)
        self.logger.info("📊 RÉSUMÉ FINAL")
        self.logger.info("="*70)
        self.logger.info(f"Total traités: {stats['processed']}")
        self.logger.info(f"Succès: ✅ {stats['successful']}")
        self.logger.info(f"Échecs: ❌ {stats['failed']}")
        self.logger.info("="*70)
        
        return stats
    
    def _extract_candidate_name(self, text: str) -> Optional[str]:
        """Extrait le nom du candidat (première ligne généralement)"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            # Première ligne non vide, nettoyée
            name = lines[0]
            # Supprimer caractères spéciaux pour nom de fichier
            name = "".join(c if c.isalnum() or c.isspace() else "_" for c in name)
            name = "_".join(name.split())  # Espaces → underscores
            return name[:50]  # Limiter longueur
        return None
    
    def _generate_improvement_report(
        self,
        cv_path: Path,
        analysis: CVAnalysis,
        optimized: OptimizedContent,
        output_files: list
    ) -> Optional[Path]:
        """Génère un rapport d'amélioration en texte"""
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_path = self.config.output_path / f"Rapport_{cv_path.stem}_{timestamp}.txt"
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("="*70 + "\n")
                f.write("CV PERFECTION & DESIGN INTELLIGENCE - RAPPORT D'AMÉLIORATION\n")
                f.write("="*70 + "\n\n")
                
                f.write(f"📄 CV Original: {cv_path.name}\n")
                f.write(f"📅 Date de traitement: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("="*70 + "\n")
                f.write("📊 ANALYSE DU CV ORIGINAL\n")
                f.write("="*70 + "\n\n")
                
                f.write(f"Score global: {analysis.overall_score:.1f}/10\n")
                f.write(f"  • Structure: {analysis.structure_score:.1f}/10\n")
                f.write(f"  • Compatibilité ATS: {analysis.ats_score:.1f}/10\n")
                f.write(f"  • Typographie: {analysis.typography_score:.1f}/10\n")
                f.write(f"  • Hiérarchie visuelle: {analysis.visual_hierarchy_score:.1f}/10\n")
                f.write(f"  • Lisibilité: {analysis.readability_score:.1f}/10\n\n")
                
                f.write(f"Statistiques:\n")
                f.write(f"  • Pages: {analysis.page_count}\n")
                f.write(f"  • Mots: {analysis.word_count}\n")
                f.write(f"  • Sections détectées: {len(analysis.sections)}\n\n")
                
                if analysis.issues:
                    f.write("❌ PROBLÈMES DÉTECTÉS:\n")
                    for issue in analysis.issues:
                        f.write(f"  • {issue}\n")
                    f.write("\n")
                
                if analysis.warnings:
                    f.write("⚠️ AVERTISSEMENTS:\n")
                    for warning in analysis.warnings:
                        f.write(f"  • {warning}\n")
                    f.write("\n")
                
                f.write("="*70 + "\n")
                f.write("✨ AMÉLIORATIONS APPORTÉES\n")
                f.write("="*70 + "\n\n")
                
                for improvement in optimized.improvements:
                    f.write(f"✓ {improvement}\n")
                f.write("\n")
                
                f.write("="*70 + "\n")
                f.write("💡 RECOMMANDATIONS\n")
                f.write("="*70 + "\n\n")
                
                for rec in analysis.recommendations:
                    f.write(f"{rec}\n")
                f.write("\n")
                
                f.write("="*70 + "\n")
                f.write("🎨 CHOIX DE DESIGN\n")
                f.write("="*70 + "\n\n")
                
                f.write(f"Style appliqué: {self.config.default_style}\n")
                f.write(f"Pourquoi ce design ?\n")
                f.write(f"  • Design moderne et professionnel\n")
                f.write(f"  • Optimisé pour la lecture rapide par recruteurs\n")
                f.write(f"  • Compatible ATS (Applicant Tracking Systems)\n")
                f.write(f"  • Hiérarchie visuelle claire\n")
                f.write(f"  • Typographie professionnelle\n\n")
                
                f.write("="*70 + "\n")
                f.write("📁 FICHIERS GÉNÉRÉS\n")
                f.write("="*70 + "\n\n")
                
                for output_file in output_files:
                    f.write(f"✓ {Path(output_file).name}\n")
                f.write("\n")
                
                f.write("="*70 + "\n")
                f.write("💼 CONSEILS POUR L'UTILISATION\n")
                f.write("="*70 + "\n\n")
                
                f.write("1. Utilisez le CV généré tel quel pour vos candidatures\n")
                f.write("2. Adaptez les mots-clés selon l'offre d'emploi ciblée\n")
                f.write("3. Exportez en PDF pour garantir le rendu visuel\n")
                f.write("4. Testez la compatibilité ATS avec des outils en ligne\n")
                f.write("5. Personnalisez la lettre de motivation en accord\n\n")
                
                f.write("="*70 + "\n")
                f.write("✅ Traitement terminé avec succès !\n")
                f.write("="*70 + "\n")
            
            return report_path
            
        except Exception as e:
            self.logger.error(f"Erreur génération rapport: {e}")
            return None
