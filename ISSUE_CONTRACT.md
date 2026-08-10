# ISSUE CONTRACT
## Pain
Object detections do not prove free space. Unknown or malformed evidence can be mistaken for drivable space, and a certificate that ignores occupied cells can certify a fully occupied grid.

## Success
- Cell states remain `FREE | OCCUPIED | UNKNOWN`
- Every evidence mass and certifier threshold is finite and bounded
- Grid evidence is non-empty, rectangular, and mass-consistent
- Unknown cells are never promoted to FREE
- Any `OCCUPIED` cell refuses the whole-grid free-space certificate
- Unknown ratio above policy refuses the certificate
- Successful certificate binds the exact evidence grid and exact certifier policy into its fingerprint
- Python and native C enforce the same occupied/unknown fail-closed outcome

## Boundary
This is an independent inverse-perception reference mechanism. A certificate is not autonomous-driving authority, does not authenticate sensor provenance, does not prove real-world drivable geometry beyond supplied evidence, and does not claim Waymo affiliation/adoption.
