#include "freespace.h"
#include "freespace.c"
#include <math.h>
#include <stdio.h>

int main(void) {
    FreeSpaceResult r;

    float free_u[4] = {0.4f, 0.4f, 0.4f, 0.4f};
    float occ_u[4] = {0.4f, 0.4f, 0.4f, 0.4f};
    if (freespace_certify(free_u, occ_u, 4, 0.7f, 0.1f, &r) != 0) return 1;
    if (r.ok || r.reason != FREESPACE_REASON_TOO_MUCH_UNKNOWN) return 2;

    float free_c[4] = {0.9f, 0.9f, 0.9f, 0.9f};
    float occ_c[4] = {0.05f, 0.05f, 0.05f, 0.05f};
    if (freespace_certify(free_c, occ_c, 4, 0.7f, 0.15f, &r) != 0) return 3;
    if (!r.ok || r.reason != FREESPACE_REASON_NONE) return 4;

    float free_o[4] = {0.9f, 0.9f, 0.05f, 0.9f};
    float occ_o[4] = {0.05f, 0.05f, 0.9f, 0.05f};
    if (freespace_certify(free_o, occ_o, 4, 0.7f, 0.15f, &r) != 0) return 5;
    if (r.ok || r.reason != FREESPACE_REASON_OCCUPIED_PRESENT) return 6;

    float free_bad[1] = {NAN};
    float occ_bad[1] = {0.0f};
    if (freespace_certify(free_bad, occ_bad, 1, 0.7f, 0.15f, &r) != -1) return 7;
    if (freespace_certify(free_c, occ_c, 4, NAN, 0.15f, &r) != -1) return 8;
    if (freespace_certify(free_c, occ_c, 4, 0.7f, NAN, &r) != -1) return 9;
    if (freespace_certify(free_c, occ_c, 0, 0.7f, 0.15f, &r) != -1) return 10;

    printf("ok\n");
    return 0;
}
