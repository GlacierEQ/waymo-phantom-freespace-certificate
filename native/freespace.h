#ifndef FREESPACE_H
#define FREESPACE_H

typedef enum { CELL_FREE, CELL_OCCUPIED, CELL_UNKNOWN } CellState;
typedef enum {
    FREESPACE_REASON_NONE = 0,
    FREESPACE_REASON_OCCUPIED_PRESENT = 1,
    FREESPACE_REASON_TOO_MUCH_UNKNOWN = 2
} FreeSpaceReason;

typedef struct {
    int ok;
    float free_ratio, unknown_ratio, occupied_ratio;
    FreeSpaceReason reason;
} FreeSpaceResult;

CellState classify_cell(float free_ev, float occ_ev, float free_threshold);
int freespace_certify(const float *free_ev, const float *occ_ev, int n,
                      float free_threshold, float max_unknown_ratio,
                      FreeSpaceResult *out);

#endif
