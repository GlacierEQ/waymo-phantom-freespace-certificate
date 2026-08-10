"""Phantom free-space certificate — inverse perception on a bounded grid.

A certificate is issued only when the supplied grid contains no occupied cells
and its unknown-cell ratio stays within the configured ceiling. The terminal
receipt binds the exact evidence grid and certifier policy. This is an
independent reference mechanism, not autonomous-driving authority.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from enum import Enum


class Cell(str, Enum):
    FREE = "FREE"
    OCCUPIED = "OCCUPIED"
    UNKNOWN = "UNKNOWN"


def digest(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(
            obj,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode()
    ).hexdigest()


@dataclass(frozen=True)
class GridEvidence:
    """Per-cell free/occupied evidence masses; residual mass is unknown."""

    free: tuple[tuple[float, ...], ...]
    occupied: tuple[tuple[float, ...], ...]

    def __post_init__(self) -> None:
        if not self.free or not self.occupied:
            raise ValueError("grid cannot be empty")
        if len(self.free) != len(self.occupied):
            raise ValueError("shape mismatch")

        width = len(self.free[0])
        if width == 0:
            raise ValueError("grid rows cannot be empty")

        for row_index, (fr, oc) in enumerate(zip(self.free, self.occupied)):
            if len(fr) != width or len(oc) != width:
                raise ValueError("grid must be rectangular")
            for col_index, (f, o) in enumerate(zip(fr, oc)):
                if isinstance(f, bool) or isinstance(o, bool):
                    raise ValueError("evidence masses must be finite numbers")
                if not isinstance(f, (int, float)) or not isinstance(o, (int, float)):
                    raise ValueError("evidence masses must be finite numbers")
                f_value, o_value = float(f), float(o)
                if not math.isfinite(f_value) or not math.isfinite(o_value):
                    raise ValueError("evidence masses must be finite numbers")
                if f_value < 0 or o_value < 0 or f_value > 1 or o_value > 1:
                    raise ValueError("evidence mass must be in [0,1]")
                if f_value + o_value > 1.0 + 1e-12:
                    raise ValueError(
                        f"invalid evidence mass at cell {row_index},{col_index}"
                    )

    def fingerprint(self) -> str:
        return digest(
            {
                "free": [list(row) for row in self.free],
                "occupied": [list(row) for row in self.occupied],
            }
        )


@dataclass(frozen=True)
class FreeSpaceCertificate:
    ok: bool
    free_ratio: float
    unknown_ratio: float
    occupied_ratio: float
    refuse_reason: str | None
    evidence_fingerprint: str
    policy_fingerprint: str
    fingerprint: str


class PhantomFreeSpaceCertifier:
    def __init__(
        self,
        free_threshold: float = 0.7,
        max_unknown_ratio: float = 0.15,
    ):
        if isinstance(free_threshold, bool) or not isinstance(
            free_threshold, (int, float)
        ):
            raise ValueError("free_threshold must be finite and in (0,1]")
        if isinstance(max_unknown_ratio, bool) or not isinstance(
            max_unknown_ratio, (int, float)
        ):
            raise ValueError("max_unknown_ratio must be finite and in [0,1)")
        free_threshold = float(free_threshold)
        max_unknown_ratio = float(max_unknown_ratio)
        if not math.isfinite(free_threshold) or not 0 < free_threshold <= 1:
            raise ValueError("free_threshold must be finite and in (0,1]")
        if not math.isfinite(max_unknown_ratio) or not 0 <= max_unknown_ratio < 1:
            raise ValueError("max_unknown_ratio must be finite and in [0,1)")
        self.free_threshold = free_threshold
        self.max_unknown_ratio = max_unknown_ratio
        self.policy_fingerprint = digest(
            {
                "free_threshold": self.free_threshold,
                "max_unknown_ratio": self.max_unknown_ratio,
                "occupied_cells_permitted": False,
                "unknown_policy": "ratio_ceiling",
            }
        )

    def classify(self, evidence: GridEvidence) -> tuple[tuple[Cell, ...], ...]:
        if not isinstance(evidence, GridEvidence):
            raise ValueError("evidence must be GridEvidence")
        grid: list[tuple[Cell, ...]] = []
        for fr, oc in zip(evidence.free, evidence.occupied):
            row: list[Cell] = []
            for f, o in zip(fr, oc):
                if f >= self.free_threshold and f > o:
                    row.append(Cell.FREE)
                elif o >= self.free_threshold and o > f:
                    row.append(Cell.OCCUPIED)
                else:
                    row.append(Cell.UNKNOWN)
            grid.append(tuple(row))
        return tuple(grid)

    def certify(self, evidence: GridEvidence) -> FreeSpaceCertificate:
        grid = self.classify(evidence)
        flat = [cell for row in grid for cell in row]
        n = len(flat)
        free_n = sum(cell is Cell.FREE for cell in flat)
        unk_n = sum(cell is Cell.UNKNOWN for cell in flat)
        occ_n = n - free_n - unk_n
        free_r = free_n / n
        unk_r = unk_n / n
        occ_r = occ_n / n

        reason: str | None = None
        if occ_n:
            reason = "OCCUPIED_PRESENT"
        elif unk_r > self.max_unknown_ratio:
            reason = "TOO_MUCH_UNKNOWN"
        ok = reason is None

        evidence_fingerprint = evidence.fingerprint()
        grid_values = [[cell.value for cell in row] for row in grid]
        body = {
            "ok": ok,
            "free": free_r,
            "unknown": unk_r,
            "occupied": occ_r,
            "reason": reason,
            "grid": grid_values,
            "evidence_fingerprint": evidence_fingerprint,
            "policy_fingerprint": self.policy_fingerprint,
        }
        return FreeSpaceCertificate(
            ok,
            free_r,
            unk_r,
            occ_r,
            reason,
            evidence_fingerprint,
            self.policy_fingerprint,
            digest(body),
        )
