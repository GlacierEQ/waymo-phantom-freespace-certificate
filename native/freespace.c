/* Babel: C — inverse perception free-space certificate on grids. */
#include "freespace.h"

CellState classify_cell(float free_ev, float occ_ev, float free_threshold) {
    if (free_ev >= free_threshold && free_ev > occ_ev) return CELL_FREE;
    if (occ_ev >= free_threshold && occ_ev > free_ev) return CELL_OCCUPIED;
    return CELL_UNKNOWN;
}

int freespace_certify(const float *free_ev, const float *occ_ev, int n,
                      float free_threshold, float max_unknown_ratio,
                      FreeSpaceResult *out) {
    if (!free_ev || !occ_ev || n <= 0 || !out) return -1;
    int free_n=0, unk_n=0, occ_n=0;
    for (int i=0;i<n;i++) {
        CellState s = classify_cell(free_ev[i], occ_ev[i], free_threshold);
        if (s == CELL_FREE) free_n++;
        else if (s == CELL_UNKNOWN) unk_n++;
        else occ_n++;
    }
    out->free_ratio = (float)free_n / (float)n;
    out->unknown_ratio = (float)unk_n / (float)n;
    out->occupied_ratio = (float)occ_n / (float)n;
    out->ok = out->unknown_ratio <= max_unknown_ratio ? 1 : 0;
    return 0;
}
