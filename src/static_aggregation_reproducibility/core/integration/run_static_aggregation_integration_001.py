from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

CORE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CORE))
from common import DEFAULT_INPUT, close, resolve_run_id, resolve_output_root, stage_dir, write_csv, write_json, write_text


def run_stage(script: Path, input_path: Path, output_root: Path, run_id: str) -> None:
    subprocess.run([sys.executable,str(script),"--input",str(input_path),"--output-root",str(output_root),"--run-id",run_id],check=True)


def run(input_path: Path, output_root_arg: str | None, run_id: str) -> dict:
    output_root = resolve_output_root(output_root_arg)
    for script in [CORE/"skeleton"/"run_static_aggregation_skeleton_001.py",CORE/"standard"/"run_static_aggregation_standard_001.py",CORE/"static_aggregation"/"run_static_aggregation_static_aggregation_001.py"]:
        run_stage(script,input_path,output_root,run_id)
    standard_path = output_root/"standard"/run_id/"standard_values.json"
    theory_path = output_root/"static_aggregation"/run_id/"static_aggregation_values.json"
    standard = json.loads(standard_path.read_text(encoding="utf-8"))
    theory = json.loads(theory_path.read_text(encoding="utf-8"))
    data = json.loads(input_path.read_text(encoding="utf-8"))
    tol = float(data["tolerance"])
    comparisons = []
    for channel, baseline in standard["channels"].items():
        computed = theory["terms"][channel]
        comparisons.append({"category":"channel_term","item":channel,"standard":baseline,"static_aggregation":computed,"abs_error":abs(computed-baseline),"passed":close(computed,baseline,tol)})
    for support, baseline in standard["channel_aggregates"].items():
        computed = theory["finite_aggregates"][support]
        comparisons.append({"category":"finite_channel_aggregate","item":support,"standard":baseline,"static_aggregation":computed,"abs_error":abs(computed-baseline),"passed":close(computed,baseline,tol)})
    for support, baseline in standard["property_aggregates"].items():
        computed = theory["property_aggregates"][support]
        comparisons.append({"category":"finite_property_aggregate","item":support,"standard":baseline,"static_aggregation":computed,"abs_error":abs(computed-baseline),"passed":close(computed,baseline,tol)})
    passed = theory["status"] == "PASS" and all(row["passed"] for row in comparisons)
    out = stage_dir("integration",run_id,output_root)
    write_csv(out/"integration_master_comparison.csv",comparisons,["category","item","standard","static_aggregation","abs_error","passed"])
    result = {"status":"PASS" if passed else "FAIL","run_id":run_id,"input":str(input_path),"standard_values":str(standard_path),"static_aggregation_values":str(theory_path),"comparisons":comparisons,"theory_check_count":len(theory["checks"]),"theory_checks_passed":sum(1 for c in theory["checks"] if c["passed"])}
    write_json(out/"integration_values.json",result)
    write_json(out/"manifest.json",{"run_id":run_id,"input":str(input_path),"script":"run_static_aggregation_integration_001.py","stages":["skeleton","standard","static_aggregation","integration"],"theory_layer":"static_aggregation","status":result["status"],"output_root":str(output_root)})
    write_text(out/"integration_summary_001.txt","\n".join(["Static aggregation integration summary",f"status: {result['status']}",f"baseline comparisons: {sum(1 for r in comparisons if r['passed'])}/{len(comparisons)} passed",f"analytic checks: {result['theory_checks_passed']}/{result['theory_check_count']} passed","scope: formal/basic reproducibility only; no application dataset included."]))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the complete basic static-aggregation reproducibility pipeline.")
    parser.add_argument("--input",type=Path,default=DEFAULT_INPUT)
    parser.add_argument("--output-root",default=None)
    parser.add_argument("--run-id",default=None)
    args = parser.parse_args()
    result = run(args.input,args.output_root,resolve_run_id(args.run_id))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
