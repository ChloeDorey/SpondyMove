import os

import numpy as np
import pandas as pd

import FireFiles as ff
import PATHS


def analysis():
    """
    Get mean, median angle, and std duration from pelvis and thorax while lateral tilting of the chest (both sides).
    """
    # Getting al the repeats for the exercise 005 and 006
    all_paths = ff.get_all_files(PATHS.XSENS)
    exercise = ["005", "006"]
    sheet = "Ergonomic Joint Angles ZXY"
    markers = ["Vertical_Pelvis Lateral Bending", "Vertical_T8 Lateral Bending", "Vertical_Pelvis Lateral Bending", "Vertical_T8 Lateral Bending", ]  # add your markers here
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

    identities_results = {"003_DoMa": ([], [],[], []), "002_BaEl": ([], [],[], []), "004_LoJu": ([], [],[], []), "005_LuWi": ([], [],[], []),
                          "006_ReCo": ([], [],[], []), "007_AmVi": ([], [],[], []), "008_GuEm": ([], [],[], []), "009_ChCl": ([], [],[], []),
                          "010_AnKo": ([], [],[], []), "011_YaJu": ([], [],[], []), "012_PaMa": ([], [],[], []), "013_SaCl": ([], [],[], []),
                          "014_MoLu": ([], [],[], []), "015_LaJu": ([], [],[], []), "016_LaCh": ([], [],[], []), "017_GoMa": ([], [],[], []),
                          "018_FaFr": ([], [],[], []), "019_GuAl": ([], [],[], []), "020_PlSi": ([], [],[], []), "021_GuGi": ([], [],[], []),
                          "022_DrGe": ([], [],[], []), }

    for p in all_repeats:
        identity = os.path.basename(os.path.dirname(os.path.dirname(p)))
        df = pd.read_excel(p, sheet_name=sheet)

        if os.path.basename(p).split("-")[0] == exercise[0]:
            identities_results[identity][0].append(round(max(df[markers[0]]), 3))  # copier coller + changer 0 ou 1 pour correspondre aux marqueurs
            identities_results[identity][1].append(round(max(df[markers[1]]), 3))
        elif os.path.basename(p).split("-")[0] == exercise[1]:
            identities_results[identity][2].append(round(max(df[markers[2]]), 3))  # copier coller + changer 0 ou 1 pour correspondre aux marqueurs
            identities_results[identity][3].append(round(max(df[markers[3]]), 3))

    # Sum up and writing file
    title = rf"{PATHS.RES}\rom_005.csv"
    columns = "identity,mean maximum pelvis first angle,median pelvis first angle,std pelvis first angle," \
              "mean maximum thorax first angle,median thorax first angle,std thorax first angle," \
              "mean maximum pelvis second angle,median pelvis second angle,std pelvis second angle," \
              "mean maximum thorax second angle,median thorax second angle,std thorax second angle\n"  # if new metric, add the column here

    for xid in range(len(identities)):
        with open(title, "w+") as f:
            lines = []  # initialisation de toutes les lignes
            lines.insert(0, columns)
            for id in identities_results:
                mean_pelvis1 = np.mean(identities_results[id][0])
                mean_thorax1 = np.mean(identities_results[id][1])
                std_pelvis1 = np.std(identities_results[id][0])
                std_thorax1 = np.std(identities_results[id][1])
                median_pelvis1 = np.median(identities_results[id][0])
                median_thorax1 = np.median(identities_results[id][1])
                mean_pelvis2 = np.mean(identities_results[id][2])
                mean_thorax2 = np.mean(identities_results[id][3])
                std_pelvis2 = np.std(identities_results[id][2])
                std_thorax2 = np.std(identities_results[id][3])
                median_pelvis2 = np.median(identities_results[id][2])
                median_thorax2 = np.median(identities_results[id][3])  # add your metric here (based on all repeats)

                new_line1 = f"{id},{round(mean_pelvis1, 3)},{round(median_pelvis1, 3)},{round(std_pelvis1, 3)}," \
                       f"{round(mean_thorax1, 3)},{round(median_thorax1, 3)},{round(std_thorax1, 3)}," \
                        f"{round(mean_pelvis2, 3)},{round(median_pelvis2, 3)},{round(std_pelvis2, 3)}," \
                        f"{round(mean_thorax2, 3)},{round(median_thorax2, 3)},{round(std_thorax2, 3)}\n"  # add the metric in new_line

                lines.append(new_line1)  # on ajoute notre nouvelle ligne à la liste de toutes les lignes
            for line in lines:  # on parcourt toutes les lignes de notre liste
                f.write(line)
