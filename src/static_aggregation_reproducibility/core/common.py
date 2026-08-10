from __future__ import annotations

import csv
import json
import math
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT = REPO_ROOT / "data" / "derived" / "static_aggregation_reproducibility" / "input" / "core" / "finite_witness.json"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "results" / "static_aggregation_reproducibility" / "output"


@dataclass(frozen=True)
class Check:
    check_id: str
    paper_reference: str
    computed: float | str | bool
    expected: float | str | bool
    abs_error: float
    passed: bool
    note: str = ""


def load_input(path: Path = DEFAULT_INPUT) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def resolve_run_id(explicit: str | None = None) -> str:
    return explicit or os.environ.get("DSD_RUN_ID") or datetime.now().strftime("%Y%m%d_%H%M%S")


def resolve_output_root(explicit: str | Path | None = None) -> Path:
    if explicit:
        return Path(explicit)
    env = os.environ.get("DSD_OUTPUT_ROOT")
    return Path(env) if env else DEFAULT_OUTPUT_ROOT


def stage_dir(stage: str, run_id: str, output_root: str | Path | None = None) -> Path:
    root = resolve_output_root(output_root)
    path = root / stage / run_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Sequence[Mapping[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def close(a: float, b: float, tol: float) -> bool:
    return math.isclose(a, b, rel_tol=tol, abs_tol=tol)


def integral(values: Sequence[float], density: Sequence[float], measure_mass: Sequence[float]) -> float:
    if not (len(values) == len(density) == len(measure_mass)):
        raise ValueError("values, density, and measure_mass must have equal lengths")
    return sum(v * w * m for v, w, m in zip(values, density, measure_mass))


def normalized_density(density: Sequence[float], measure_mass: Sequence[float], tol: float = 1e-12) -> bool:
    return all(w >= 0 for w in density) and close(sum(w * m for w, m in zip(density, measure_mass)), 1.0, tol)


def component_term(zeta: Sequence[float], weight: Sequence[float], measure_mass: Sequence[float]) -> float:
    if not normalized_density(weight, measure_mass):
        raise ValueError("weight must be nonnegative and integrate to one")
    return integral(zeta, weight, measure_mass)


def beta_bound(zeta: Sequence[float], weight: Sequence[float], measure_mass: Sequence[float]) -> float:
    return integral([abs(x) for x in zeta], weight, measure_mass)


def finite_comp(terms: Mapping[str, float], support: Iterable[str]) -> float:
    return sum(terms[c] for c in support)


def property_aggregate(records: Mapping[str, float], support: Iterable[str]) -> float:
    return sum(records[r] for r in support)


def static_descriptor(channel_value: float, property_value: float) -> tuple[float, float]:
    return (channel_value, property_value)


def geometric_partial(first_term: float, ratio: float, n_terms: int) -> float:
    return sum(first_term * (ratio ** j) for j in range(n_terms))


def geometric_infinite(first_term: float, ratio: float) -> float:
    if abs(ratio) >= 1:
        raise ValueError("absolute summability requires |ratio| < 1 for this witness")
    return first_term / (1.0 - ratio)


def geometric_absolute_sum(first_term: float, ratio: float) -> float:
    if abs(ratio) >= 1:
        raise ValueError("absolute summability requires |ratio| < 1 for this witness")
    return abs(first_term) / (1.0 - abs(ratio))


def stability_witness(
    zeta: Sequence[float],
    zeta_prime: Sequence[float],
    weight: Sequence[float],
    weight_prime: Sequence[float],
    measure_mass: Sequence[float],
) -> dict[str, float]:
    t = component_term(zeta, weight, measure_mass)
    tp = component_term(zeta_prime, weight_prime, measure_mass)
    lhs = abs(t - tp)
    direct_rhs = integral([abs(a - b) for a, b in zip(zeta, zeta_prime)], weight, measure_mass)
    direct_rhs += sum(abs(b) * abs(w - wp) * m for b, w, wp, m in zip(zeta_prime, weight, weight_prime, measure_mass))
    sup_field = max(abs(a - b) for a, b in zip(zeta, zeta_prime))
    sup_prime = max(abs(b) for b in zeta_prime)
    l1_weight = sum(abs(w - wp) * m for w, wp, m in zip(weight, weight_prime, measure_mass))
    sup_rhs = sup_field + sup_prime * l1_weight
    return {
        "T": t,
        "T_prime": tp,
        "lhs": lhs,
        "direct_rhs": direct_rhs,
        "sup_rhs": sup_rhs,
        "l1_weight": l1_weight,
    }


def weighted_structural_descriptor(alpha: Sequence[float], weight: Sequence[float], measure_mass: Sequence[float]) -> float:
    if not normalized_density(weight, measure_mass):
        raise ValueError("D_w weight must integrate to one")
    return integral(alpha, weight, measure_mass)


def scalar_transport(terms_l: Mapping[str, float], scale: float) -> dict[str, float]:
    return {f"phi({c})": scale * value for c, value in terms_l.items()}


def check_rows_to_dicts(checks: Sequence[Check]) -> list[dict[str, object]]:
    return [
        {
            "check_id": c.check_id,
            "paper_reference": c.paper_reference,
            "computed": c.computed,
            "expected": c.expected,
            "abs_error": c.abs_error,
            "passed": c.passed,
            "note": c.note,
        }
        for c in checks
    ]
