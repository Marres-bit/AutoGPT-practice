from pathlib import Path
import argparse
import time
from datetime import datetime, timedelta

from autonomous_scheduler import AutonomousScheduler

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration-hours", type=int, default=48, help="Total run duration in hours")
    parser.add_argument("--interval-hours", type=int, default=4, help="Interval between cycles")
    parser.add_argument("--report-dir", type=str, default=None, help="Where to save reports (default: Desktop)")
    args = parser.parse_args()

    project_root = Path(__file__).parent
    scheduler = AutonomousScheduler(interval_hours=args.interval_hours, project_root=project_root)
    end_time = datetime.utcnow() + timedelta(hours=args.duration_hours)
    print(f"📅 Run until: {end_time.isoformat()} (UTC)")

    while datetime.utcnow() < end_time:
        print(f"\n🔬 Running one-shot at {datetime.utcnow().isoformat()}...")
        res = scheduler.run_one_shot(simulate=True)
        summary = res.get("summary") if isinstance(res, dict) else {}
        # generate .docx report
        try:
            dest = Path(args.report_dir) if args.report_dir else None
            report_path = scheduler.generate_cycle_docx(summary, target_dir=dest)
            print(f"✅ Report written: {report_path}")
        except Exception as e:
            print(f"❌ Failed to write report: {e}")
        # learning adjust
        try:
            new_state = scheduler.adjust_strategy(summary)
            print(f"🔧 Learned state: {new_state}")
        except Exception:
            pass
        # sleep until next scheduled cycle
        print(f"⏳ Sleeping for {args.interval_hours} hours...")
        time.sleep(args.interval_hours * 3600)

    print("✅ Run duration completed. Exiting.")

if __name__ == "__main__":
    main()