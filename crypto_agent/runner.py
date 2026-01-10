"""
Runner to perform one cycle (analysis + optional simulated trade) and optionally schedule hourly runs.
"""
import argparse
import time
from pathlib import Path
from .binance_client import BinanceTestnetClient
from .analyzer import build_market_summary
from .capital import CapitalManager
from .engine import TradingEngine
from .report import generate_docx_report
from . import config


def run_cycle(simulate: bool = True, do_report: bool = True, principal: float = None) -> dict:
    client = BinanceTestnetClient()
    tickers = client.fetch_24h_tickers()
    market_summary = build_market_summary(tickers, top_n=10)

    capital = CapitalManager(principal if principal is not None else config.DEFAULT_PRINCIPAL_USDT)
    engine = TradingEngine(client, capital, simulate=simulate)

    # Decide and execute/simulate
    decision = engine.evaluate_and_trade(market_summary)
    trades = []
    if decision and decision.get('position'):
        pos = decision['position']
        # If simulated, we may immediately simulate TP hit for demonstration
        if simulate:
            closed = engine.simulate_close_for_take_profit(pos)
            trades.append(closed)
        else:
            # For real Testnet, we place market buy and OCO; trades will be realized later when OCO fires
            trades.append(pos)

    # Build capital snapshot
    cap_snap = capital.snapshot().__dict__

    # Generate report
    report_path = None
    if do_report:
        ts = int(time.time())
        fname = config.REPORT_DESKTOP_DIR / f"SP_Testnet_Report_{ts}.docx"
        generate_docx_report(fname, market_summary, decision, trades, cap_snap)
        report_path = str(fname)

    return {
        'market_summary': market_summary,
        'decision': decision,
        'trades': trades,
        'capital': cap_snap,
        'report': report_path
    }


