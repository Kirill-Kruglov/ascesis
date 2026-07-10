"""
SCOUT 16 (OC-TUNE AT SCALE, NOT citable): scout 15's frozen pipeline —
no new knobs, only scale (prereg E5 of scout 15: the window question is
a matter of n). R_INST 3 -> 8, K_SEEDS 3 -> 5 (cells 15 -> 25 per
instance; per-stratum power step 0.33 -> ~0.12 on admissible pairs).

Everything else is byte-identical to scout 15: same rule, same
thresholds, same bank construction, same TUNE master seed lineage.
"""
import scout_14_oc_tune as s14
import scout_15_oc_tune2 as s15

s14.R_INST = 8
s14.K_SEEDS = 5
s15.R_INST = 8
s15.K_SEEDS = 5

if __name__ == '__main__':
    s15.main()
