from __future__ import annotations

import math
import unittest

from src.freespace import GridEvidence, PhantomFreeSpaceCertifier


class FreeSpaceTests(unittest.TestCase):
    def test_unknown_not_free(self):
        evidence = GridEvidence(
            free=((0.4, 0.4), (0.4, 0.4)),
            occupied=((0.4, 0.4), (0.4, 0.4)),
        )
        cert = PhantomFreeSpaceCertifier(
            free_threshold=0.7, max_unknown_ratio=0.1
        ).certify(evidence)
        self.assertFalse(cert.ok)
        self.assertEqual(cert.refuse_reason, "TOO_MUCH_UNKNOWN")
        self.assertEqual(cert.free_ratio, 0.0)

    def test_clear_corridor(self):
        free = ((0.9, 0.9), (0.9, 0.9))
        occupied = ((0.05, 0.05), (0.05, 0.05))
        cert = PhantomFreeSpaceCertifier().certify(GridEvidence(free, occupied))
        self.assertTrue(cert.ok)
        self.assertIsNone(cert.refuse_reason)
        self.assertEqual(cert.free_ratio, 1.0)
        self.assertEqual(cert.occupied_ratio, 0.0)

    def test_occupied_cell_refuses_certificate(self):
        evidence = GridEvidence(
            free=((0.9, 0.9), (0.05, 0.9)),
            occupied=((0.05, 0.05), (0.9, 0.05)),
        )
        cert = PhantomFreeSpaceCertifier().certify(evidence)
        self.assertFalse(cert.ok)
        self.assertEqual(cert.refuse_reason, "OCCUPIED_PRESENT")
        self.assertEqual(cert.occupied_ratio, 0.25)

    def test_one_occupied_cell_cannot_hide_below_unknown_budget(self):
        evidence = GridEvidence(
            free=((0.9,) * 9 + (0.05,),),
            occupied=((0.05,) * 9 + (0.9,),),
        )
        cert = PhantomFreeSpaceCertifier(max_unknown_ratio=0.15).certify(evidence)
        self.assertEqual(cert.unknown_ratio, 0.0)
        self.assertFalse(cert.ok)
        self.assertEqual(cert.refuse_reason, "OCCUPIED_PRESENT")

    def test_empty_and_ragged_grids_refuse(self):
        with self.assertRaisesRegex(ValueError, "grid cannot be empty"):
            GridEvidence((), ())
        with self.assertRaisesRegex(ValueError, "rectangular"):
            GridEvidence(
                free=((0.9,), (0.9, 0.9)),
                occupied=((0.05,), (0.05, 0.05)),
            )

    def test_non_finite_evidence_refuses(self):
        for bad in (math.nan, math.inf, -math.inf):
            with self.assertRaisesRegex(ValueError, "finite numbers"):
                GridEvidence(free=((bad,),), occupied=((0.0,),))

    def test_invalid_evidence_mass_refuses(self):
        with self.assertRaisesRegex(ValueError, "\[0,1\]"):
            GridEvidence(free=((1.1,),), occupied=((0.0,),))
        with self.assertRaisesRegex(ValueError, "invalid evidence mass"):
            GridEvidence(free=((0.7,),), occupied=((0.4,),))

    def test_invalid_policy_refuses(self):
        for threshold in (0.0, -0.1, 1.1, math.nan, math.inf):
            with self.assertRaisesRegex(ValueError, "free_threshold"):
                PhantomFreeSpaceCertifier(free_threshold=threshold)
        for unknown in (-0.1, 1.0, 1.1, math.nan, math.inf):
            with self.assertRaisesRegex(ValueError, "max_unknown_ratio"):
                PhantomFreeSpaceCertifier(max_unknown_ratio=unknown)

    def test_certificate_binds_exact_evidence_not_only_classification(self):
        first = GridEvidence(free=((0.9,),), occupied=((0.05,),))
        second = GridEvidence(free=((0.8,),), occupied=((0.05,),))
        certifier = PhantomFreeSpaceCertifier()
        first_cert = certifier.certify(first)
        second_cert = certifier.certify(second)
        self.assertTrue(first_cert.ok and second_cert.ok)
        self.assertNotEqual(
            first_cert.evidence_fingerprint, second_cert.evidence_fingerprint
        )
        self.assertNotEqual(first_cert.fingerprint, second_cert.fingerprint)

    def test_certificate_binds_policy_even_when_outcome_same(self):
        evidence = GridEvidence(free=((0.9,),), occupied=((0.05,),))
        first = PhantomFreeSpaceCertifier(
            free_threshold=0.7, max_unknown_ratio=0.15
        ).certify(evidence)
        second = PhantomFreeSpaceCertifier(
            free_threshold=0.8, max_unknown_ratio=0.15
        ).certify(evidence)
        self.assertTrue(first.ok and second.ok)
        self.assertNotEqual(first.policy_fingerprint, second.policy_fingerprint)
        self.assertNotEqual(first.fingerprint, second.fingerprint)

    def test_wrong_evidence_type_refuses(self):
        with self.assertRaisesRegex(ValueError, "GridEvidence"):
            PhantomFreeSpaceCertifier().certify({})  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
