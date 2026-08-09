#include "freespace.h"
#include "freespace.c"
#include <stdio.h>
int main(void) {
    float free_u[4] = {0.4f,0.4f,0.4f,0.4f};
    float occ_u[4] = {0.4f,0.4f,0.4f,0.4f};
    FreeSpaceResult r;
    freespace_certify(free_u, occ_u, 4, 0.7f, 0.1f, &r);
    if (r.ok) return 1;
    float free_c[4] = {0.9f,0.9f,0.9f,0.9f};
    float occ_c[4] = {0.05f,0.05f,0.05f,0.05f};
    freespace_certify(free_c, occ_c, 4, 0.7f, 0.15f, &r);
    if (!r.ok) return 2;
    printf("ok\n");
    return 0;
}
