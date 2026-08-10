from __future__ import annotations

import argparse
import sys
from pathlib import Path

CORE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CORE))
from common import DEFAULT_INPUT, finite_comp, load_input, property_aggregate, resolve_run_id, stage_dir, static_descriptor, write_csv, write_json, write_text


def run(input_path: Path, output_root: str | None, run_id: str) -> dict:
    data = load_input(input_path)
    channels = {k: float(v) for k, v in data["channels"].items()}
    props = {k: float(v) for k, v in data["property_records"].items()}
    channel_aggregates = {name: finite_comp(channels, support) for name, support in data["channel_supports"].items()}
    property_aggregates = {name: property_aggregate(props, support) for name, support in data["property_supports"].items()}
    combined = {"Fpm_Gpm": static_descriptor(channel_aggregates["Fpm"], property_aggregates["Gpm"]), "F0_G0": static_descriptor(channel_aggregates["F0"], property_aggregates["G0"])}
    result = {"status":"PASS","run_id":run_id,"channels":channels,"channel_aggregates":channel_aggregates,"property_aggregates":property_aggregates,"combined":{k:list(v) for k,v in combined.items()}}
    out = stage_dir("standard", run_id, output_root)
    rows = []
    for key, value in channels.items(): rows.append({"category":"channel_term_baseline","item":key,"value":value})
    for key, value in channel_aggregates.items(): rows.append({"category":"finite_channel_aggregate","item":key,"value":value})
    for key, value in property_aggregates.items(): rows.append({"category":"finite_property_aggregate","item":key,"value":value})
    write_csv(out / "standard_master_working.csv", rows, ["category","item","value"])
    write_json(out / "standard_values.json", result)
    write_json(out / "manifest.json", {"run_id":run_id,"input":str(input_path),"script":"run_static_aggregation_standard_001.py","stage":"standard","baseline_type":"direct algebraic manuscript witness","status":"PASS"})
    write_text(out / "standard_summary_001.txt", "\n".join(["Static aggregation algebraic baseline","status: PASS",f"Comp(F0)={channel_aggregates['F0']}",f"Comp(Fpm)={channel_aggregates['Fpm']}",f"Comp(Fepsilon)={channel_aggregates['Fepsilon']}",f"Agg(Gpm)={property_aggregates['Gpm']}",f"Agg(G0)={property_aggregates['G0']}","No external physical baseline is used in this basic release."]))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-root", default=None)
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    run(args.input, args.output_root, resolve_run_id(args.run_id))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
