import json
from pathlib import Path
from autonomous_scheduler import AutonomousScheduler

def test_run_one_shot_creates_files(tmp_path: Path):
    sched = AutonomousScheduler(interval_hours=1, project_root=tmp_path)
    result = sched.run_one_shot(simulate=True)
    # Files exist
    assert (tmp_path / "sp_agent.log").exists()
    assert (tmp_path / "last_cycle_summary.txt").exists()
    assert (tmp_path / "capital_state.json").exists()
    # Structure of summary
    assert isinstance(result, dict)
    summary = result.get("summary")
    assert "market" in summary
    assert "capital" in summary
    # Capital JSON parseable
    with open(tmp_path / "capital_state.json", "r", encoding="utf-8") as f:
        state = json.load(f)
    assert "principal" in state and "investment" in state