def start_loop(days: int = 5, interval_sec: int = 3600, simulate: bool = True, principal: float = None):
    """Run cycles hourly for given number of days. If simulate=False, operates in Testnet mode (places orders).

    This function now maintains persistent capital state and open positions in the logs directory,
    and adds robust logging and error handling so the loop continues on exceptions.
    """
    import logging
    log_path = config.LOG_DIR / 'sp_agent.log'
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[
        logging.FileHandler(str(log_path)),
        logging.StreamHandler()
    ])
    logger = logging.getLogger('sp_agent')

    # Load or initialize capital state
    state_path = config.LOG_DIR / 'capital_state.json'
    capital = None
    cm_loaded = CapitalManager.load_state(state_path)
    if cm_loaded:
        capital = cm_loaded
        logger.info("Loaded capital state from disk")
    else:
        capital = CapitalManager(principal if principal is not None else config.DEFAULT_PRINCIPAL_USDT)
        logger.info("Initialized new capital manager")

    # Create client and engine
    client = BinanceTestnetClient()
    from .trader import BinanceTestnetTrader
    trader = BinanceTestnetTrader(api_key=config.BINANCE_API_KEY, api_secret=config.BINANCE_API_SECRET) if not simulate else None
    engine = TradingEngine(client, capital, simulate=simulate, trader=trader)

    # Setup positions persistence
    positions_path = config.LOG_DIR / 'open_positions.json'
    engine.set_positions_path(positions_path)
    engine.load_open_positions(positions_path)

    total_cycles = max(1, int(days * 24))
    logger.info(f"Starting loop: days={days}, cycles={total_cycles}, simulate={simulate}")

    for i in range(total_cycles):
        logger.info(f"=== Cycle {i+1}/{total_cycles} ===")
        try:
            tickers = client.fetch_24h_tickers()
            market_summary = build_market_summary(tickers, top_n=10)
            logger.info("Market analysis complete: %d symbols", market_summary.get('universe_size'))

            decision = engine.evaluate_and_trade(market_summary)
            trades = []
            if decision and decision.get('position'):
                pos = decision['position']
                trades.append(pos)
                # Persist positions
                try:
                    engine.save_open_positions(positions_path)
                except Exception:
                    pass

            # Poll for fills and update capital
            try:
                closed_positions = engine.poll_and_update_positions(positions_path)
                if closed_positions:
                    logger.info(f"Closed positions detected: {len(closed_positions)}")
                    for cpos in closed_positions:
                        logger.info(f"Closed: {cpos.get('symbol')} pnl={cpos.get('pnl')}")
            except Exception as e:
                logger.exception("Error while polling positions: %s", e)

            # Save capital state
            try:
                capital.save_state(state_path)
                logger.info("Saved capital state")
            except Exception as e:
                logger.exception("Error saving capital state: %s", e)

            # Generate report
            try:
                ts = int(time.time())
                fname = config.REPORT_DESKTOP_DIR / f"SP_Testnet_Report_{ts}.docx"
                generate_docx_report(fname, market_summary, decision, trades, capital.snapshot().__dict__)
                logger.info("Report generated: %s", str(fname))

                # Write a concise textual summary for quick notification / inspection
                try:
                    summary_lines = []
                    summary_lines.append(f"Cycle: {i+1}/{total_cycles}")
                    summary_lines.append(f"Timestamp: {ts} (UTC)")
                    # Top gainers / losers
                    top_gainers = market_summary.get('top_gainers', [])[:5]
                    top_losers = market_summary.get('top_losers', [])[:5]
                    summary_lines.append("Top Gainers:")
                    for g in top_gainers:
                        summary_lines.append(f"  - {g['symbol']}: {g['change_pct']}% vol={g['volume']}")
                    summary_lines.append("Top Losers:")
                    for l in top_losers:
                        summary_lines.append(f"  - {l['symbol']}: {l['change_pct']}% vol={l['volume']}")

                    # Decision / Trades
                    if decision:
                        summary_lines.append(f"Decision: {decision.get('action')}")
                        cand = decision.get('candidate')
                        if cand:
                            summary_lines.append(f"Candidate: {cand.get('symbol')} (change {cand.get('change_pct')}%)")
                    else:
                        summary_lines.append("Decision: none")

                    if trades:
                        summary_lines.append("Trades executed/simulated:")
                        for t in trades:
                            summary_lines.append(f"  - {t.get('symbol')} entry={t.get('entry_price')} qty={t.get('quantity')} status={t.get('status')} pnl={t.get('pnl',0):.2f}")
                    else:
                        summary_lines.append("Trades executed/simulated: none")

                    # Capital
                    cap = capital.snapshot().__dict__
                    summary_lines.append(f"Capital - Principal: {cap.get('principal'):.2f} USDT | Investment balance: {cap.get('investment_balance'):.2f} USDT | Cumulative profits: {cap.get('cumulative_profits'):.2f} USDT")

                    summary_lines.append(f"Report file: {str(fname)}")

                    # Write to disk
                    last_summary = config.LOG_DIR / 'last_cycle_summary.txt'
                    last_report_ref = config.LOG_DIR / 'last_report_path.txt'
                    with open(last_summary, 'w', encoding='utf-8') as fsum:
                        fsum.write('\n'.join(summary_lines))
                    with open(last_report_ref, 'w', encoding='utf-8') as fred:
                        fred.write(str(fname))

                    logger.info("Summary written: %s", str(last_summary))

                    # Attempt to send the summary by email if SMTP is configured
                    try:
                        from .notifier import send_summary_email
                        if config.SMTP_HOST and config.SMTP_USER and config.SMTP_PASS:
                            send_summary_email(last_summary, report_path=fname, recipient=config.EMAIL_RECIPIENT)
                            logger.info("Summary emailed to %s", config.EMAIL_RECIPIENT)
                        else:
                            logger.info("SMTP not configured; skipping email.")
                    except Exception as e:
                        logger.exception("Error sending summary email: %s", e)
                except Exception as e:
                    logger.exception("Error writing summary: %s", e)
            except Exception as e:
                logger.exception("Error generating report: %s", e)

        except Exception as e:
            logger.exception("Error in cycle %d: %s", i+1, e)

        if i < total_cycles - 1:
            logger.info("Sleeping for %d seconds", interval_sec)
            time.sleep(interval_sec)

    logger.info("Loop finished.")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SP Testnet Runner')
    parser.add_argument('--simulate', action='store_true', default=True, help='Run in simulation mode (no testnet orders)')
    parser.add_argument('--once', action='store_true', default=True, help='Run one cycle and exit')
    parser.add_argument('--principal', type=float, default=None, help='Override default principal amount')
    args = parser.parse_args()

    result = run_cycle(simulate=args.simulate, do_report=True, principal=args.principal)
    print("Cycle complete. Report:", result.get('report'))
    if args.once:
        print("Exiting (one-shot mode).")
