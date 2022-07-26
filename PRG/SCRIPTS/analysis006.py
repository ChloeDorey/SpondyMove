import os

import numpy as np
import pandas as pd

import FireFiles as ff
import PATHS


def analysis():
    """
    Get mean maximum angle, median angle, and std for the pelvis and the thorax while trunk flexion.
    """
    # Getting al the repeats for the exercise 007
    all_paths = ff.get_all_files(PATHS.XSENS)
    exercise = "007"
    sheet = "Ergonomic Joint Angles ZXY"
    markers = ["Vertical_Pelvis Flexion/Extension", "Vertical_T8 Flexion/Extension", ]  # add your markers here
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

    identities_results = {"003_DoMa": ([], []), "002_BaEl": ([], []), "004_LoJu": ([], []), "005_LuWi": ([], []),
                          "006_ReCo": ([], []), "007_AmVi": ([], []), "008_GuEm": ([], []), "009_ChCl": ([], []),
                          "010_AnKo": ([], []), "011_YaJu": ([], []), "012_PaMa": ([], []), "013_SaCl": ([], []),
                          "014_MoLu": ([], []), "015_LaJu": ([], []), "016_LaCh": ([], []), "017_GoMa": ([], []),
                          "018_FaFr": ([], []), "019_GuAl": ([], []), "020_PlSi": ([], []), "021_GuGi": ([], []),
                          "022_DrGe": ([], []), }

    for p in all_repeats:
        identity = os.path.basename(os.path.dirname(os.path.dirname(p)))
        df = pd.read_excel(p, sheet_name=sheet)

        identities_results[identity][0].append(round(max(df[markers[0]]), 3)) #copier coller + changer 0 ou 1 pour correspondre aux marqueurs
        identities_results[identity][1].append(round(max(df[markers[1]]), 3))

    # Sum up and writing file
    title = rf"{PATHS.RES}\rom_006.csv"
    columns = "identity,mean maximum pelvis angle,median pelvis angle,std pelvis angle,mean maximum thorax angle," \
              "median thorax angle,std thorax angle\n"  # if new metric, add the column here

    with open(title, "w+") as f:
        lines = []
        lines.insert(0, columns)
        for id in identities_results:
            mean_pelvis = np.mean(identities_results[id][0])
            mean_thorax = np.mean(identities_results[id][1])
            std_pelvis = np.std(identities_results[id][0])
            std_thorax = np.std(identities_results[id][1])
            median_pelvis = np.median(identities_results[id][0])
            median_thorax = np.median(identities_results[id][1])  # add your metric here (based on all repeats)

            new_line = f"{id},{round(mean_pelvis, 3)},{round(median_pelvis, 3)},{round(std_pelvis, 3)}," \
                       f"{round(mean_thorax, 3)},{round(median_thorax, 3)},{round(std_thorax, 3)}\n"  # add the metric in new_line
            lines.append(new_line)
        for line in lines:
            f.write(line)

