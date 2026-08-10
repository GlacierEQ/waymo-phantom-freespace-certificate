/* Babel: C — inverse perception free-space certificate on bounded grids. */
#include "freespace.h"
#include <math.h>

static int valid_mass(float value) {
    return isfinite(value) && value >= 0.0f && value <= 1.0f;
}

CellState classify_cell(float free_ev, float occ_ev, float free_threshold) {
    if (!valid_mass(free_ev) || !valid_mass(occ_ev) ||
        !isfinite(free_threshold) || free_threshold <= 0.0f ||
        free_threshold > 1.0f || free_ev + occ_ev > 1.0f + 1e-6f) {
        return CELL_UNKNOWN;
    }
    if (free_ev >= free_threshold && free_ev > occ_ev) return CELL_FREE;
    if (occ_ev >= free_threshold && occ_ev > free_ev) return CELL_OCCUPIED;
    return CELL_UNKNOWN;
}

int freespace_certify(const float *free_ev, const float *occ_ev, int n,
                      float free_threshold, float max_unknown_ratio,
                      FreeSpaceResult *out) {
    if (!free_ev || !occ_ev || n <= 0 || !out) return -1;
    if (!isfinite(free_threshold) || free_threshold <= 0.0f || free_threshold > 1.0f)
        return -1;
    if (!isfinite(max_unknown_ratio) || max_unknown_ratio < 0.0f ||
        max_unknown_ratio >= 1.0f)
        return -1;

    int free_n = 0, unk_n = 0, occ_n = 0;
    for (int i = 0; i < n; i++) {
        if (!valid_mass(free_ev[i]) || !valid_mass(occ_ev[i]) ||
            free_ev[i] + occ_ev[i] > 1.0f + 1e-6f)
            return -1;
        CellState state = classify_cell(free_ev[i], occ_ev[i], free_threshold);
        if (state == CELL_FREE) free_n++;
        else if (state == CELL_UNKNOWN) unk_n++;
        else occ_n++;
    }

    out->free_ratio = (float)free_n / (float)n;
    out->unknown_ratio = (float)unk_n / (float)n;
    out->occupied_ratio = (float)occ_n / (float)n;
    out->ok = 0;
    out->reason = FREESPACE_REASON_NONE;

    if (occ_n > 0) {
        out->reason = FREESPACE_REASON_OCCUPIED_PRESENT;
    } else if (out->unknown_ratio > max_unknown_ratio) {
        out->reason = FREESPACE_REASON_TOO_MUCH_UNKNOWN;
    } else {
        out->ok = 1;
    }
    return 0;
}
