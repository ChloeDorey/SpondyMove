import os

import numpy as np
import pandas as pd
import skinematics

import FireFiles as ff
import PATHS


def analysis():
    """
    Get maximum angle of rotation between the hand and the thorax while rotating the trunk.
    """
    # Getting al the repeats for the exercise 008 and 009
    all_paths = ff.get_all_files(PATHS.XSENS)
    exercise = ["008", "009"]
    sheet = "Segment Position"
    markers = ["Left Hand x", "Left Hand y", "Left Hand z", "T8 x", "T8 y", "T8 z", "Right Hand x", "Right Hand y", "Right Hand z", ]  # add your markers here
    all_repeats = []
    for p in all_paths:
        if exercise[0] + "-repeat" in p:
            all_repeats.append(p)
        if exercise[1] + "-repeat" in p:
            all_repeats.append(p)

    # Getting the different participating people
    identities = []
    for r in all_repeats:
        identity = os.path.basename(os.path.dirname(os.path.dirname(r)))
        already_exist = False
        for id in identities:
            if identity in id:
                already_exist = True
        if not already_exist:
            identities.append(identity)

    identities_results = {"003_DoMa": ([], [], [], [], [], []), "002_BaEl": ([], [], [], [], [], []), "004_LoJu": ([], [], [], [], [], []),
                          "005_LuWi": ([], [], [], [], [], []),
                          "006_ReCo": ([], [], [], [], [], []), "007_AmVi": ([], [], [], [], [], []), "008_GuEm": ([], [], [], [], [], []),
                          "009_ChCl": ([], [], [], [], [], []),
                          "010_AnKo": ([], [], [], [], [], []), "011_YaJu": ([], [], [], [], [], []), "012_PaMa": ([], [], [], [], [], []),
                          "013_SaCl": ([], [], [], [], [], []),
                          "014_MoLu": ([], [], [], [], [], []), "015_LaJu": ([], [], [], [], [], []), "016_LaCh": ([], [], [], [], [], []),
                          "017_GoMa": ([], [], [], [], [], []),
                          "018_FaFr": ([], [], [], [], [], []), "019_GuAl": ([], [], [], [], [], []), "020_PlSi": ([], [], [], [], [], []),
                          "021_GuGi": ([], [], [], [], [], []),
                          "022_DrGe": ([], [], [], [], [], []), }


    for p in all_repeats:
        identity = os.path.basename(os.path.dirname(os.path.dirname(p)))
        df = pd.read_excel(p, sheet_name=sheet)

        if os.path.basename(p).split("-")[0] == exercise[0]:

            first_hand_begin_vector = [round(df[markers[0]][0], 3), round(df[markers[1]][0], 3), round(df[markers[2]][0], 3)]
            identities_results[identity][0].append(first_hand_begin_vector)

            first_hand_end_vector = [round(max(df[markers[0]]), 3), round(max(df[markers[1]]), 3),
                                      round(max(df[markers[2]]), 3)]
            identities_results[identity][1].append(first_hand_end_vector)

            thorax_vector = [round(max(df[markers[3]]), 3), round(max(df[markers[4]]), 3), round(max(df[markers[5]]), 3)]
            identities_results[identity][2].append(thorax_vector)  # calculation of the metric for one repeat here
        elif os.path.basename(p).split("-")[0] == exercise[1]:
            second_hand_begin_vector = [round(df[markers[0]][0], 3), round(df[markers[1]][0], 3),
                                      round(df[markers[2]][0], 3)]
            identities_results[identity][3].append(second_hand_begin_vector)

            second_hand_end_vector = [round(max(df[markers[0]]), 3), round(max(df[markers[1]]), 3),
                                    round(max(df[markers[2]]), 3)]
            identities_results[identity][4].append(second_hand_end_vector)
            thorax_vector = [round(max(df[markers[3]]), 3), round(max(df[markers[4]]), 3), round(max(df[markers[5]]), 3)]

            identities_results[identity][5].append(thorax_vector)  # calculation of the metric for one repeat here


    # Sum up and writing file
    title = rf"{PATHS.RES}\rom_007.csv"
    columns = "identity,first angle,second angle\n"  # if new metric, add the column here

    for xid in range(len(identities)):
        with open(title, "w+") as f:
            lines = []  # initialisation de toutes les lignes
            lines.insert(0, columns)

            for id in identities_results:
                first_hand_arrays_begin = [np.array(x) for x in identities_results[id][0]]
                first_hand_pos_begin_mean_vector = [np.mean(k) for k in zip(*first_hand_arrays_begin)]

                second_hand_arrays_begin = [np.array(x) for x in identities_results[id][1]]
                second_hand_pos_begin_mean_vector = [np.mean(k) for k in zip(*second_hand_arrays_begin)]

                first_hand_arrays_end = [np.array(x) for x in identities_results[id][2]]
                first_hand_pos_end_mean_vector = [np.mean(k) for k in zip(*first_hand_arrays_end)]

                second_hand_arrays_end = [np.array(x) for x in identities_results[id][3]]
                second_hand_pos_end_mean_vector = [np.mean(k) for k in zip(*second_hand_arrays_end)]

                first_thorax_arrays_begin = [np.array(x) for x in identities_results[id][4]]
                first_thorax_pos_mean_vector = [np.mean(k) for k in zip(*first_thorax_arrays_begin)]

                first_begin_vector = [first_hand_pos_begin_mean_vector[0] - first_thorax_pos_mean_vector[0],
                                      first_hand_pos_begin_mean_vector[1] - first_thorax_pos_mean_vector[1],
                                      first_hand_pos_begin_mean_vector[2] - first_thorax_pos_mean_vector[2], ]

                first_end_vector = [first_hand_pos_end_mean_vector[0] - first_thorax_pos_mean_vector[0],
                                    first_hand_pos_end_mean_vector[1] - first_thorax_pos_mean_vector[1],
                                    first_hand_pos_end_mean_vector[2] - first_thorax_pos_mean_vector[2], ]

                first_angle = round(skinematics.vector.angle(first_begin_vector, first_end_vector), 3)

                second_begin_vector = [second_hand_pos_begin_mean_vector[0] - first_thorax_pos_mean_vector[0],
                                       second_hand_pos_begin_mean_vector[1] - first_thorax_pos_mean_vector[1],
                                       second_hand_pos_begin_mean_vector[2] - first_thorax_pos_mean_vector[2], ]

                second_end_vector = [second_hand_pos_end_mean_vector[0] - first_thorax_pos_mean_vector[0],
                                     second_hand_pos_end_mean_vector[1] - first_thorax_pos_mean_vector[1],
                                     second_hand_pos_end_mean_vector[2] - first_thorax_pos_mean_vector[2], ]

                second_angle = round(skinematics.vector.angle(second_begin_vector, second_end_vector), 3)

                new_line1 = f"{id},{round(first_angle, 3)},{round(second_angle, 3)}\n"  # add the metric in new_line

                lines.append(new_line1)
            for line in lines:
                f.write(line)

