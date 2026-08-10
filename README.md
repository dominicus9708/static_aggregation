# Static Aggregation — Basic Reproducibility Pipeline

Reproducibility code for the English manuscript:

**Kwon Dominicus, _Channel-Indexed Static Aggregation in Dimensional-Structural Describability_ (2026-08-10).**

This repository starts with a **basic formal/computational reproducibility release**. It intentionally excludes concrete, materials, cosmology, and other application-specific models. Those should be added later as separate application releases without changing the meaning of this baseline.

## What this release reproduces

- channel-indexed scalar realization of the component-term integral;
- channel norm bound in a discrete finite witness;
- finite Formation-compatible composition;
- an absolutely summable countable geometric witness;
- channel and finite-family stability inequalities;
- a finite-dimensional witness of analytic transport condition (E9);
- finite composite covariance;
- channel-support, property-support, and combined descriptor collisions;
- one-channel scalar `D_w` specialization;
- the finite worked witnesses from Section 13.

The computations are **reproducibility witnesses and regression checks, not replacements for the paper's general proofs**.

## Repository layout

```text
data/derived/static_aggregation_reproducibility/input/core/
    finite_witness.json          # official final input for v0.1.0
src/static_aggregation_reproducibility/core/
    skeleton/
    standard/
    static_aggregation/
    integration/
results/static_aggregation_reproducibility/output/
    skeleton/<run_id>/
    standard/<run_id>/
    static_aggregation/<run_id>/
    integration/<run_id>/
docs/
tests/
```

`standard` is the direct algebraic manuscript baseline. `static_aggregation` reconstructs the same core values through the analytic realization layer. No observational standard is introduced in this basic release.

## Requirements

- Python 3.11+
- No third-party runtime packages for the core pipeline

## Run on Windows

From the repository root:

```bat
py -3.11 -m unittest discover -s tests -v
py -3.11 src\static_aggregation_reproducibility\core\integration\run_static_aggregation_integration_001.py
```

The default input is:

```text
data\derived\static_aggregation_reproducibility\input\core\finite_witness.json
```

Outputs are created under:

```text
results\static_aggregation_reproducibility\output\<stage>\YYYYMMDD_HHMMSS\
```

To use a fixed run ID:

```bat
py -3.11 src\static_aggregation_reproducibility\core\integration\run_static_aggregation_integration_001.py --run-id 20260810_110200
```

## Validation status

The committed reference snapshot is produced from the same official input and should report all checks as `PASS`.

See:

- `docs/validation_scope.md`
- `docs/paper_mapping.md`
- `docs/source_registry.md`

## Release policy

`v0.1.0` is the basic formal reproducibility baseline. Later application releases may add domain-specific input, standard baselines, and application layers, but should keep the basic formal checks intact and separately identified.
