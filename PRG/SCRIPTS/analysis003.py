import os

import numpy as np
import pandas as pd

import FireFiles as ff
import PATHS


def analysis():
    """
    Get mean maximum angle, median angle, and std for the hips and the knees while going up and down stairs. 
    There are 3 steps per repeat.
    """
    # Getting al the repeats for the exercise 003
    all_paths = ff.get_all_files(PATHS.XSENS)
    exercise = "003"
    sheet = "Joint Angles ZXY"
    markers = ["Right Hip Flexion/Extension", "Right Knee Flexion/Extension", "Left Hip Flexion/Extension", "Left Knee Flexion/Extension", ]  # add your markers here
    all_repeats = []
    for p in all_paths:
        if exercise + "-repeat" in p:
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

    identities_results = {"003_DoMa": ([], [], [], []), "002_BaEl": ([], [], [], []), "004_LoJu": ([], [], [], []), "005_LuWi": ([], [], [], []),
                          "006_ReCo": ([], [], [], []), "007_AmVi": ([], [], [], []), "008_GuEm": ([], [], [], []), "009_ChCl": ([], [], [], []),
                          "010_AnKo": ([], [], [], []), "011_YaJu": ([], [], [], []), "012_PaMa": ([], [], [], []), "013_SaCl": ([], [], [], []),
                          "014_MoLu": ([], [], [], []), "015_LaJu": ([], [], [], []), "016_LaCh": ([], [], [], []), "017_GoMa": ([], [], [], []),
                          "018_FaFr": ([], [], [], []), "019_GuAl": ([], [], [], []), "020_PlSi": ([], [], [], []), "021_GuGi": ([], [], [], []),
                          "022_DrGe": ([], [], [], []), }

    for p in all_repeats:
        identity = os.path.basename(os.path.dirname(os.path.dirname(p)))
        df = pd.read_excel(p, sheet_name=sheet)

        identities_results[identity][0].append(round(min(df[markers[0]]), 3))
        identities_results[identity][1].append(round(min(df[markers[1]]), 3))
        identities_results[identity][2].append(round(min(df[markers[2]]), 3))
        identities_results[identity][3].append(round(min(df[markers[3]]), 3))  # calculation of the metric for one repeat here

    # Sum up and writing file
    title = rf"{PATHS.RES}\rom_003.csv"
    columns = "identity,mean maximum right_hip angle,median right_hip angle,std right_hip angle,mean maximum right_knee angle," \
              "median right_knee angle,std right_knee angle,mean maximum left_hip angle,median left_hip angle," \
              "std left_hip angle,mean maximum left_knee angle,median left_knee angle,std left_knee angle\n"  # if new metric, add the column here

    with open(title, "w+") as f:
        lines = []
        lines.insert(0, columns)
        for id in identities_results:
            mean_left_hip = np.mean(identities_results[id][0])
            mean_right_hip = np.mean(identities_results[id][1])
            mean_left_knee = np.mean(identities_results[id][2])
            mean_right_knee = np.mean(identities_results[id][3])
            std_left_hip = np.std(identities_results[id][0])
            std_left_knee = np.std(identities_results[id][1])
            std_right_hip = np.std(identities_results[id][2])
            std_right_knee = np.std(identities_results[id][3])
            median_left_hip = np.median(identities_results[id][0])
            median_left_knee = np.median(identities_results[id][1])
            median_right_hip = np.median(identities_results[id][2])
            median_right_knee = np.median(identities_results[id][3])  # add your metric here (based on all repeats)

            new_line = f"{id},{round(mean_left_hip, 3)},{round(median_left_hip, 3)},{round(std_left_hip, 3)}," \
                       f"{round(mean_left_knee, 3)},{round(median_left_knee, 3)},{round(std_left_knee, 3)}," \
                       f"{round(mean_right_hip, 3)},{round(median_right_hip, 3)},{round(std_right_hip, 3)}," \
                       f"{round(mean_right_knee, 3)},{round(median_right_knee, 3)},{round(std_right_knee, 3)}\n"  # add the metric in new_line
            lines.append(new_line)
        for line in lines:
            f.write(line)

