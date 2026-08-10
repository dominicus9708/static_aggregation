# v0.1.0 — Basic Formal Reproducibility

This release establishes the basic computational reproducibility baseline for:

**Kwon Dominicus, _Channel-Indexed Static Aggregation in Dimensional-Structural Describability_ (English closed manuscript, 2026-08-10).**

## Included

- official `derived/input` finite witness;
- `skeleton → standard → static_aggregation → integration` pipeline;
- discrete scalar component-term realization and channel bounds;
- finite Formation-compatible composition;
- absolutely summable countable geometric witness;
- channelwise and finite-family stability checks;
- scalar finite-dimensional witness of E9 analytic transport;
- finite composite covariance;
- channel-support, property-support, and combined-descriptor collision witnesses;
- one-channel scalar `D_w` specialization;
- unit tests and GitHub Actions reproducibility checks;
- committed reference result tables and summaries.

## Reference validation

- Unit tests: **9/9 PASS**
- Analytic/manuscript checks: **16/16 PASS**
- Standard-vs-static baseline comparisons: **9/9 PASS**

## Scope

This release is a formal/basic reproducibility layer. It does not include concrete, materials, cosmology, particle, or other application-specific datasets or models, and the computational witnesses do not replace the general proofs in the manuscript.

Application-specific work should be published later as separate releases while preserving `v0.1.0` as the baseline.
