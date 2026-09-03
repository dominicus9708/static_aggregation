# Manuscript-to-code mapping

This map is synchronized with the English canonical manuscript revision dated 2026-09-02.

| Check ID | Manuscript item | Computational reproduction |
|---|---|---|
| SA-01 | Section 4: functional realization and channel bound | Discrete scalar measure-space realization; verifies `|T(c)| <= beta_c` |
| SA-02 | Section 5 / Section 13.1: Formation-compatible finite composition | Reproduces finite sums for `F0`, `Fpm`, `Fepsilon` |
| SA-03 | Section 6: optional countable analytic extension | Geometric absolutely summable family; verifies truncation accuracy and finite reordering agreement |
| SA-04 | Section 9.1: perturbation of one channel | Verifies the direct integral bound and displayed `L^infinity + L^1` upper bound |
| SA-05 | Section 9.2: perturbation of a finite channel family | Sums channel perturbation bounds over a two-channel finite witness |
| SA-06 | Section 10.1: analytic transport condition (E9) | Scalar linear isomorphism `J(x)=s x`; verifies `J(T_L(c))=T_M(phi(c))` |
| SA-07 | Section 10.1: finite composite covariance | Verifies `J(Comp_L(F))=Comp_M(phi(F))` |
| SA-08 | Section 11.1 / Section 13.1: channel support collision | Distinct channel supports `F0 != Fpm` with equal aggregate `0` |
| SA-09 | Section 11.3 / Section 13.2: typed property support collision | Uses unary/binary/unary typed property data; verifies distinct supports with equal aggregate `0` while the binary input pair remains unallocated to an owner channel |
| SA-10 | Section 11.4 / Section 13.3: combined static descriptor collision | Distinct support-retaining channel/property data with identical static descriptor `(0,0)` |
| SA-11 | Section 12.1: `D_w` specialization | Computes a normalized discrete weighted structural descriptor |

The mapping is intentionally conservative. General Banach-space, covariance, and reconstruction results remain manuscript proofs. The code supplies finite witnesses, schema checks, and regression tests only.
