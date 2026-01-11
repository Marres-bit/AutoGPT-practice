"""
Module Scheduler Autonome Ultra - Version 2.0
Gère les tâches périodiques en arrière-plan avec système d'apprentissage permanent,
analyse stratégique avancée et reporting automatisé
"""

from pathlib import Path
from datetime import datetime, timedelta
import json
import random
import threading
import time
from docx import Document
from learning_engine import LearningEngine
from strategy_analyzer import StrategyAnalyzer, MarketCondition
from strategy_fusion import StrategyFusionEngine
from advanced_reporting import AdvancedReportingSystem
from exchange_connector import get_exchange_connector
from risk_manager import RiskManager, RiskLevel
from structured_logger import get_logger

class AutonomousScheduler:
    def __init__(self, interval_hours: int = 4, gui_callback=None, project_root: Path | str | None = None):
        """
        Initialise le scheduler avec tous les systèmes avancés
        
        Args:
            interval_hours: Intervalle d'analyse en heures (défaut: 4h)
            gui_callback: Fonction de callback pour mettre à jour la GUI
            project_root: dossier où seront écrits les fichiers
        """
        self.interval_hours = interval_hours
        self.gui_callback = gui_callback
        self._running = False
        self._continuous_thread = None
        self._next_analysis = datetime.utcnow() + timedelta(hours=self.interval_hours)
        self.project_root = Path(project_root) if project_root else Path(__file__).parent
        
        # Moteur d'apprentissage permanent (amélioré)
        self.learning_engine = LearningEngine(self.project_root)
        print("[OK] Moteur d'apprentissage permanent activé (v2.0)")
        
        # Analyseur de stratégies (BullX, Photon, Glider, Binance)
        self.strategy_analyzer = StrategyAnalyzer(self.project_root)
        print("[OK] Analyseur de stratégies initialisé (BullX, Photon, Glider, Binance)")
        
        # Moteur de fusion adaptatif
        self.strategy_fusion = StrategyFusionEngine(self.project_root, self.strategy_analyzer)
        print("[OK] Moteur de fusion stratégique activé")
        
        # Système de reporting automatisé
        self.reporting_system = AdvancedReportingSystem(self.project_root)
        print("[OK] Système de reporting automatisé activé")
        
        # Connecteur Exchange (prix réels)
        self.exchange = get_exchange_connector(testnet=True)
        status = self.exchange.get_connection_status()
        mode_label = "TESTNET" if status['testnet'] else "PRODUCTION"
        print(f"[OK] Exchange connecté: Binance {mode_label} (prix réels)")
        
        # Risk Manager (gestion risques professionnelle)
        self.risk_manager = RiskManager(
            project_root=self.project_root,
            initial_capital=10000.0,
            risk_level=RiskLevel.MODERATE
        )
        print("[OK] Risk Manager activé (Kelly Criterion, Max Drawdown 20%)")
        
        # Logger structuré
        self.logger = get_logger("trading", self.project_root / "logs")
        self.logger.info("Autonomous Scheduler initialisé", mode=mode_label, interval_hours=interval_hours)
        
        self.cycle_count = 0

    def start(self):
        """Démarre le scheduler en arrière-plan (boucle continue)."""
        self._next_analysis = datetime.utcnow() + timedelta(hours=self.interval_hours)
        if self._continuous_thread and self._continuous_thread.is_alive():
            print("⚠️ Scheduler déjà actif")
            return
        self._running = True
        self._continuous_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self._continuous_thread.start()
        print(f"🚀 Scheduler autonome démarré (analyse toutes les {self.interval_hours}h)")

    def start_continuous(self, sp_mode: bool = False):
        """Alias explicite pour démarrer la boucle continue (compatibilité API)."""
        return self.start()

    def stop(self):
        """Arrête le scheduler et attend la fin du thread (si possible)."""
        self._running = False
        if self._continuous_thread and self._continuous_thread.is_alive():
            self._continuous_thread.join(timeout=2)
        print("⏸️ Scheduler arrêté")
    
    def _run_scheduler(self):
        """Boucle principale du scheduler (run en thread séparé)"""
        while self._running:
            try:
                self.run_one_shot(simulate=True)
            except Exception:
                pass
            time.sleep(self.interval_hours * 3600)

    def get_next_analysis_time(self):
        return self._next_analysis
    
    def run_one_shot(self, simulate: bool = True):
        """
        Cycle complet avec analyse stratégique avancée:
          - Détection condition de marché
          - Sélection/fusion stratégies optimales
          - Analyse post-trade avec apprentissage
          - Auto-amélioration des règles
          - Génération rapports 4h et quotidiens
        """
        project_root = self.project_root
        log_path = project_root / "sp_agent.log"
        summary_path = project_root / "last_cycle_summary.txt"
        capital_path = project_root / "capital_state.json"

        def _log(msg: str):
            ts = datetime.utcnow().isoformat() + "Z"
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"{ts} {msg}\n")

        try:
            self.cycle_count += 1
            _log(f"═══════ DÉBUT CYCLE #{self.cycle_count} ═══════")
            
            # ═══════════════════════════════════════════════════════
            # 1️⃣ CHARGEMENT CAPITAL & INITIALISATION
            # ═══════════════════════════════════════════════════════
            if capital_path.exists():
                with open(capital_path, "r", encoding="utf-8") as f:
                    capital = json.load(f)
            else:
                capital = {"principal": 10000.0, "investment": 0.0}
                with open(capital_path, "w", encoding="utf-8") as f:
                    json.dump(capital, f, indent=2)

            if capital.get("investment", 0.0) == 0.0:
                invest_amount = round(capital["principal"] * 0.7, 2)
                capital["principal"] = round(capital["principal"] - invest_amount, 2)
                capital["investment"] = round(invest_amount, 2)
                _log(f"INIT_INVEST: {invest_amount} vers investment")

            # ═══════════════════════════════════════════════════════
            # 2️⃣ ANALYSE DE MARCHÉ RÉELLE (PRIX RÉELS)
            # ═══════════════════════════════════════════════════════
            assets = ["BTC", "ETH", "SOL"]
            
            # Récupérer variations réelles du marché
            try:
                market = self.exchange.calculate_market_changes()
                _log(f"MARKET_REAL: {market} (source: Binance Testnet)")
                print(f"📊 Prix réels récupérés: {len(market)} cryptos")
            except Exception as e:
                _log(f"WARNING: Erreur récupération prix réels: {e}, fallback simulation")
                market = {a: round(random.uniform(-2.0, 3.0), 2) for a in assets}
                _log(f"MARKET_SIMULATED: {market}")
            
            # ═══════════════════════════════════════════════════════
            # 3️⃣ DÉTECTION CONDITION DE MARCHÉ
            # ═══════════════════════════════════════════════════════
            market_condition = self.strategy_analyzer.detect_market_condition(market)
            _log(f"MARKET_CONDITION: {market_condition.value}")
            print(f"📊 Condition de marché: {market_condition.value}")
            
            # ═══════════════════════════════════════════════════════
            # 4️⃣ SÉLECTION/FUSION STRATÉGIE OPTIMALE
            # ═══════════════════════════════════════════════════════
            current_strategy = self.strategy_fusion.fuse_strategies(
                market_condition.value,
                force_refusion=False
            )
            # Protection contre None
            if current_strategy is None:
                current_strategy = {
                    "name": "Default_Conservative_Strategy",
                    "type": "conservative",
                    "confidence": 0.5,
                    "rules": []
                }
            strategy_name = current_strategy.get("name", "default")
            _log(f"STRATEGY_SELECTED: {strategy_name} (confiance: {current_strategy.get('confidence', 0):.2f})")
            print(f"🎯 Stratégie: {strategy_name}")
            
            # ═══════════════════════════════════════════════════════
            # 5️⃣ GÉNÉRATION SIGNAUX DE TRADING
            # ═══════════════════════════════════════════════════════
            best_asset = max(market.items(), key=lambda x: x[1])
            worst_asset = min(market.items(), key=lambda x: x[1])
            
            trading_signals = self.strategy_fusion.get_trading_signals(market, best_asset[0])
            _log(f"TRADING_SIGNALS: {trading_signals}")
            
            # Obtenir aussi la recommandation d'apprentissage
            learning_recommendation = self.learning_engine.get_trading_recommendation(market)
            best_choice = learning_recommendation.get("best_choice")
            
            # DEBUG: Logger les recommandations
            _log(f"LEARNING_RECOMMENDATION: best_choice={best_choice}")
            if best_choice:
                _log(f"BEST_CHOICE_DETAILS: asset={best_choice.get('asset')}, should_trade={best_choice.get('should_trade')}, reason={best_choice.get('reason')}, confidence={best_choice.get('confidence')}")
            
            # ═══════════════════════════════════════════════════════
            # 6️⃣ DÉCISION & EXÉCUTION TRADE SIMULÉ
            # ═══════════════════════════════════════════════════════
            decision = "HOLD"
            trade = None
            justifications = []
            
            # Combiner signaux de fusion et apprentissage
            if (trading_signals.get("action") == "OPEN_LONG" and 
                best_choice and best_choice.get("should_trade") and 
                capital["investment"] > 0):
                
                # ⚠️ VALIDATION RISK MANAGER (prioritaire)
                can_trade, risk_reason = self.risk_manager.can_trade()
                if not can_trade:
                    decision = "HOLD"
                    justifications.append(f"❌ BLOQUÉ PAR RISK MANAGER: {risk_reason}")
                    _log(f"TRADE_BLOCKED_RISK: {risk_reason}")
                    self.logger.warning("Trade bloqué par Risk Manager", reason=risk_reason, capital=capital["investment"])
                    print(f"⚠️ Trade bloqué: {risk_reason}")
                elif trading_signals.get("confidence", 0) > 0.5:
                    # Double validation apprentissage
                    should_trade, reason = self.learning_engine.should_trade(
                        best_choice["asset"],
                        market
                    )
                    
                    if should_trade:
                        decision = "OPEN_LONG"
                        asset = best_choice["asset"]
                        
                        # Prix réels de l'exchange
                        try:
                            symbol = f"{asset}/USDT"
                            market_data = self.exchange.get_market_data(symbol)
                            entry_price = market_data['price']
                            
                            # 🎯 RISK MANAGER: Calcul position size optimale avec Kelly Criterion
                            confidence = (trading_signals.get("confidence", 0.5) + best_choice.get("confidence", 0.5)) / 2
                            
                            # Calculer stop-loss basé sur volatilité
                            volatility = abs(market.get(asset, 0)) / 100  # Approximation volatilité
                            stop_loss_pct = max(0.03, min(0.05, volatility * 2))  # 3-5% stop-loss dynamique
                            stop_loss_price = entry_price * (1 - stop_loss_pct)
                            
                            risk_metrics = self.risk_manager.calculate_position_size(
                                current_capital=capital["investment"],
                                entry_price=entry_price,
                                stop_loss_price=stop_loss_price,
                                confidence=confidence
                            )
                            
                            # Utiliser la position calculée par Risk Manager
                            amount = risk_metrics.max_position_size
                            stop_loss_price = risk_metrics.stop_loss_price
                            take_profit_price = risk_metrics.take_profit_price
                            
                            self.logger.info(
                                f"Position calculée par Risk Manager",
                                asset=asset,
                                amount=amount,
                                stop_loss=stop_loss_price,
                                take_profit=take_profit_price,
                                kelly_pct=risk_metrics.kelly_percentage,
                                risk_reward=risk_metrics.risk_reward_ratio
                            )
                        
                            # Simulation de sortie (testnet = pas de trade réel)
                            # Vérifier si stop-loss ou take-profit touché
                            market_move = market.get(asset, 0)
                            simulated_price = entry_price * (1 + market_move / 100)
                            
                            if simulated_price <= stop_loss_price:
                                exit_price = stop_loss_price
                                _log(f"STOP_LOSS_HIT: {asset} @ {stop_loss_price:.2f}")
                            elif simulated_price >= take_profit_price:
                                exit_price = take_profit_price
                                _log(f"TAKE_PROFIT_HIT: {asset} @ {take_profit_price:.2f}")
                            else:
                                # Sortie normale
                                exit_move = random.uniform(market_move - 1, market_move + 2)
                                exit_price = round(entry_price * (1 + exit_move / 100), 2)
                        
                                # Calcul quantité réaliste
                            quantity = amount / entry_price
                            pnl = round((exit_price - entry_price) * quantity, 2)
                            
                            # 📊 UPDATE RISK MANAGER avec résultat trade
                            self.risk_manager.update_after_trade(
                                pnl=pnl,
                                was_win=(pnl > 0),
                                trade_info={
                                    "asset": asset,
                                    "entry": entry_price,
                                    "exit": exit_price,
                                    "confidence": confidence
                                }
                            )
                            
                            # 📝 Logger l'exécution du trade
                            self.logger.log_trade_execution(
                                asset=asset,
                                action="BUY",
                                entry_price=entry_price,
                                quantity=quantity,
                                strategy=strategy_name,
                                confidence=confidence,
                                stop_loss=stop_loss_price,
                                take_profit=take_profit_price
                            )
                            
                            _log(f"PRICE_REAL: {asset} entrée={entry_price:.2f} sortie={exit_price:.2f} qty={quantity:.6f}")
                        except Exception as e:
                            _log(f"WARNING: Prix réel échoué, fallback simulation: {e}")
                            self.logger.error("Erreur fetch prix exchange, fallback simulation", error=str(e), asset=asset)
                            
                            # Fallback: position size basique
                            position_size = 0.1  # 10% conservateur
                            amount = round(capital["investment"] * position_size, 2)
                            
                            entry_price = round(1000 * (1 + random.uniform(-0.01, 0.01)), 2)
                            market_move = market.get(asset, 0)
                            exit_move = random.uniform(market_move - 1, market_move + 2)
                            exit_price = round(entry_price * (1 + exit_move / 100), 2)
                            quantity = amount / entry_price
                            pnl = round((exit_price - entry_price) * quantity, 2)
                            
                            stop_loss_price = entry_price * 0.97
                            take_profit_price = entry_price * 1.06
                    
                    # Mise à jour capital
                            capital["investment"] = round(capital["investment"] + pnl, 2)
                            withdrawn = 0.0
                            if pnl > 0:
                                withdrawn = round(pnl * 0.2, 2)
                                capital["investment"] = round(capital["investment"] - withdrawn, 2)
                                capital["principal"] = round(capital["principal"] + withdrawn, 2)
                            
                            # Logger clôture trade
                            self.logger.log_trade_close(
                                asset=asset,
                                exit_price=exit_price,
                                pnl=pnl,
                                pnl_pct=(pnl / amount * 100) if amount > 0 else 0,
                                duration_seconds=random.randint(3600, 14400)  # Simulated
                            )
                            
                            trade = {
                                "asset": asset,
                                "entry_price": entry_price,
                                "exit_price": exit_price,
                                "amount": amount,
                                "pnl": pnl,
                                "withdrawn_to_principal": withdrawn,
                                "strategy_used": strategy_name,
                                "fusion_confidence": current_strategy.get("confidence", 0),
                                "learning_confidence": best_choice.get("confidence", 0),
                                "timestamp": datetime.utcnow().isoformat(),
                                "stop_loss_price": stop_loss_price,
                                "take_profit_price": take_profit_price,
                                "risk_metrics": {
                                    "kelly_pct": risk_metrics.kelly_percentage,
                                    "risk_reward_ratio": risk_metrics.risk_reward_ratio,
                                    "position_size_pct": (amount / capital["investment"] * 100)
                                }
                            }
                            
                            justifications.extend([
                                f"Stratégie fusionnée ({strategy_name}) recommande LONG",
                                f"Confiance fusion: {current_strategy.get('confidence', 0):.1%}",
                                f"Apprentissage valide le signal (confiance: {best_choice.get('confidence', 0):.1%})",
                                f"Mouvement {asset}: {market.get(asset, 0):+.2f}%",
                                f"Risk Manager: Position={amount:.2f}$ (Kelly: {risk_metrics.kelly_percentage:.1%})",
                                f"Stop-Loss: ${stop_loss_price:.2f}, Take-Profit: ${take_profit_price:.2f}"
                            ])
                            
                            _log(f"TRADE_EXECUTED: {trade}")
                            print(f"✅ Trade exécuté: {asset} P&L=${pnl:.2f}")
                        except Exception as e:
                            _log(f"WARNING: Prix réel échoué, fallback simulation: {e}")
                            self.logger.error("Erreur fetch prix exchange, fallback simulation", error=str(e), asset=asset)
                            decision = "HOLD"
                            justifications.append(f"❌ Erreur technique: {str(e)}")
                    else:
                        decision = f"HOLD"
                        justifications.append(f"Signal bloqué par apprentissage: {reason}")
                        _log(f"TRADE_BLOCKED_LEARNING: {reason}")
            
            elif trading_signals.get("action") == "AVOID":
                decision = "HOLD"
                justifications.extend(trading_signals.get("reasons", ["Conditions défavorables"]))
                _log(f"DECISION: AVOID - {justifications[-1]}")
            else:
                decision = "HOLD"
                justifications.append("Aucun signal de trading valide")
                _log("DECISION: HOLD")
            
            # ═══════════════════════════════════════════════════════
            # 7️⃣ ANALYSE POST-TRADE & APPRENTISSAGE
            # ═══════════════════════════════════════════════════════
            summary = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "cycle": self.cycle_count,
                "market": market,
                "market_condition": market_condition.value,
                "top_up": {best_asset[0]: best_asset[1]},
                "top_down": {worst_asset[0]: worst_asset[1]},
                "decision": decision,
                "trade": trade,
                "capital": capital,
                "strategy_used": strategy_name,
                "justifications": justifications
            }
            
            if trade:
                # 🧠 Analyse post-trade complète
                post_analysis = self.learning_engine.perform_post_trade_analysis(trade, market)
                summary["post_trade_analysis"] = post_analysis
                _log(f"POST_TRADE_ANALYSIS: errors={len(post_analysis.get('errors_identified', []))}, avoidable={post_analysis.get('avoidable')}")
                
                # Analyser et ajuster
                learning_adjustments = self.learning_engine.analyze_trade(summary)
                summary["learning_adjustments"] = learning_adjustments
                _log(f"LEARNING_ADJUSTMENTS: {learning_adjustments.get('changes', [])}")
                
                # Afficher les changements
                for change in learning_adjustments.get("changes", []):
                    _log(f"LEARNING_CHANGE: {change}")
                    print(f"  🔧 {change}")
                
                # Mettre à jour les performances de la stratégie
                self.strategy_analyzer.update_strategy_performance(
                    strategy_name,
                    {**trade, "rules_used": []}
                )
                
                # Adapter la stratégie fusionnée selon performance
                recent_trades = [c.get("trade") for c in self.reporting_system.cycle_history[-20:] if c.get("trade")]
                fusion_adaptation = self.strategy_fusion.adapt_to_performance(recent_trades)
                if fusion_adaptation.get("adjusted"):
                    _log(f"FUSION_ADAPTATION: {fusion_adaptation.get('changes', [])}")
                    print(f"🔄 Adaptation fusion: {fusion_adaptation.get('new_mode')}")
            
            # ═══════════════════════════════════════════════════════
            # 8️⃣ AUTO-MODIFICATION DES RÈGLES
            # ═══════════════════════════════════════════════════════
            if self.cycle_count % 5 == 0:  # Tous les 5 cycles
                print("🔍 Analyse des erreurs récurrentes...")
                rule_modifications = self.learning_engine.auto_modify_trading_rules()
                if rule_modifications.get("rules_modified") or rule_modifications.get("parameters_adjusted"):
                    _log(f"RULES_AUTO_MODIFIED: {rule_modifications}")
                    summary["rule_modifications"] = rule_modifications
            
            # ═══════════════════════════════════════════════════════
            # 9️⃣ GÉNÉRATION RAPPORTS
            # ═══════════════════════════════════════════════════════
            
            # Résumé texte
            learning_summary = self.learning_engine.get_summary()
            
            # 📊 Ajouter résumé Risk Manager
            risk_summary = self.risk_manager.get_risk_summary()
            
            # Logger les métriques de performance
            self.logger.log_performance_metrics(
                capital=capital["principal"] + capital["investment"],
                win_rate=learning_summary.get("win_rate", 0),
                total_trades=learning_summary.get("total_trades", 0),
                max_drawdown=risk_summary.get("current_drawdown", 0)
            )
            
            text = []
            text.append(f"Résumé cycle #{self.cycle_count} - {summary['timestamp']}")
            text.append(f"Condition marché: {market_condition.value}")
            text.append(f"Stratégie: {strategy_name}")
            text.append(f"Top hausses: {summary['top_up']}")
            text.append(f"Top baisses: {summary['top_down']}")
            text.append(f"Décision: {decision}")
            if trade:
                text.append(f"Trade: {trade['asset']} P&L=${trade['pnl']:.2f}")
            text.append(f"Capital: Principal=${capital['principal']:.2f} Investment=${capital['investment']:.2f}")
            text.append(f"\n📊 Performance:")
            text.append(f"  Win Rate: {learning_summary['win_rate']:.1%}")
            text.append(f"  Total Trades: {learning_summary['total_trades']}")
            text.append(f"  Niveau Risque: {learning_summary['risk_level']:.2f}")
            text.append(f"\n🛡️ Risk Manager:")
            text.append(f"  Drawdown Actuel: {risk_summary.get('current_drawdown', '0%')}")
            text.append(f"  Max Drawdown Limite: {risk_summary.get('max_drawdown_limit', '20%')}")
            text.append(f"  Trades Consécutifs Perdants: {risk_summary.get('consecutive_losses', 0)}")
            text.append(f"  Emergency Stop: {'🔴 ACTIF' if risk_summary.get('emergency_stop') else '🟢 Inactif'}")
            
            with open(summary_path, "w", encoding="utf-8") as f:
                f.write("\n".join(text))
            
            # Sauvegarder capital
            with open(capital_path, "w", encoding="utf-8") as f:
                json.dump(capital, f, indent=2)
            
            _log(f"SUMMARY_WRITTEN -> {summary_path.name}")
            
            # 📄 Rapport 4h automatique
            try:
                report_path = self.reporting_system.generate_4h_report(
                    cycle_data=summary,
                    learning_summary=learning_summary,
                    strategy_info=current_strategy
                )
                if report_path:
                    _log(f"REPORT_4H_GENERATED -> {report_path}")
                    print(f"📄 Rapport 4h: {report_path}")
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                _log(f"REPORT_4H_ERROR: {e}\\n{error_details}")
                print(f"⚠️ Erreur rapport 4h: {e}")
            
            # 📅 Rapport quotidien si nécessaire
            if self.reporting_system.should_generate_daily_report():
                try:
                    daily_report = self.reporting_system.generate_daily_report()
                    if daily_report:
                        _log(f"REPORT_DAILY_GENERATED -> {daily_report}")
                        print(f"📅 Rapport quotidien: {daily_report}")
                except Exception as e:
                    _log(f"REPORT_DAILY_ERROR: {e}")
            
            _log(f"═══════ FIN CYCLE #{self.cycle_count} ═══════\n")
            
            # Callback GUI
            if self.gui_callback:
                try:
                    self.gui_callback("success", f"Cycle #{self.cycle_count} terminé", data=summary)
                except Exception:
                    pass

            return {"summary": summary, "summary_text": "\n".join(text)}
            
        except Exception as ex:
            _log(f"ERROR_CYCLE: {ex}")
            print(f"❌ Erreur cycle: {ex}")
            if self.gui_callback:
                try:
                    self.gui_callback("error", f"Erreur: {ex}")
                except Exception:
                    pass
            raise

    def _atomic_write_json(self, path: Path, data):
        tmp = path.with_suffix(path.suffix + ".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        tmp.replace(path)

    def generate_cycle_docx(self, summary: dict, target_dir: Path | None = None):
        """
        Write a Word (.docx) report for a single cycle summarizing market, decision, trade, capital and lessons.
        Returns path to the written file.
        """
        try:
            target_dir = Path(target_dir) if target_dir else Path.home() / "Desktop"
            target_dir.mkdir(parents=True, exist_ok=True)
            timestamp = summary.get("timestamp", datetime.utcnow().isoformat())
            safe_ts = timestamp.replace(":", "-")
            filename = f"TestNet_Report_{safe_ts}.docx"
            doc = Document()
            doc.add_heading(f"TestNet Cycle Report — {timestamp}", level=1)
            doc.add_paragraph("Analyse du marché:")
            for k, v in summary.get("market", {}).items():
                doc.add_paragraph(f" - {k}: {v} %")
            doc.add_paragraph(f"Décision: {summary.get('decision')}")
            if summary.get("trade"):
                doc.add_heading("Trade simulé", level=2)
                for kk, vv in summary["trade"].items():
                    doc.add_paragraph(f"{kk}: {vv}")
            doc.add_heading("Capital", level=2)
            doc.add_paragraph(json.dumps(summary.get("capital", {}), indent=2))
            # simple lessons: pnl and suggestion
            pnl = summary.get("trade", {}).get("pnl") if summary.get("trade") else None
            doc.add_heading("Analyse & Leçons", level=2)
            if pnl is not None:
                doc.add_paragraph(f"PNL du cycle: {pnl}")
                if pnl < 0:
                    doc.add_paragraph("Perte constatée — suggestion: réduire la fraction d'investissement ou augmenter seuil d'entrée.")
                else:
                    doc.add_paragraph("Profit constaté — conserver stratégie ou envisager léger réinvestissement.")
            else:
                doc.add_paragraph("Aucun trade ouvert durant ce cycle.")
            path = target_dir / filename
            doc.save(path)
            return path
        except Exception as e:
            # fallback: write plain text summary
            txt = (target_dir or Path.home() / "Desktop") / f"TestNet_Report_{safe_ts}.txt"
            with open(txt, "w", encoding="utf-8") as f:
                f.write("Failed to create docx: " + str(e) + "\n")
            return txt

    def _load_learning_state(self):
        p = self.project_root / "learning_state.json"
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        # defaults
        state = {"min_gain_to_open": 0.5, "consecutive_losses": 0}
        with open(p, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        return state

    def _save_learning_state(self, state: dict):
        p = self.project_root / "learning_state.json"
        tmp = p.with_suffix(p.suffix + ".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        tmp.replace(p)

    def adjust_strategy(self, summary: dict):
        """
        Ajustement de stratégie délégué au moteur d'apprentissage permanent
        (Maintenu pour compatibilité avec l'API existante)
        """
        try:
            # Utiliser le nouveau moteur d'apprentissage
            if hasattr(self, 'learning_engine'):
                adjustments = self.learning_engine.analyze_trade(summary)
                return adjustments.get("new_parameters", {})
            
            # Fallback vers l'ancienne méthode si moteur non disponible
            state = self._load_learning_state()
            trade = summary.get("trade")
            if trade and isinstance(trade.get("pnl"), (int, float)):
                pnl = trade["pnl"]
                if pnl < 0:
                    state["consecutive_losses"] = state.get("consecutive_losses", 0) + 1
                else:
                    state["consecutive_losses"] = 0
            # if 3 losses in a row -> increase entry threshold by 0.2%
            if state.get("consecutive_losses", 0) >= 3:
                state["min_gain_to_open"] = round(state.get("min_gain_to_open", 0.5) + 0.2, 2)
                state["consecutive_losses"] = 0
            # persist
            self._save_learning_state(state)
            return state
        except Exception:
            return {}

def main():
    """Test du scheduler"""
    print("🧪 Test du Scheduler Autonome\n")
    
    def callback(status, message, data=None):
        print(f"[CALLBACK] {status.upper()}: {message}")
    
    scheduler = AutonomousScheduler(interval_hours=2, gui_callback=callback)
    scheduler.start()
    
    # Garder le thread actif pour les tests
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        print("\nArrêt du scheduler...")
        scheduler.stop()


if __name__ == "__main__":
    main()
