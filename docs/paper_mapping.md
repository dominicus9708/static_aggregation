# Manuscript-to-code mapping

| Check ID | Manuscript item | Computational reproduction |
|---|---|---|
| SA-01 | Section 4: realized component term and channel bound | Discrete scalar measure-space realization; verifies `|T(c)| <= beta_c` |
| SA-02 | Section 5: finite Formation-compatible composition | Reproduces finite sums for `F0`, `Fpm`, `Fepsilon` |
| SA-03 | Section 6: optional countable absolute extension | Geometric absolutely summable family; verifies partial-sum convergence and enumeration invariance for finite truncation |
| SA-04 | Section 9: channelwise combined stability | Verifies the direct integral bound and displayed `L^infty + L^1` upper bound |
| SA-05 | Section 9: finite composite stability | Sums channel perturbation bounds over a finite support |
| SA-06 | Section 10: analytic lift to E9 | Scalar linear isomorphism `J(x)=s x`; verifies `J(T_L(c))=T_M(phi(c))` |
| SA-07 | Section 10: finite composite covariance | Verifies `J(Comp_L(F))=Comp_M(phi(F))` |
| SA-08 | Section 11 / Section 13.1 | Distinct channel supports `F0 != Fpm` with equal aggregate `0` |
| SA-09 | Section 11 / Section 13.2 | Distinct property supports `G0 != Gpm` with equal aggregate `0` |
| SA-10 | Section 13.3 | Distinct combined support-tagged records with identical static descriptor `(0,0)` |
| SA-11 | Section 12: `D_w` specialization | Computes a normalized discrete weighted structural descriptor |

The mapping is intentionally conservative: the general proofs remain in the paper; the code supplies reproducible finite witnesses and regression checks.
