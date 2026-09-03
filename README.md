# Static Aggregation — Basic Reproducibility Pipeline

Reproducibility code for the English canonical manuscript revision:

**Kwon Dominicus, _Channel-Indexed Static Aggregation in Dimensional-Structural Describability_ (2026-09-02).**

The `v0.2.x` line synchronizes the basic formal/computational pipeline with the generalized Property Axiom System interface while preserving the channel-indexed analytic core. It intentionally excludes concrete, materials, cosmology, and other application-specific models. Those should be added later as separate application releases without changing the meaning of this baseline.

## What this release reproduces

- channel-indexed scalar realization of the component-term integral;
- channel norm bound in a discrete finite witness;
- finite Formation-compatible composition;
- an absolutely summable countable geometric witness;
- channel and finite-family stability inequalities;
- a finite-dimensional witness of analytic transport condition (E9);
- finite composite covariance;
- channel-support, typed-property-support, and combined descriptor collisions;
- a general typed-property witness containing unary and binary property data;
- preservation of the binary input pair without introducing an owner channel;
- one-channel scalar `D_w` specialization;
- the finite worked witnesses from Section 13.

The computations are **reproducibility witnesses and regression checks, not replacements for the paper's general proofs**.

## Generalized property interface

The official `v0.2.x` input encodes each selected defined property datum with:

```json
{
  "kind": "varpi_b",
  "profile": ["channel", "channel"],
  "input": ["cplus", "cminus"],
  "value": -2.0
}
```

The binary datum remains attached to the full typed input pair. The reproducibility layer does not assign it to either participating channel unless an additional allocation rule is explicitly supplied.

## Repository layout

```text
data/derived/static_aggregation_reproducibility/input/core/
    finite_witness.json          # official v0.2.x core witness
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
py -3.11 src\static_aggregation_reproducibility\core\integration\run_static_aggregation_integration_001.py --run-id 20260903_132600
```

## Validation status

The `v0.2.0` synchronization check produced:

- Unit tests: **9/9 PASS**
- Static/manuscript checks: **16/16 PASS**
- Standard-vs-static integration comparisons: **10/10 PASS**
- Typed property schema and support resolution: **PASS**

The committed `20260903_132600` reference snapshot is generated from the official `v0.2.x` input.

See:

- `docs/validation_scope.md`
- `docs/paper_mapping.md`
- `docs/source_registry.md`

## Release policy

- `v0.1.0` established the original basic formal reproducibility baseline.
- `v0.1.1` synchronized metadata with the shortened 2026-08-10 manuscript title.
- `v0.2.0` synchronizes the repository with the 2026-09-02 generalized static-aggregation manuscript and the general Property Axiom System interface.

Later application releases may add domain-specific input, standard baselines, and application layers, but should keep the basic formal checks intact and separately identified.
