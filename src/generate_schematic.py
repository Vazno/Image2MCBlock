import os
from enum import Enum

import mcschematic

class Version(Enum):
	"""
	The Enum used to specify which Minecraft version we want to save a schematic
	for in MCSchematic#save().
	Numbers are taken from: https://minecraft.fandom.com/wiki/Data_version
	"""
	JE_1_20_1 = 3465
	JE_1_20_1_RELEASE_CANDIDATE_1 = 3464
	JE_1_20 = 3463
	JE_1_20_RELEASE_CANDIDATE_1 = 3462
	JE_1_20_PRE_RELEASE_7 = 3461
	JE_1_20_PRE_RELEASE_6 = 3460
	JE_1_20_PRE_RELEASE_5 = 3458
	JE_1_20_PRE_RELEASE_4 = 3457
	JE_1_20_PRE_RELEASE_3 = 3456
	JE_1_20_PRE_RELEASE_2 = 3455
	JE_1_20_PRE_RELEASE_1 = 3454
	JE_23W18A = 3453
	JE_23W17A = 3452
	JE_23W16A = 3449
	JE_23W14A = 3445
	JE_23W13A = 3443
	JE_23W12A = 3442
	JE_1_19_4 = 3337
	JE_1_19_4_RELEASE_CANDIDATE_3 = 3336
	JE_1_19_4_RELEASE_CANDIDATE_2 = 3335
	JE_1_19_4_RELEASE_CANDIDATE_1 = 3334
	JE_1_19_4_PRE_RELEASE_4 = 3333
	JE_1_19_4_PRE_RELEASE_3 = 3332
	JE_1_19_4_PRE_RELEASE_2 = 3331
	JE_1_19_4_PRE_RELEASE_1 = 3330
	JE_23W07A = 3329
	JE_23W06A = 3326
	JE_23W05A = 3323
	JE_23W04A = 3321
	JE_23W03A = 3320
	JE_1_19_3 = 3218
	JE_1_19_3_RELEASE_CANDIDATE_3 = 3217
	JE_1_19_3_RELEASE_CANDIDATE_2 = 3216
	JE_1_19_3_RELEASE_CANDIDATE_1 = 3215
	JE_1_19_3_PRE_RELEASE_3 = 3213
	JE_1_19_3_PRE_RELEASE_2 = 3212
	JE_1_19_3_PRE_RELEASE_1 = 3211
	JE_22W46A = 3210
	JE_22W45A = 3208
	JE_22W44A = 3207
	JE_22W43A = 3206
	JE_22W42A = 3205
	JE_1_19_2 = 3120
	JE_1_19_2_RELEASE_CANDIDATE_2 = 3119
	JE_1_19_2_RELEASE_CANDIDATE_1 = 3118
	JE_1_19_1 = 3117
	JE_1_19_1_RELEASE_CANDIDATE_3 = 3116
	JE_1_19_1_RELEASE_CANDIDATE_2 = 3115
	JE_1_19_1_PRE_RELEASE_6 = 3114
	JE_1_19_1_PRE_RELEASE_5 = 3113
	JE_1_19_1_PRE_RELEASE_4 = 3112
	JE_1_19_1_PRE_RELEASE_3 = 3111
	JE_1_19_1_PRE_RELEASE_2 = 3110
	JE_1_19_1_RELEASE_CANDIDATE_1 = 3109
	JE_1_19_1_PRE_RELEASE_1 = 3107
	JE_22W24A = 3106
	JE_1_19 = 3105
	JE_1_19_RELEASE_CANDIDATE_2 = 3104
	JE_1_19_RELEASE_CANDIDATE_1 = 3103
	JE_1_19_PRE_RELEASE_5 = 3102
	JE_1_19_PRE_RELEASE_4 = 3101
	JE_1_19_PRE_RELEASE_3 = 3100
	JE_1_19_PRE_RELEASE_2 = 3099
	JE_1_19_PRE_RELEASE_1 = 3098
	JE_22W19A = 3096
	JE_22W18A = 3095
	JE_22W17A = 3093
	JE_22W16B = 3092
	JE_22W16A = 3091
	JE_22W15A = 3089
	JE_22W14A = 3088
	JE_22W13A = 3085
	JE_22W12A = 3082
	JE_22W11A = 3080
	JE_DEEP_DARK_EXPERIMENTAL_SNAPSHOT_1 = 3066
	JE_1_18_2 = 2975
	JE_1_18_2_RELEASE_CANDIDATE_1 = 2974
	JE_1_18_2_PRE_RELEASE_3 = 2973
	JE_1_18_2_PRE_RELEASE_2 = 2972
	JE_1_18_2_PRE_RELEASE_1 = 2971
	JE_22W07A = 2969
	JE_22W06A = 2968
	JE_22W05A = 2967
	JE_22W03A = 2966
	JE_1_18_1 = 2865
	JE_1_18_1_RELEASE_CANDIDATE_3 = 2864
	JE_1_18_1_RELEASE_CANDIDATE_2 = 2863
	JE_1_18_1_RELEASE_CANDIDATE_1 = 2862
	JE_1_18_1_PRE_RELEASE_1 = 2861
	JE_1_18 = 2860
	JE_1_18_RELEASE_CANDIDATE_4 = 2859
	JE_1_18_RELEASE_CANDIDATE_3 = 2858
	JE_1_18_RELEASE_CANDIDATE_2 = 2857
	JE_1_18_RELEASE_CANDIDATE_1 = 2856
	JE_1_18_PRE_RELEASE_8 = 2855
	JE_1_18_PRE_RELEASE_7 = 2854
	JE_1_18_PRE_RELEASE_6 = 2853
	JE_1_18_PRE_RELEASE_5 = 2851
	JE_1_18_PRE_RELEASE_4 = 2850
	JE_1_18_PRE_RELEASE_3 = 2849
	JE_1_18_PRE_RELEASE_2 = 2848
	JE_1_18_PRE_RELEASE_1 = 2847
	JE_21W44A = 2845
	JE_21W43A = 2844
	JE_21W42A = 2840
	JE_21W41A = 2839
	JE_21W40A = 2838
	JE_21W39A = 2836
	JE_21W38A = 2835
	JE_21W37A = 2834
	JE_1_18_EXPERIMENTAL_SNAPSHOT_7 = 2831
	JE_1_18_EXPERIMENTAL_SNAPSHOT_6 = 2830
	JE_1_18_EXPERIMENTAL_SNAPSHOT_5 = 2829
	JE_1_18_EXPERIMENTAL_SNAPSHOT_4 = 2828
	JE_1_18_EXPERIMENTAL_SNAPSHOT_3 = 2827
	JE_1_18_EXPERIMENTAL_SNAPSHOT_2 = 2826
	JE_1_18_EXPERIMENTAL_SNAPSHOT_1 = 2825
	JE_1_17_1 = 2730
	JE_1_17_1_RELEASE_CANDIDATE_2 = 2729
	JE_1_17_1_RELEASE_CANDIDATE_1 = 2728
	JE_1_17_1_PRE_RELEASE_3 = 2727
	JE_1_17_1_PRE_RELEASE_2 = 2726
	JE_1_17_1_PRE_RELEASE_1 = 2725
	JE_1_17 = 2724
	JE_1_17_RELEASE_CANDIDATE_2 = 2723
	JE_1_17_RELEASE_CANDIDATE_1 = 2722
	JE_1_17_PRE_RELEASE_5 = 2721
	JE_1_17_PRE_RELEASE_4 = 2720
	JE_1_17_PRE_RELEASE_3 = 2719
	JE_1_17_PRE_RELEASE_2 = 2718
	JE_1_17_PRE_RELEASE_1 = 2716
	JE_21W20A = 2715
	JE_21W19A = 2714
	JE_21W18A = 2713
	JE_21W17A = 2712
	JE_21W16A = 2711
	JE_21W15A = 2709
	JE_21W14A = 2706
	JE_21W13A = 2705
	JE_21W11A = 2703
	JE_21W10A = 2699
	JE_21W08B = 2698
	JE_21W08A = 2697
	JE_21W07A = 2695
	JE_21W06A = 2694
	JE_21W05B = 2692
	JE_21W05A = 2690
	JE_21W03A = 2689
	JE_20W51A = 2687
	JE_20W49A = 2685
	JE_20W48A = 2683
	JE_20W46A = 2682
	JE_20W45A = 2681
	JE_COMBAT_TEST_8C = 2707
	JE_COMBAT_TEST_8B = 2706
	JE_COMBAT_TEST_8 = 2705
	JE_COMBAT_TEST_7C = 2704
	JE_COMBAT_TEST_7B = 2703
	JE_COMBAT_TEST_7 = 2702
	JE_COMBAT_TEST_6 = 2701
	JE_1_16_5 = 2586
	JE_1_16_5_RELEASE_CANDIDATE_1 = 2585
	JE_1_16_4 = 2584
	JE_1_16_4_RELEASE_CANDIDATE_1 = 2583
	JE_1_16_4_PRE_RELEASE_2 = 2582
	JE_1_16_4_PRE_RELEASE_1 = 2581
	JE_1_16_3 = 2580
	JE_1_16_3_RELEASE_CANDIDATE_1 = 2579
	JE_1_16_2 = 2578
	JE_1_16_2_RELEASE_CANDIDATE_2 = 2577
	JE_1_16_2_RELEASE_CANDIDATE_1 = 2576
	JE_1_16_2_PRE_RELEASE_3 = 2575
	JE_1_16_2_PRE_RELEASE_2 = 2574
	JE_1_16_2_PRE_RELEASE_1 = 2573
	JE_20W30A = 2572
	JE_20W29A = 2571
	JE_20W28A = 2570
	JE_20W27A = 2569
	JE_1_16_1 = 2567
	JE_1_16 = 2566
	JE_1_16_RELEASE_CANDIDATE_1 = 2565
	JE_1_16_PRE_RELEASE_8 = 2564
	JE_1_16_PRE_RELEASE_7 = 2563
	JE_1_16_PRE_RELEASE_6 = 2562
	JE_1_16_PRE_RELEASE_5 = 2561
	JE_1_16_PRE_RELEASE_4 = 2560
	JE_1_16_PRE_RELEASE_3 = 2559
	JE_1_16_PRE_RELEASE_2 = 2557
	JE_1_16_PRE_RELEASE_1 = 2556
	JE_20W22A = 2555
	JE_20W21A = 2554
	JE_20W20B = 2537
	JE_20W20A = 2536
	JE_20W19A = 2534
	JE_20W18A = 2532
	JE_20W17A = 2529
	JE_20W16A = 2526
	JE_20W15A = 2525
	JE_20W14A = 2524
	JE_20W13B = 2521
	JE_20W13A = 2520
	JE_20W12A = 2515
	JE_20W11A = 2513
	JE_20W10A = 2512
	JE_20W09A = 2510
	JE_20W08A = 2507
	JE_20W07A = 2506
	JE_SNAPSHOT_20W06A = 2504
	JE_COMBAT_TEST_5 = 2321
	JE_COMBAT_TEST_4 = 2320
	JE_1_15_2 = 2230
	JE_1_15_2_PRE_RELEASE_2 = 2229
	JE_1_15_2_PRE_RELEASE_1 = 2228
	JE_1_15_1 = 2227
	JE_1_15_1_PRE_RELEASE_1 = 2226
	JE_1_15 = 2225
	JE_1_15_PRE_RELEASE_7 = 2224
	JE_1_15_PRE_RELEASE_6 = 2223
	JE_1_15_PRE_RELEASE_5 = 2222
	JE_1_15_PRE_RELEASE_4 = 2221
	JE_1_15_PRE_RELEASE_3 = 2220
	JE_1_15_PRE_RELEASE_2 = 2219
	JE_1_15_PRE_RELEASE_1 = 2218
	JE_19W46B = 2217
	JE_19W46A = 2216
	JE_19W45B = 2215
	JE_19W45A = 2214
	JE_19W44A = 2213
	JE_19W42A = 2212
	JE_19W41A = 2210
	JE_19W40A = 2208
	JE_19W39A = 2207
	JE_19W38B = 2206
	JE_19W38A = 2205
	JE_19W37A = 2204
	JE_19W36A = 2203
	JE_19W35A = 2201
	JE_19W34A = 2200
	JE_COMBAT_TEST_3 = 2069
	JE_COMBAT_TEST_2 = 2068
	JE_1_14_3___COMBAT_TEST = 2067
	JE_1_14_4 = 1976
	JE_1_14_4_PRE_RELEASE_7 = 1975
	JE_1_14_4_PRE_RELEASE_6 = 1974
	JE_1_14_4_PRE_RELEASE_5 = 1973
	JE_1_14_4_PRE_RELEASE_4 = 1972
	JE_1_14_4_PRE_RELEASE_3 = 1971
	JE_1_14_4_PRE_RELEASE_2 = 1970
	JE_1_14_4_PRE_RELEASE_1 = 1969
	JE_1_14_3 = 1968
	JE_1_14_3_PRE_RELEASE_4 = 1967
	JE_1_14_3_PRE_RELEASE_3 = 1966
	JE_1_14_3_PRE_RELEASE_2 = 1965
	JE_1_14_3_PRE_RELEASE_1 = 1964
	JE_1_14_2 = 1963
	JE_1_14_2_PRE_RELEASE_4 = 1962
	JE_1_14_2_PRE_RELEASE_3 = 1960
	JE_1_14_2_PRE_RELEASE_2 = 1959
	JE_1_14_2_PRE_RELEASE_1 = 1958
	JE_1_14_1 = 1957
	JE_1_14_1_PRE_RELEASE_2 = 1956
	JE_1_14_1_PRE_RELEASE_1 = 1955
	JE_1_14 = 1952
	JE_1_14_PRE_RELEASE_5 = 1951
	JE_1_14_PRE_RELEASE_4 = 1950
	JE_1_14_PRE_RELEASE_3 = 1949
	JE_1_14_PRE_RELEASE_2 = 1948
	JE_1_14_PRE_RELEASE_1 = 1947
	JE_19W14B = 1945
	JE_19W14A = 1944
	JE_19W13B = 1943
	JE_19W13A = 1942
	JE_19W12B = 1941
	JE_19W12A = 1940
	JE_19W11B = 1938
	JE_19W11A = 1937
	JE_19W09A = 1935
	JE_19W08B = 1934
	JE_19W08A = 1933
	JE_19W07A = 1932
	JE_19W06A = 1931
	JE_19W05A = 1930
	JE_19W04B = 1927
	JE_19W04A = 1926
	JE_19W03C = 1924
	JE_19W03B = 1923
	JE_19W03A = 1922
	JE_19W02A = 1921
	JE_18W50A = 1919
	JE_18W49A = 1916
	JE_18W48B = 1915
	JE_18W48A = 1914
	JE_18W47B = 1913
	JE_18W47A = 1912
	JE_18W46A = 1910
	JE_18W45A = 1908
	JE_18W44A = 1907
	JE_18W43C = 1903
	JE_18W43B = 1902
	JE_18W43A = 1901
	JE_1_13_2 = 1631
	JE_1_13_2_PRE2 = 1630
	JE_1_13_2_PRE1 = 1629
	JE_1_13_1 = 1628
	JE_1_13_1_PRE2 = 1627
	JE_1_13_1_PRE1 = 1626
	JE_18W33A = 1625
	JE_18W32A = 1623
	JE_18W31A = 1622
	JE_18W30B = 1621
	JE_18W30A = 1620
	JE_1_13 = 1519
	JE_1_13_PRE10 = 1518
	JE_1_13_PRE9 = 1517
	JE_1_13_PRE8 = 1516
	JE_1_13_PRE7 = 1513
	JE_1_13_PRE6 = 1512
	JE_1_13_PRE5 = 1511
	JE_1_13_PRE4 = 1504
	JE_1_13_PRE3 = 1503
	JE_1_13_PRE2 = 1502
	JE_1_13_PRE1 = 1501
	JE_18W22C = 1499
	JE_18W22B = 1498
	JE_18W22A = 1497
	JE_18W21B = 1496
	JE_18W21A = 1495
	JE_18W20C = 1493
	JE_18W20B = 1491
	JE_18W20A = 1489
	JE_18W19B = 1485
	JE_18W19A = 1484
	JE_18W16A = 1483
	JE_18W15A = 1482
	JE_18W14B = 1481
	JE_18W14A = 1479
	JE_18W11A = 1478
	JE_18W10D = 1477
	JE_18W10C = 1476
	JE_18W10B = 1474
	JE_18W10A = 1473
	JE_18W09A = 1472
	JE_18W08B = 1471
	JE_18W08A = 1470
	JE_18W07C = 1469
	JE_18W07B = 1468
	JE_18W07A = 1467
	JE_18W06A = 1466
	JE_18W05A = 1464
	JE_18W03B = 1463
	JE_18W03A = 1462
	JE_18W02A = 1461
	JE_18W01A = 1459
	JE_17W50A = 1457
	JE_17W49B = 1455
	JE_17W49A = 1454
	JE_17W48A = 1453
	JE_17W47B = 1452
	JE_17W47A = 1451
	JE_17W46A = 1449
	JE_17W45B = 1448
	JE_17W45A = 1447
	JE_17W43B = 1445
	JE_17W43A = 1444
	JE_1_12_2 = 1343
	JE_1_12_2_PRE2 = 1342
	JE_1_12_2_PRE1 = 1341
	JE_1_12_1 = 1241
	JE_1_12_1_PRE1 = 1240
	JE_17W31A = 1239
	JE_1_12 = 1139
	JE_1_12_PRE7 = 1138
	JE_1_12_PRE6 = 1137
	JE_1_12_PRE5 = 1136
	JE_1_12_PRE4 = 1135
	JE_1_12_PRE3 = 1134
	JE_1_12_PRE2 = 1133
	JE_1_12_PRE1 = 1132
	JE_17W18B = 1131
	JE_17W18A = 1130
	JE_17W17B = 1129
	JE_17W17A = 1128
	JE_17W16B = 1127
	JE_17W16A = 1126
	JE_17W15A = 1125
	JE_17W14A = 1124
	JE_17W13B = 1123
	JE_17W13A = 1122
	JE_17W06A = 1022
	JE_1_11_2 = 922
	JE_1_11_1 = 921
	JE_16W50A = 920
	JE_1_11 = 819
	JE_1_11_PRE1 = 818
	JE_16W44A = 817
	JE_16W43A = 816
	JE_16W42A = 815
	JE_16W41A = 814
	JE_16W40A = 813
	JE_16W39C = 812
	JE_16W39B = 811
	JE_16W39A = 809
	JE_16W38A = 807
	JE_16W36A = 805
	JE_16W35A = 803
	JE_16W33A = 802
	JE_16W32B = 801
	JE_16W32A = 800
	JE_1_10_2 = 512
	JE_1_10_1 = 511
	JE_1_10 = 510
	JE_1_10_PRE2 = 507
	JE_1_10_PRE1 = 506
	JE_16W21B = 504
	JE_16W21A = 503
	JE_16W20A = 501
	JE_1_9_4 = 184
	JE_1_9_3 = 183
	JE_1_9_3_PRE3 = 182
	JE_1_9_3_PRE2 = 181
	JE_1_9_3_PRE1 = 180
	JE_16W15B = 179
	JE_16W15A = 178
	JE_16W14A = 177
	JE_1_9_2 = 176
	JE_1_9_1 = 175
	JE_1_9_1_PRE3 = 172
	JE_1_9_1_PRE2 = 171
	JE_1_9_1_PRE1 = 170
	JE_1_9 = 169
	JE_1_9_PRE4 = 168
	JE_1_9_PRE3 = 167
	JE_1_9_PRE2 = 165
	JE_1_9_PRE1 = 164
	JE_16W07B = 163
	JE_16W07A = 162
	JE_16W06A = 161
	JE_16W05B = 160
	JE_16W05A = 159
	JE_16W04A = 158
	JE_16W03A = 157
	JE_16W02A = 156
	JE_15W51B = 155
	JE_15W51A = 154
	JE_15W50A = 153
	JE_15W49B = 152
	JE_15W49A = 151
	JE_15W47C = 150
	JE_15W47B = 149
	JE_15W47A = 148
	JE_15W46A = 146
	JE_15W45A = 145
	JE_15W44B = 143
	JE_15W44A = 142
	JE_15W43C = 141
	JE_15W43B = 140
	JE_15W43A = 139
	JE_15W42A = 138
	JE_15W41B = 137
	JE_15W41A = 136
	JE_15W40B = 134
	JE_15W40A = 133
	JE_15W39C = 132
	JE_15W39B = 131
	JE_15W39A = 130
	JE_15W38B = 129
	JE_15W38A = 128
	JE_15W37A = 127
	JE_15W36D = 126
	JE_15W36C = 125
	JE_15W36B = 124
	JE_15W36A = 123
	JE_15W35E = 122
	JE_15W35D = 121
	JE_15W35C = 120
	JE_15W35B = 119
	JE_15W35A = 118
	JE_15W34D = 117
	JE_15W34C = 116
	JE_15W34B = 115
	JE_15W34A = 114
	JE_15W33C = 112
	JE_15W33B = 111
	JE_15W33A = 55
	JE_15W32C = 104
	JE_15W32B = 103
	JE_15W32A = 100

def create_2d_schematic(blocks, output_path):
	width = len(blocks[0])
	height = len(blocks)
	mcschematic.Version = Version
	
	schematic = mcschematic.MCSchematic()

	for y in range(height):
		for x in range(width):
			schematic.setBlock((x, 0, y), "end_stone")

	for y in range(height):
		for x in range(width):
			block = blocks[y][x]
			schematic.setBlock((x, 1, y), block)

	schem_name = os.path.splitext(os.path.basename(output_path))[0]
	output_folder = os.path.dirname(output_path)
	schematic.save(output_folder, schem_name, mcschematic.Version.JE_1_20_1)
