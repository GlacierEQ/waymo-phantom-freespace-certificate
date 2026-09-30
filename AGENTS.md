# AGENTS.md — waymo-phantom-freespace-certificate

**Company:** Waymo
**Domain:** Autonomous Vehicle Safety & Perception

## Quick Rules
- **Test command:** `PYTHONPATH=src pytest tests/ -v`
- **Lint:** `ruff check src/ tests/`
- **No drive-by edits** — load the skill first.

## Architecture
- `src/waymo_phantom_freespace_certificate/core.py` — Domain logic (Autonomous Vehicle Safety & Perception)
- `tests/` — Verified test suite
- `.github/workflows/ci.yml` — Enforced CI pipeline
