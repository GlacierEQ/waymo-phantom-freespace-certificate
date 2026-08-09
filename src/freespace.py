
"""Phantom free-space certificate — inverse perception on a grid."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from typing import Sequence


class Cell(str, Enum):
    FREE = "FREE"
    OCCUPIED = "OCCUPIED"
    UNKNOWN = "UNKNOWN"


def digest(obj: object) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True)
class GridEvidence:
    """Per-cell evidence scores in [0,1] for free and occupied; residual is unknown mass."""
    free: tuple[tuple[float, ...], ...]
    occupied: tuple[tuple[float, ...], ...]

    def __post_init__(self) -> None:
        if len(self.free) != len(self.occupied):
            raise ValueError("shape mismatch")
        for fr, oc in zip(self.free, self.occupied):
            if len(fr) != len(oc):
                raise ValueError("row shape mismatch")
            for f, o in zip(fr, oc):
                if f < 0 or o < 0 or f + o > 1.0 + 1e-9:
                    raise ValueError("invalid evidence mass")


@dataclass(frozen=True)
class FreeSpaceCertificate:
    ok: bool
    free_ratio: float
    unknown_ratio: float
    occupied_ratio: float
    refuse_reason: str | None
    fingerprint: str


class PhantomFreeSpaceCertifier:
    def __init__(self, free_threshold: float = 0.7, max_unknown_ratio: float = 0.15):
        self.free_threshold = free_threshold
        self.max_unknown_ratio = max_unknown_ratio

    def classify(self, evidence: GridEvidence) -> list[list[Cell]]:
        grid: list[list[Cell]] = []
        for fr, oc in zip(evidence.free, evidence.occupied):
            row: list[Cell] = []
            for f, o in zip(fr, oc):
                if f >= self.free_threshold and f > o:
                    row.append(Cell.FREE)
                elif o >= self.free_threshold and o > f:
                    row.append(Cell.OCCUPIED)
                else:
                    row.append(Cell.UNKNOWN)
            grid.append(row)
        return grid

    def certify(self, evidence: GridEvidence) -> FreeSpaceCertificate:
        grid = self.classify(evidence)
        flat = [c for row in grid for c in row]
        n = len(flat)
        free_n = sum(c is Cell.FREE for c in flat)
        unk_n = sum(c is Cell.UNKNOWN for c in flat)
        occ_n = n - free_n - unk_n
        free_r, unk_r, occ_r = free_n / n, unk_n / n, occ_n / n
        reason = None
        ok = True
        if unk_r > self.max_unknown_ratio:
            ok = False
            reason = "TOO_MUCH_UNKNOWN"
        body = {
            "ok": ok,
            "free": free_r,
            "unknown": unk_r,
            "occupied": occ_r,
            "reason": reason,
            "grid": [[c.value for c in row] for row in grid],
        }
        return FreeSpaceCertificate(ok, free_r, unk_r, occ_r, reason, digest(body))
