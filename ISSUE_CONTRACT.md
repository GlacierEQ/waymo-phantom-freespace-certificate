# ISSUE CONTRACT
## Pain
Detectors output objects; free space is assumed. Phantoms and unknown regions get treated as drivable.
## Success
- Cell states: FREE | OCCUPIED | UNKNOWN
- Certificate only when free cells meet evidence threshold
- Unknown never auto-promoted to FREE
