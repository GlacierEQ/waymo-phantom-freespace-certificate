
from __future__ import annotations
import unittest
from src.freespace import GridEvidence, PhantomFreeSpaceCertifier

class FreeSpaceTests(unittest.TestCase):
    def test_unknown_not_free(self):
        ev = GridEvidence(free=((0.4, 0.4), (0.4, 0.4)), occupied=((0.4, 0.4), (0.4, 0.4)))
        cert = PhantomFreeSpaceCertifier(free_threshold=0.7, max_unknown_ratio=0.1).certify(ev)
        self.assertFalse(cert.ok)
        self.assertEqual(cert.refuse_reason, "TOO_MUCH_UNKNOWN")

    def test_clear_corridor(self):
        free = ((0.9, 0.9), (0.9, 0.9))
        occ = ((0.05, 0.05), (0.05, 0.05))
        cert = PhantomFreeSpaceCertifier().certify(GridEvidence(free, occ))
        self.assertTrue(cert.ok)

if __name__ == "__main__":
    unittest.main()
