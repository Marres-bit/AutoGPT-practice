"""
Dashboard Streamlit - Interface de visualisation en temps réel
Lance avec: streamlit run dashboard.py
"""

import streamlit as st
from pathlib import Path
import json
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


class TradingDashboard:
    """Dashboard interactif pour monitoring de l'agent"""
    
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.capital_file = self.project_root / "capital_state.json"
        self.learning_file = self.project_root / "learning_state.json"
        self.risk_file = self.project_root / "risk_state.json"
        self.cycle_history_file = self.project_root / "cycle_history.json"
        
    def load_data(self):
        """Charge toutes les données"""
        data = {}
        
        # Capital
        if self.capital_file.exists():
            with open(self.capital_file, 'r') as f:
                data['capital'] = json.load(f)
        
        # Learning
        if self.learning_file.exists():
            with open(self.learning_file, 'r') as f:
                data['learning'] = json.load(f)
        
        # Risk
        if self.risk_file.exists():
            with open(self.risk_file, 'r') as f:
                data['risk'] = json.load(f)
        
        # Historique cycles
        if self.cycle_history_file.exists():
            with open(self.cycle_history_file, 'r') as f:
                data['cycles'] = json.load(f)
        
        return data
    
    def render_metrics(self, data):
        """Affiche métriques principales"""
        st.header("📊 Métriques de Performance")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Capital
        capital_data = data.get('capital', {})
        total_capital = capital_data.get('principal', 0) + capital_data.get('investment', 0)
        
        with col1:
            st.metric(
                "Capital Total",
                f"${total_capital:,.2f}",
                delta=f"+${capital_data.get('investment', 0):,.2f}"
            )
        
        # Win Rate
        learning_data = data.get('learning', {})
        win_rate = learning_data.get('win_rate', 0)
        
        with col2:
            st.metric(
                "Win Rate",
                f"{win_rate:.1%}",
                delta=f"{win_rate - 0.5:.1%}" if win_rate > 0.5 else f"{win_rate - 0.5:.1%}"
            )
        
        # Total Trades
        total_trades = learning_data.get('total_trades', 0)
        
        with col3:
            st.metric(
                "Total Trades",
                total_trades
            )
        
        # Drawdown
        risk_data = data.get('risk', {})
        current_dd = risk_data.get('current_drawdown', 0) if risk_data else 0
        
        with col4:
            st.metric(
                "Drawdown Actuel",
                f"{current_dd:.1%}",
                delta=f"{current_dd:.1%}",
                delta_color="inverse"
            )
    
    def render_equity_curve(self, data):
        """Affiche courbe d'equity"""
        st.header("📈 Equity Curve")
        
        cycles = data.get('cycles', [])
        
        if not cycles:
            st.info("Pas encore de données de cycles")
            return
        
        # Construire DataFrame
        df_data = []
        cumulative_pnl = 10000  # Capital initial
        
        for cycle in cycles:
            timestamp = cycle.get('timestamp', '')
            pnl = cycle.get('pnl', 0)
            cumulative_pnl += pnl
            
            df_data.append({
                'timestamp': pd.to_datetime(timestamp),
                'capital': cumulative_pnl,
                'pnl': pnl
            })
        
        df = pd.DataFrame(df_data)
        
        # Plotly chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['capital'],
            mode='lines+markers',
            name='Capital',
            line=dict(color='#00cc96', width=2),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title='Évolution du Capital',
            xaxis_title='Date',
            yaxis_title='Capital ($)',
            hovermode='x unified',
            template='plotly_dark'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_performance_breakdown(self, data):
        """Affiche breakdown des performances"""
        st.header("🎯 Performance par Asset")
        
        learning_data = data.get('learning', {})
        asset_stats = learning_data.get('asset_statistics', {})
        
        if not asset_stats:
            st.info("Pas encore de statistiques par asset")
            return
        
        # Créer DataFrame
        df_assets = []
        for asset, stats in asset_stats.items():
            df_assets.append({
                'Asset': asset,
                'Trades': stats.get('total_trades', 0),
                'Wins': stats.get('winning_trades', 0),
                'Losses': stats.get('losing_trades', 0),
                'Win Rate': stats.get('win_rate', 0),
                'Avg PnL': stats.get('avg_pnl', 0)
            })
        
        df = pd.DataFrame(df_assets)
        
        # Bar chart win rate
        fig = px.bar(
            df,
            x='Asset',
            y='Win Rate',
            title='Win Rate par Asset',
            color='Win Rate',
            color_continuous_scale='RdYlGn'
        )
        
        fig.update_layout(template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
        
        # Tableau détaillé
        st.dataframe(
            df.style.format({
                'Win Rate': '{:.1%}',
                'Avg PnL': '${:.2f}'
            }).background_gradient(subset=['Win Rate'], cmap='RdYlGn'),
            use_container_width=True
        )
    
    def render_risk_analysis(self, data):
        """Affiche analyse des risques"""
        st.header("🛡️ Analyse des Risques")
        
        risk_data = data.get('risk', {})
        
        if not risk_data:
            st.info("Pas de données de risque")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Drawdown gauge
            current_dd = risk_data.get('current_drawdown', 0)
            max_dd = risk_data.get('max_drawdown_limit', 0.20)
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=current_dd * 100,
                title={'text': "Drawdown (%)"},
                gauge={
                    'axis': {'range': [0, max_dd * 100]},
                    'bar': {'color': "red" if current_dd > max_dd * 0.7 else "orange" if current_dd > max_dd * 0.5 else "green"},
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': max_dd * 100
                    }
                }
            ))
            
            fig.update_layout(height=300, template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Risk metrics
            st.subheader("Métriques de Risque")
            
            st.metric("Niveau de Risque", risk_data.get('risk_level', 'N/A'))
            st.metric("Risque par Trade", f"{risk_data.get('risk_per_trade', 0):.1%}")
            st.metric("Pertes Consécutives", risk_data.get('consecutive_losses', 0))
            
            emergency = risk_data.get('emergency_stop_active', False)
            if emergency:
                st.error("🚨 ARRÊT D'URGENCE ACTIF")
            else:
                st.success("✅ Système opérationnel")
    
    def render_recent_trades(self, data):
        """Affiche trades récents"""
        st.header("🔄 Trades Récents")
        
        cycles = data.get('cycles', [])
        
        if not cycles:
            st.info("Pas encore de trades")
            return
        
        # Derniers 10 cycles
        recent = cycles[-10:] if len(cycles) > 10 else cycles
        recent.reverse()
        
        for cycle in recent:
            decision = cycle.get('decision', 'HOLD')
            asset = cycle.get('asset', 'N/A')
            pnl = cycle.get('pnl', 0)
            timestamp = cycle.get('timestamp', '')
            
            col1, col2, col3, col4 = st.columns([2, 2, 2, 3])
            
            with col1:
                st.text(timestamp[:16] if timestamp else 'N/A')
            
            with col2:
                if decision == "TRADE":
                    st.success(f"✅ TRADE {asset}")
                else:
                    st.info("⏸️ HOLD")
            
            with col3:
                if pnl > 0:
                    st.success(f"+${pnl:.2f}")
                elif pnl < 0:
                    st.error(f"${pnl:.2f}")
                else:
                    st.text("$0.00")
            
            with col4:
                reason = cycle.get('reason', '')
                st.caption(reason[:50] + '...' if len(reason) > 50 else reason)
            
            st.divider()
    
    def render_settings(self, data):
        """Affiche paramètres"""
        st.header("⚙️ Paramètres Actuels")
        
        learning_data = data.get('learning', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Learning Engine")
            st.metric("Min Gain to Open", f"{learning_data.get('min_gain_to_open', 0):.2f}%")
            st.metric("Risk Level", f"{learning_data.get('risk_level', 0):.2f}")
            st.metric("Consecutive Losses", learning_data.get('consecutive_losses', 0))
        
        with col2:
            st.subheader("Patterns à Éviter")
            avoid_patterns = learning_data.get('avoid_patterns', [])
            if avoid_patterns:
                for pattern in avoid_patterns:
                    st.warning(f"⚠️ {pattern}")
            else:
                st.success("✅ Aucun pattern à éviter")


def main():
    """Point d'entrée du dashboard"""
    st.set_page_config(
        page_title="Crypto Trading Agent Dashboard",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🤖 Agent AI Crypto - Dashboard en Temps Réel")
    st.caption("Monitoring et analyse de performance")
    
    # Sidebar
    with st.sidebar:
        st.header("Configuration")
        
        project_root = st.text_input(
            "Dossier Projet",
            value="c:\\Users\\sanim\\git-practice\\AutoGPT"
        )
        
        refresh_rate = st.slider("Rafraîchissement (sec)", 5, 60, 10)
        
        if st.button("🔄 Rafraîchir Maintenant", use_container_width=True):
            st.rerun()
        
        st.divider()
        
        st.subheader("Navigation")
        page = st.radio(
            "Page",
            ["📊 Vue d'ensemble", "📈 Performance", "🛡️ Risques", "⚙️ Paramètres"]
        )
    
    # Charger données
    dashboard = TradingDashboard(Path(project_root))
    data = dashboard.load_data()
    
    # Afficher page sélectionnée
    if page == "📊 Vue d'ensemble":
        dashboard.render_metrics(data)
        dashboard.render_equity_curve(data)
        dashboard.render_recent_trades(data)
    
    elif page == "📈 Performance":
        dashboard.render_metrics(data)
        dashboard.render_performance_breakdown(data)
        dashboard.render_equity_curve(data)
    
    elif page == "🛡️ Risques":
        dashboard.render_risk_analysis(data)
        dashboard.render_recent_trades(data)
    
    elif page == "⚙️ Paramètres":
        dashboard.render_settings(data)
    
    # Auto-refresh
    st.caption(f"Dernière mise à jour: {datetime.now().strftime('%H:%M:%S')}")


if __name__ == "__main__":
    main()
