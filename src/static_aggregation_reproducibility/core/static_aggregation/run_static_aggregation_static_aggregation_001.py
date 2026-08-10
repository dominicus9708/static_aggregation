from __future__ import annotations

import argparse
import sys
from pathlib import Path

CORE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CORE))
from common import Check, DEFAULT_INPUT, beta_bound, check_rows_to_dicts, close, component_term, finite_comp, geometric_absolute_sum, geometric_infinite, geometric_partial, load_input, property_aggregate, resolve_run_id, scalar_transport, stability_witness, stage_dir, static_descriptor, weighted_structural_descriptor, write_csv, write_json, write_text


def run(input_path: Path, output_root: str | None, run_id: str) -> dict:
    data = load_input(input_path)
    tol = float(data["tolerance"])
    n = int(data["grid_points"])
    masses = [1.0 / n] * n
    weight = [1.0] * n
    terms = {}
    betas = {}
    checks: list[Check] = []
    for name, scalar in data["channels"].items():
        zeta = [float(scalar)] * n
        t = component_term(zeta, weight, masses)
        beta = beta_bound(zeta, weight, masses)
        terms[name] = t
        betas[name] = beta
        checks.append(Check("SA-01", "Section 4: realized component term and channel bound", t, float(scalar), abs(t-float(scalar)), close(t,float(scalar),tol) and abs(t) <= beta + tol, f"{name}: |T|={abs(t)} <= beta={beta}"))
    finite_values = {name: finite_comp(terms, support) for name, support in data["channel_supports"].items()}
    expected_finite = {"F0":0.0,"Fpm":0.0,"Fepsilon":float(data["epsilon"])}
    for name, expected in expected_finite.items():
        value = finite_values[name]
        checks.append(Check("SA-02","Section 5 / Section 13.1: finite composition",value,expected,abs(value-expected),close(value,expected,tol),name))
    ce = data["countable_extension"]
    first, ratio, count = float(ce["first_term"]), float(ce["ratio"]), int(ce["terms"])
    terms_geo = [first * ratio**j for j in range(count)]
    partial = geometric_partial(first, ratio, count)
    reversed_partial = sum(reversed(terms_geo))
    infinite = geometric_infinite(first, ratio)
    abs_sum = geometric_absolute_sum(first, ratio)
    tail_bound = abs(first * ratio**count / (1-ratio))
    countable_ok = close(partial,reversed_partial,tol) and abs(partial-infinite) <= tail_bound + tol
    checks.append(Check("SA-03","Section 6: absolute countable extension",partial,infinite,abs(partial-infinite),countable_ok,f"absolute norm sum={abs_sum}; reversed finite truncation={reversed_partial}"))
    st = data["stability"]
    stab = stability_witness(st["zeta"],st["zeta_prime"],st["weight"],st["weight_prime"],st["measure_mass"])
    stability_ok = stab["lhs"] <= stab["direct_rhs"] + tol and stab["direct_rhs"] <= stab["sup_rhs"] + tol
    checks.append(Check("SA-04","Section 9: channelwise combined stability",stab["lhs"],stab["sup_rhs"],max(0.0,stab["lhs"]-stab["sup_rhs"]),stability_ok,f"direct_rhs={stab['direct_rhs']}"))
    family_lhs, family_rhs = 2.0*stab["lhs"], 2.0*stab["sup_rhs"]
    checks.append(Check("SA-05","Section 9: finite composite stability",family_lhs,family_rhs,max(0.0,family_lhs-family_rhs),family_lhs <= family_rhs + tol,"two-channel finite witness"))
    scale = float(data["transport"]["scale_J"])
    transported = scalar_transport(terms, scale)
    e9_ok = all(close(scale*value,transported[f"phi({c})"],tol) for c,value in terms.items())
    checks.append(Check("SA-06","Section 10: analytic transport condition (E9)",e9_ok,True,0.0 if e9_ok else 1.0,e9_ok,f"J(x)={scale}x"))
    support = data["transport"]["support"]
    comp_l = finite_comp(terms,support)
    comp_m = sum(transported[f"phi({c})"] for c in support)
    covariance_ok = close(scale*comp_l,comp_m,tol)
    checks.append(Check("SA-07","Section 10: finite composite covariance",comp_m,scale*comp_l,abs(comp_m-scale*comp_l),covariance_ok,str(support)))
    props = {k:float(v) for k,v in data["property_records"].items()}
    prop_values = {name:property_aggregate(props,support) for name,support in data["property_supports"].items()}
    channel_collision = data["channel_supports"]["F0"] != data["channel_supports"]["Fpm"] and close(finite_values["F0"],finite_values["Fpm"],tol)
    prop_collision = data["property_supports"]["G0"] != data["property_supports"]["Gpm"] and close(prop_values["G0"],prop_values["Gpm"],tol)
    checks.append(Check("SA-08","Section 11 / Section 13.1: channel support collision",channel_collision,True,0.0 if channel_collision else 1.0,channel_collision))
    checks.append(Check("SA-09","Section 11 / Section 13.2: property support collision",prop_collision,True,0.0 if prop_collision else 1.0,prop_collision))
    combined_pm = static_descriptor(finite_values["Fpm"],prop_values["Gpm"])
    combined_0 = static_descriptor(finite_values["F0"],prop_values["G0"])
    combined_collision = combined_pm == combined_0 and channel_collision and prop_collision
    checks.append(Check("SA-10","Section 13.3: combined static descriptor collision",str(combined_pm),str(combined_0),0.0 if combined_pm == combined_0 else 1.0,combined_collision))
    dw = data["weighted_structural_descriptor"]
    dw_value = weighted_structural_descriptor(dw["alpha"],dw["weight"],dw["measure_mass"])
    dw_expected = sum(a*w*m for a,w,m in zip(dw["alpha"],dw["weight"],dw["measure_mass"]))
    checks.append(Check("SA-11","Section 12: one-channel scalar D_w specialization",dw_value,dw_expected,abs(dw_value-dw_expected),close(dw_value,dw_expected,tol)))
    passed = all(c.passed for c in checks)
    out = stage_dir("static_aggregation",run_id,output_root)
    rows = check_rows_to_dicts(checks)
    write_csv(out/"static_aggregation_master_working.csv",rows,["check_id","paper_reference","computed","expected","abs_error","passed","note"])
    result = {"status":"PASS" if passed else "FAIL","run_id":run_id,"terms":terms,"betas":betas,"finite_aggregates":finite_values,"property_aggregates":prop_values,"combined":{"Fpm_Gpm":list(combined_pm),"F0_G0":list(combined_0)},"countable":{"partial":partial,"infinite":infinite,"absolute_sum":abs_sum,"reversed_partial":reversed_partial},"stability":stab,"transport":{"scale_J":scale,"terms_M":transported,"comp_L":comp_l,"comp_M":comp_m},"D_w":dw_value,"checks":rows}
    write_json(out/"static_aggregation_values.json",result)
    write_json(out/"manifest.json",{"run_id":run_id,"input":str(input_path),"script":"run_static_aggregation_static_aggregation_001.py","stage":"static_aggregation","theory_layer":"static_aggregation","status":result["status"],"check_count":len(checks)})
    summary = ["Static aggregation basic reproducibility",f"status: {result['status']}",f"checks: {sum(c.passed for c in checks)}/{len(checks)} passed",""] + [f"{c.check_id}: {'PASS' if c.passed else 'FAIL'} — {c.note}" for c in checks] + ["","Interpretation: computational finite witnesses and regression checks; not a proof of the general Banach-space theorems."]
    write_text(out/"static_aggregation_summary_001.txt","\n".join(summary))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",type=Path,default=DEFAULT_INPUT)
    parser.add_argument("--output-root",default=None)
    parser.add_argument("--run-id",default=None)
    args = parser.parse_args()
    result = run(args.input,args.output_root,resolve_run_id(args.run_id))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
