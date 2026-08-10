from __future__ import annotations

import argparse
import sys
from pathlib import Path

CORE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CORE))
from common import load_input, resolve_run_id, stage_dir, write_json, write_text

REQUIRED_KEYS = {"epsilon","delta","channels","channel_supports","property_records","property_supports","countable_extension","stability","transport","weighted_structural_descriptor","tolerance"}


def run(input_path: Path, output_root: str | None, run_id: str) -> dict:
    data = load_input(input_path)
    missing = sorted(REQUIRED_KEYS - set(data))
    epsilon_ok = 0.0 < float(data["epsilon"]) < float(data["delta"])
    status = not missing and epsilon_ok
    out = stage_dir("skeleton", run_id, output_root)
    result = {"status":"PASS" if status else "FAIL","input":str(input_path),"missing_keys":missing,"epsilon_negligible_witness":epsilon_ok,"run_id":run_id,"theory_layer":"static_aggregation"}
    write_json(out / "manifest.json", result)
    write_text(out / "skeleton_summary_001.txt", "\n".join(["Static aggregation reproducibility skeleton",f"status: {result['status']}",f"input: {input_path}",f"missing_keys: {missing}",f"0 < epsilon < delta: {epsilon_ok}"]))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=None)
    parser.add_argument("--output-root", default=None)
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    from common import DEFAULT_INPUT
    result = run(args.input or DEFAULT_INPUT, args.output_root, resolve_run_id(args.run_id))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
