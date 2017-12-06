

def chs2lba(
    cylinder,
    head,
    sector,
    heads_per_cylinder=255,
    sectors_per_track=63
):
    return ((cylinder * heads_per_cylinder) + head) * \
           sectors_per_track + sector - 1
