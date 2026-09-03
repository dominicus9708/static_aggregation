# Final input: core finite and analytic witnesses

This directory is the official `derived/input` starting point for the generalized basic reproducibility release.

The values are taken only from, or chosen as explicit finite-dimensional specializations of, the English canonical manuscript revision dated 2026-09-02.

- `c0 = 0`, `cplus = 1`, `cminus = -1`, and `cepsilon = epsilon` reproduce Section 13.1.
- `iota_u` is unary on `cplus` with value `2`.
- `iota_b` is binary on the full typed input pair `(cplus,cminus)` with value `-2`.
- `iota_0` is unary on `cminus` with value `0`.
- `Gpm = {iota_u,iota_b}` and `G0 = {iota_0}` reproduce the Section 13.2 typed-property support collision.
- The binary datum contains no `owner` field. The input pair is preserved rather than reassigned to one participating channel.
- `epsilon = 0.01 < delta = 0.1` instantiates the manuscript's defined-nonzero-negligible condition.
- The geometric countable family, stability arrays, transport scale, and discrete `D_w` data are finite-dimensional computational witnesses for the corresponding analytic statements; they are not additional physical assumptions.

No observational or application-specific data are included in this release.
