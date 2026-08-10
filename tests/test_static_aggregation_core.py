from __future__ import annotations

import sys
import unittest
from pathlib import Path

CORE = Path(__file__).resolve().parents[1] / "src" / "static_aggregation_reproducibility" / "core"
sys.path.insert(0, str(CORE))

from common import beta_bound, close, component_term, finite_comp, geometric_infinite, geometric_partial, property_aggregate, scalar_transport, stability_witness, static_descriptor, weighted_structural_descriptor


class StaticAggregationCoreTests(unittest.TestCase):
    def test_constant_component_term_and_bound(self):
        zeta,w,mu=[1.0]*4,[1.0]*4,[0.25]*4
        self.assertTrue(close(component_term(zeta,w,mu),1.0,1e-12))
        self.assertLessEqual(abs(component_term(zeta,w,mu)),beta_bound(zeta,w,mu))

    def test_finite_collision(self):
        terms={"c0":0.0,"cplus":1.0,"cminus":-1.0}
        self.assertEqual(finite_comp(terms,["c0"]),finite_comp(terms,["cplus","cminus"]))

    def test_countable_geometric_witness(self):
        self.assertAlmostEqual(geometric_partial(1.0,0.5,64),geometric_infinite(1.0,0.5),places=12)

    def test_stability_bound(self):
        r=stability_witness([1.0,3.0],[1.2,2.8],[0.8,1.2],[1.1,0.9],[0.5,0.5])
        self.assertLessEqual(r["lhs"],r["direct_rhs"]+1e-12)
        self.assertLessEqual(r["direct_rhs"],r["sup_rhs"]+1e-12)

    def test_property_collision(self):
        props={"u":2.0,"b":-2.0,"z":0.0}
        self.assertEqual(property_aggregate(props,["u","b"]),property_aggregate(props,["z"]))

    def test_combined_collision(self):
        self.assertEqual(static_descriptor(0.0,0.0),static_descriptor(1.0+-1.0,2.0+-2.0))

    def test_transport_e9_scalar_witness(self):
        terms={"cplus":1.0,"cepsilon":0.01}; scale=2.5; transported=scalar_transport(terms,scale)
        for c,value in terms.items(): self.assertAlmostEqual(scale*value,transported[f"phi({c})"])

    def test_finite_covariance(self):
        terms={"cplus":1.0,"cepsilon":0.01}; scale=2.5; transported=scalar_transport(terms,scale)
        self.assertAlmostEqual(scale*finite_comp(terms,["cplus","cepsilon"]),transported["phi(cplus)"]+transported["phi(cepsilon)"])

    def test_weighted_structural_descriptor(self):
        value=weighted_structural_descriptor([1.0,2.0,3.0],[0.5,1.0,1.5],[1/3,1/3,1/3])
        self.assertAlmostEqual(value,7.0/3.0)


if __name__ == "__main__":
    unittest.main()
