from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str):
    return json.loads((ROOT / path).read_text())


CANONICAL = load("machine/canonical-position.json")
CAPABILITIES = load("machine/capabilities.json")
TARGET = load("machine/target-contract.json")
STATE = load("machine/excellence-state.json")
PROOF = load("machine/canonical-position-proof.json")


class CanonicalPositionContractTests(unittest.TestCase):
    def test_repository_owns_bounded_grid_certificate_not_driving_authority(self):
        self.assertEqual(CANONICAL["role"], "CANONICAL_SPECIALIST")
        self.assertEqual(
            CANONICAL["owns"], "evidence_bound_whole_grid_freespace_certification"
        )
        self.assertIn("autonomous-driving actuation authority", CANONICAL["does_not_own"])
        self.assertIn("sensor provenance authentication", CANONICAL["does_not_own"])

    def test_uncertainty_lane_graph_is_not_integrated(self):
        edge = CANONICAL["relationships"][0]
        self.assertEqual(
            edge["repository"], "GlacierEQ/waymo-uncertainty-lane-graph"
        )
        self.assertFalse(edge["integration_exercised"])

    def test_capabilities_are_repository_native(self):
        capabilities = set(CAPABILITIES["capabilities"])
        self.assertNotIn("hyper-scaling", capabilities)
        self.assertIn("occupied_cell_certificate_veto", capabilities)
        self.assertIn("unknown_ratio_certificate_ceiling", capabilities)
        self.assertIn("exact_grid_evidence_fingerprint", capabilities)
        self.assertIn("python_c_certificate_outcome_parity", capabilities)

    def test_machine_state_is_evolving_after_exact_proof(self):
        self.assertEqual(TARGET["current"]["state"], "EVOLVING")
        self.assertTrue(TARGET["current"]["canonical_position_resolved"])
        self.assertFalse(TARGET["current"]["deployed"])
        self.assertEqual(STATE["principal_state"], "EVOLVING")
        self.assertEqual(
            STATE["gates"]["CANONICAL_POSITION_RESOLVED"]["status"], "PASS"
        )

    def test_proof_binds_exact_tested_source_and_run(self):
        self.assertEqual(
            PROOF["source_sha"],
            "feee6e51999ea391bd8793a77f2576c21b6464bc",
        )
        self.assertEqual(PROOF["workflow"]["run_id"], 31403184766)
        self.assertEqual(PROOF["workflow"]["conclusion"], "success")
        self.assertEqual(set(PROOF["workflow"]["jobs"]), {"py", "c"})

    def test_truth_boundary_excludes_real_world_authority(self):
        boundary = CAPABILITIES["truth_boundary"]
        self.assertIn("does not authenticate sensor provenance", boundary)
        self.assertIn("autonomous driving", boundary)
        self.assertIn("Waymo affiliation/adoption", boundary)


if __name__ == "__main__":
    unittest.main()
