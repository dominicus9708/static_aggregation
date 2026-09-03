# v0.2.0 — General Property Interface Synchronization

This release synchronizes the repository with the generalized English canonical manuscript revision:

**Kwon Dominicus, _Channel-Indexed Static Aggregation in Dimensional-Structural Describability_ (2026-09-02).**

## Changes from v0.1.1

- replaced the scalar-only property-witness input encoding with explicit typed property data containing `kind`, `profile`, `input`, and `value`;
- added a unary/binary/unary Section 13.2 witness matching the generalized Property Axiom System interface;
- preserved the binary property datum on its full input pair `(cplus,cminus)` without introducing an owner channel;
- added typed property-schema and support-resolution checks to the skeleton stage;
- updated the algebraic standard and static-aggregation stages to aggregate typed property data through their supplied values without collapsing the typed inputs;
- added an integration comparison that verifies typed property data are preserved between the standard and analytic layers;
- synchronized manuscript section mappings, validation scope, source registry, input documentation, README, and citation metadata;
- preserved the original channel-indexed analytic core and the historical v0.1.x snapshots.

## Validation status

Validated locally against the synchronized source tree:

- Unit tests: **9/9 PASS**
- Static/manuscript checks: **16/16 PASS**
- Standard-vs-static integration comparisons: **10/10 PASS**
- Typed property schema: **PASS**
- Property support resolution: **PASS**

## Scope

This remains a formal/basic reproducibility package. The finite computations do not replace the manuscript's general proofs, do not implement the full Property Axiom System, and do not add physical or application-specific semantics.
